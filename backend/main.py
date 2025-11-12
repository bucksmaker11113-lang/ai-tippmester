from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.vision.vision_processor import VisionAnalyzer
import uvicorn
import os
import io

app = FastAPI(title="Tippmester AI 5.3 Vision Live Edition")

# CORS beállítások
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vision modul inicializálás
vision = VisionAnalyzer()

@app.get("/")
def root():
    return {"message": "Tippmester AI 5.3 Vision Live Edition is running 🚀"}

# ----------------------------
# 📸 KÉPFELISMERÉS ENDPOINT
# ----------------------------
@app.post("/vision/analyze_image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = vision.analyze_image(contents)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ----------------------------
# 🔧 EGYÉB HELPER ENDPOINTOK
# ----------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/version")
def get_version():
    return {"version": "5.3", "name": "Vision Live Edition"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
