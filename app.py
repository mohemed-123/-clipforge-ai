import os, subprocess, uuid, threading
from flask import Flask, render_template, request, jsonify, send_from_directory

BASE=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(BASE,"data")
os.makedirs(DATA,exist_ok=True)
app=Flask(__name__)

jobs={}

def run_job(job_id, src, length):
    outdir=os.path.join(DATA,job_id); os.makedirs(outdir,exist_ok=True)
    jobs[job_id]={"status":"processing","progress":10,"clips":[]}
    try:
        # Create one clean vertical clip from the requested section.
        # This starter server is intentionally simple and can be upgraded with
        # Whisper/highlight ranking after deployment.
        out=os.path.join(outdir,"clip_01.mp4")
        vf="scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
        cmd=["ffmpeg","-y","-i",src,"-t",str(length),"-vf",vf,
             "-c:v","libx264","-preset","ultrafast","-crf","28",
             "-c:a","aac","-movflags","+faststart",out]
        subprocess.run(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
        jobs[job_id]={"status":"done","progress":100,
                      "clips":[f"/files/{job_id}/clip_01.mp4"]}
    except Exception as e:
        jobs[job_id]={"status":"error","progress":100,"error":str(e)}

@app.route("/")
def index(): return render_template("index.html")

@app.post("/api/process")
def process():
    f=request.files.get("video")
    if not f: return jsonify(error="Upload a video first."),400
    length=max(30,min(90,int(request.form.get("length","60"))))
    job_id=uuid.uuid4().hex
    folder=os.path.join(DATA,job_id); os.makedirs(folder,exist_ok=True)
    src=os.path.join(folder,"source.mp4"); f.save(src)
    jobs[job_id]={"status":"queued","progress":0,"clips":[]}
    threading.Thread(target=run_job,args=(job_id,src,length),daemon=True).start()
    return jsonify(job_id=job_id)

@app.get("/api/jobs/<job_id>")
def status(job_id):
    return jsonify(jobs.get(job_id,{"status":"unknown"}))

@app.get("/files/<job_id>/<path:name>")
def files(job_id,name):
    return send_from_directory(os.path.join(DATA,job_id),name,as_attachment=False)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",8000)))
