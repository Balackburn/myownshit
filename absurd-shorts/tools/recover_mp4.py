"""recover_mp4.py BROKEN.mp4 REFERENCE.mp4 OUT.h264: an H.264 MP4 whose writer was killed (no moov atom) -> an Annex-B stream. The mdat of such a
file is a run of [4-byte length][NAL unit]; the parameter sets (SPS, PPS) are taken from a finished file written by the same encoder with the same
settings (REFERENCE). A truncated last unit is dropped. Then: ffmpeg -r 30 -i OUT.h264 ... (decode it; the tail may lose its last few frames)."""
import struct, sys
src, ref, out = sys.argv[1:4]
b = open(ref, 'rb').read(); i = b.find(b'avcC'); assert i > 0, 'no avcC in the reference'
p = i + 4; p += 5; nsps = b[p] & 31; p += 1; sets = []
for _ in range(nsps): n = struct.unpack('>H', b[p:p + 2])[0]; sets.append(b[p + 2:p + 2 + n]); p += 2 + n
npps = b[p]; p += 1
for _ in range(npps): n = struct.unpack('>H', b[p:p + 2])[0]; sets.append(b[p + 2:p + 2 + n]); p += 2 + n
d = open(src, 'rb').read(); m = d.find(b'mdat'); assert m > 0; p = m + 4; SC = b'\x00\x00\x00\x01'; o = [SC + x for x in sets]; n_units = 0; kinds = {}
while p + 4 <= len(d):
    n = struct.unpack('>I', d[p:p + 4])[0]
    if n == 0 or p + 4 + n > len(d): break
    nal = d[p + 4:p + 4 + n]; t = nal[0] & 31
    if nal[0] & 0x80 or t == 0 or t > 23: break            # not a NAL unit: the data stops making sense here
    kinds[t] = kinds.get(t, 0) + 1; o.append(SC + nal); p += 4 + n; n_units += 1
open(out, 'wb').write(b''.join(o)); print(src, '->', out, n_units, 'units', kinds, 'stopped at byte', p, 'of', len(d))
