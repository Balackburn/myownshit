# MDX-Net (UVR Inst HQ 3) inference with onnxruntime + numpy STFT matching torch.stft(center=True, reflect, periodic hann)
import numpy as np, onnxruntime as ort, sys, wave
N_FFT, HOP, DIM_F, DIM_T, COMP = 6144, 1024, 3072, 256, 1.022
CH = HOP * (DIM_T - 1); TRIM = N_FFT // 2; GEN = CH - 2 * TRIM; NB = N_FFT // 2 + 1
win = (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N_FFT) / N_FFT)).astype(np.float32)
def stft(x):  # x [2, CH] -> [1, 4, DIM_F, DIM_T]
    out = []
    for c in range(2):
        xp = np.pad(x[c], N_FFT // 2, mode='reflect')
        fr = np.stack([xp[t * HOP: t * HOP + N_FFT] * win for t in range(DIM_T)], 1)   # [N_FFT, T]
        S = np.fft.rfft(fr, axis=0)                                                    # [NB, T]
        out += [S.real, S.imag]
    return np.stack(out)[None, :, :DIM_F, :].astype(np.float32)
def istft(s):  # [1, 4, DIM_F, DIM_T] -> [2, CH]
    s = np.concatenate([s[0], np.zeros((4, NB - DIM_F, DIM_T), np.float32)], 1)
    res = []
    for c in range(2):
        S = s[2 * c] + 1j * s[2 * c + 1]
        fr = np.fft.irfft(S, n=N_FFT, axis=0) * win[:, None]
        L = N_FFT + HOP * (DIM_T - 1); y = np.zeros(L); env = np.zeros(L)
        for t in range(DIM_T): y[t * HOP: t * HOP + N_FFT] += fr[:, t]; env[t * HOP: t * HOP + N_FFT] += win ** 2
        y = y / np.maximum(env, 1e-8); res.append(y[N_FFT // 2: N_FFT // 2 + CH])
    return np.stack(res)
sess = ort.InferenceSession('Inst_HQ_3.onnx', providers=['CPUExecutionProvider'])
mix = np.fromfile(sys.argv[1], np.float32).reshape(-1, 2).T.astype(np.float32)   # [2, N]
N = mix.shape[1]; padded = np.concatenate([np.zeros((2, TRIM), np.float32), mix, np.zeros((2, GEN + TRIM), np.float32)], 1)
inst = np.zeros_like(padded)
for i in range(0, N, GEN):
    chunk = padded[:, i:i + CH]
    if chunk.shape[1] < CH: chunk = np.pad(chunk, ((0, 0), (0, CH - chunk.shape[1])))
    spec = stft(chunk)
    pred = 0.5 * sess.run(None, {'input': spec})[0] - 0.5 * sess.run(None, {'input': -spec})[0]   # denoise trick
    wav = istft(pred)
    inst[:, i + TRIM: i + TRIM + GEN] = wav[:, TRIM:TRIM + GEN]
    print('chunk', i // GEN, flush=True)
inst = inst[:, TRIM:TRIM + N] * COMP; voc = mix - inst
def save(p, x):
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100); w.writeframes((np.clip(x.T, -1, 1) * 32767).astype('<i2').tobytes())
save('instrumental.wav', inst); save('vocals.wav', voc)
db = lambda x: 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
for t in np.arange(0, 28.8, 1.0):
    a, b = int(t * 44100), int((t + 1) * 44100)
    print(f'{t:4.1f}s mix {db(mix[:, a:b]):6.1f}  inst {db(inst[:, a:b]):6.1f}  voc {db(voc[:, a:b]):6.1f}')
