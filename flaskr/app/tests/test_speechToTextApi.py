import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from speech_to_text_api.speech_to_text_api import transcribe_audio
from faster_whisper import WhisperModel

class TestTranscribeAudio(unittest.TestCase):
    def setUp(self):
        self.model_size = "distil-large-v3"
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
        self.test_audio_path = "MLKDream_64kb.mp3"  # Replace with your test audio file path

    def test_transcribe_audio(self):
        transcription = transcribe_audio(self.test_audio_path)
        # Add your assertions here to check the expected transcription
        self.assertIsNotNone(transcription)
        # You can add more specific assertions based on the expected content of the transcription
        self.assertIn("Dr. Martin Luther King", transcription)  # Replace with an expected word

if __name__ == '__main__':
    unittest.main()