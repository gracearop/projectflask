from faster_whisper import WhisperModel

model_size = "distil-large-v3"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

def transcribe_audio(filepath):
    # Transcribe the audio file
    segments, _ = model.transcribe(filepath, beam_size=5, language="en", condition_on_previous_text=False)
    # Combine all segments into a single string
    transcription = " ".join([segment.text for segment in segments])
    return transcription