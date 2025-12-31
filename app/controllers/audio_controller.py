from fastapi import UploadFile, HTTPException
import tempfile
import os
import shutil
from app.services.azure_transcription_service import azure_transcription_service

class AudioController:
    async def transcribe_audio(self, file: UploadFile):
        # Save uploaded file to temp
        suffix = os.path.splitext(file.filename)[1] if file.filename else ".webm"
        # Ensure suffix is valid for ffmpeg if possible, but webm is fine
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        wav_path = None
        try:
            # Convert to wav (16kHz mono) using extract_audio_from_video
            # We use a temp path for the wav output
            wav_path = tmp_path + "_converted.wav"
            
            # Use the static method from the class, or the instance method if it's bound
            # The service instance has the method.
            success = await azure_transcription_service.extract_audio_from_video(tmp_path, wav_path)
            
            if not success:
                 raise HTTPException(status_code=500, detail="Audio conversion failed")
            
            # Transcribe
            success, text, segments, confidence = await azure_transcription_service.transcribe_with_diarization(wav_path)
            
            if not success:
                 raise HTTPException(status_code=500, detail="Transcription failed")
            
            return {"text": text, "segments": segments}
            
        finally:
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except:
                    pass
            if wav_path and os.path.exists(wav_path):
                try:
                    os.remove(wav_path)
                except:
                    pass

audio_controller = AudioController()
