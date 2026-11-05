# 01-tornado-fr: French version of the tornado replica

Same picture as `../01-tornado-reverse` (the 3D layer of `absurd-shorts/scripts-fr/replica_tornado.py`), with:

- the French narration: 14 lines (`tools/lines_fr.json`) spoken by the narrator voice of the French series (ElevenLabs,
  `/with-timestamps` word timings). Each line starts on the English line's start, pushed later only while the previous
  line is still speaking;
- the original's music and effects under it: separated from the English voice with an MDX-Net model (UVR Inst HQ 3,
  onnxruntime, `tools/separate_mdx.py`). The French voice sits at the English voice's loudness; the mix is -16 LUFS
  like the original;
- French captions in the original's style, timed to the spoken words; VOL on the title card; VERROUILLÉ on the lock-on tag.

Rebuild (from a work folder holding `lines_fr.json`):

```bash
export ELEVENLABS_API_KEY=...   # environment only, never in a file
python3 tts_fr.py               # per-line mp3 + word timings -> timed_fr.json
python3 build_fr.py             # compositions/captions.html + voice_fr.wav
python3 separate_mdx.py orig.f32   # instrumental.wav (needs UVR-MDX-NET-Inst_HQ_3.onnx next to it)
ffmpeg -i instrumental.wav -i voice_fr.wav -filter_complex "[1:a]volume=2.7dB,aformat=channel_layouts=stereo[v];[0:a][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89:level=false" assets/audio_fr.wav
npx --yes hyperframes@0.9.13 render -o renders/tornado_fr.mp4 --fps 30
```
