============================================================
Whisper → Text in Snowflake (Audio-File Workflow)
My exact end‑to‑end setup (commands + files), in order
Project: WHISPER_TRANSCRIBE
============================================================

This guide captures exactly what I've chosen and done so far, then finishes
the remaining steps so I can run my first transcription.

I chose:
- Audio files (not live/streaming) → transcribe with Whisper (faster-whisper)
- Source code in my GitHub/VS Code workspace
- Build locally with Docker and push to Snowflake Image Repository
- Snowflake project/database named: WHISPER_TRANSCRIBE
- Image repository: WHISPER_REPO
- Stages: svc_stage (for spec), audio_stage (for audio)
- Image pushed to: sdriskw-xw90326.registry.snowflakecomputing.com/whisper_transcribe/app/whisper_repo/whisper-api:0.1

------------------------------------------------------------
0) Prerequisites (one-time on my laptop/VS Code dev box)
------------------------------------------------------------
- Docker Desktop running and working:  `docker version`
- Access to Snowflake (worksheet + role with SCS privileges)
- A small audio test file handy (e.g., meeting.m4a)

Tip: If I am on Codespaces or a remote dev container, Docker must be available
inside that environment. I check with: `docker ps` and `docker images`.

------------------------------------------------------------
1) Snowflake scaffolding (I ALREADY ran this)
------------------------------------------------------------
-- Create and select a clean home for everything
CREATE DATABASE IF NOT EXISTS WHISPER_TRANSCRIBE;
CREATE SCHEMA  IF NOT EXISTS WHISPER_TRANSCRIBE.APP;
USE SCHEMA WHISPER_TRANSCRIBE.APP;

-- Create an image repository (where I'll push the Docker image)
CREATE IMAGE REPOSITORY IF NOT EXISTS WHISPER_REPO;

-- Create two stages:
-- 1) svc_stage: to hold the service spec (YAML)
-- 2) audio_stage: to upload audio files I'll transcribe
CREATE STAGE IF NOT EXISTS svc_stage;
CREATE STAGE IF NOT EXISTS audio_stage ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');

-- Confirm the image repository URL (REPO_URL)
SHOW IMAGE REPOSITORIES LIKE 'WHISPER_REPO';

-- (Later) verify the pushed image
SHOW IMAGES IN IMAGE REPOSITORY WHISPER_TRANSCRIBE.APP.WHISPER_REPO;

------------------------------------------------------------
2) VS Code / GitHub workspace (I CREATED these files)
------------------------------------------------------------
I created this folder in my repo:  whisper-service/

whisper-service/
├── app.py
├── requirements.txt
└── Dockerfile

---- requirements.txt ----
fastapi
uvicorn[standard]
faster-whisper
ffmpeg-python
requests
--------------------------

---- app.py ----
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
---------------------------

---- Dockerfile ----
FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
ENV PORT=8000 WHISPER_MODEL=small WHISPER_COMPUTE=auto
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
--------------------

Build locally:
cd whisper-service
docker build -t whisper-api:0.1 .

------------------------------------------------------------
3) Tag, login, and PUSH image to Snowflake (I DID this)
------------------------------------------------------------
# Replace with the repo URL from SHOW IMAGE REPOSITORIES
export REPO_URL="sdriskw-xw90326.registry.snowflakecomputing.com/whisper_transcribe/app/whisper_repo"

docker tag whisper-api:0.1 $REPO_URL/whisper-api:0.1
docker login sdriskw-xw90326.registry.snowflakecomputing.com
docker push $REPO_URL/whisper-api:0.1

Verify in Snowflake:
USE SCHEMA WHISPER_TRANSCRIBE.APP;
SHOW IMAGES IN IMAGE REPOSITORY WHISPER_TRANSCRIBE.APP.WHISPER_REPO;

Expected line: (If no return then nothing is there)
whisper-api | 0.1 | sha256:<digest> | whisper_transcribe/app/whisper_repo/whisper-api:0.1




---------------------------------------------------------------------------
4) Computing Pool
---------------------------------------------------------------------------
Next Step I created an computing POOL here


USE SCHEMA WHISPER_TRANSCRIBE.APP;


CREATE COMPUTE POOL IF NOT EXISTS WHISPER_CPU
  MIN_NODES = 1
  MAX_NODES = 1
  INSTANCE_FAMILY = CPU_X64_M;

-- If need more RAM instead, use:
-- CREATE COMPUTE POOL IF NOT EXISTS WHISPER_CPU
--   MIN_NODES = 1
--   MAX_NODES = 1
--   INSTANCE_FAMILY = HIGHMEM_X64_S;

SHOW COMPUTE POOLS;





---------------------------------------------------------------------------
5) Snowflake CLI connection
---------------------------------------------------------------------------
I discovered That I need the CLI connection to Snowflake in order to upload the spec.yml file So this will be a setup for that


I first Ren downloading commands : 

# Download installer (latest version)
curl -O https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.28-linux_x86_64.bash
# Install it (accept defaults)
bash snowsql-1.2.28-linux_x86_64.bash


Then expoted the path and checked for version after 

echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
snowsql -v



Step 2 of CLI setup
------------------------------------------------------------------------------

First I will create the connexion file and edit it inside config file in order to start conenxions

mkdir -p ~/.snowsql
nano ~/.snowsql/config

Then I modified the connection file to have this specs
I dont put the possword for it not to be compromised xD, happy to retype it evcery time I run the command

[connections.my_snowflake]
accountname = sdriskw-xw90326
username = Lazar1244
rolename = ACCOUNTADMIN
dbname = WHISPER_TRANSCRIBE
schemaname = APP
warehousename = COMPUTE_WH
password = 




Then I call the snowsql command to connect : 

snowsql -c my_snowflake -q "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_DATABASE();"



Once I am connected I get :

* SnowSQL * v1.2.32
Type SQL statements or !help
+----------------+----------------+--------------------+                        
| CURRENT_USER() | CURRENT_ROLE() | CURRENT_DATABASE() |
|----------------+----------------+--------------------|
| LAZAR1244      | ACCOUNTADMIN   | WHISPER_TRANSCRIBE |
+----------------+----------------+--------------------+


---------------------------------------------------------------------------
6) Sending the spec.yml
------------------------------------------------------------------------------------------------
Now that i connected through CLI I can send the yml to snoflake, I go into my wisper-service folder and send it fromù there sienc that is where the spec.yml is


cd /workspaces/WhisperForg/whisper-service
snowsql -c my_snowflake -q "PUT file://spec.yml @WHISPER_TRANSCRIBE.APP.svc_stage AUTO_COMPRESS=FALSE OVERWRITE=TRUE;"




7) Now I create the service inside the Snowflake with following sql querry inside the setup file 




