from fastapi import FastAPI, UploadFile, File, Form
from faster_whisper import WhisperModel
import tempfile, requests, os, subprocess, uuid

MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")
COMPUTE_TYPE = os.getenv("WHISPER_COMPUTE", "auto")  # "auto" uses GPU if present
model = WhisperModel(MODEL_SIZE, compute_type=COMPUTE_TYPE)

app = FastAPI()

def ensure_wav(path_in):
    out = f"{path_in}.wav"
    subprocess.run(
        ["ffmpeg","-y","-i",path_in,"-ac","1","-ar","16000",out],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return out

@app.post("/asr")
async def asr(
    url: str | None = Form(default=None),
    language: str | None = Form(default=None),
    file: UploadFile | None = File(default=None)
):
    with tempfile.TemporaryDirectory() as td:
        raw = os.path.join(td, f"{uuid.uuid4().hex}")
        if url:
            r = requests.get(url, timeout=120); r.raise_for_status()
            open(raw, "wb").write(r.content)
        elif file:
            open(raw, "wb").write(await file.read())
        else:
            return {"error":"Provide 'url' (presigned) or 'file'."}

        wav = ensure_wav(raw)
        segments, info = model.transcribe(wav, language=language, vad_filter=True)
        text = "".join(s.text for s in segments).strip()
        segs = [{"start": s.start, "end": s.end, "text": s.text}
                for s in model.transcribe(wav, language=language)[0]]
        return {"language": info.language, "duration": info.duration, "text": text, "segments": segs}
