import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Adjust sys.path to include the root directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from app import transcribe_audio
from app import classify_text
from app import upload_audio

from app import create_app  # Now you can use the absolute import

class TestUploadAudio(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = '/tmp/uploads'  # Assuming a temporary upload folder
        self.app.test = True
        self.client = self.app.test_client()

    def test_no_audio_file(self):
        # Simulate request without audio file
        with self.app.test_request_context():
            request.files = {}
            response = upload_audio()
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'error': 'No audio file part'})

    def test_empty_filename(self):
        # Simulate request with empty filename
        test_file = MagicMock(filename='')
        with self.app.test_request_context():
            request.files = {'audio': test_file}
            response = upload_audio()
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'error': 'No selected file'})

    @patch.object(speech_to_text_api, 'transcribe_audio')
    @patch.object(text_classifier_api, 'classify_text')
    def test_successful_upload(self, mock_classify_text, mock_transcribe_audio):
        # Mock speech-to-text and text classification
        mock_transcribe_audio.return_value = "I want to pay for my CBT charges"
        mock_classify_text.return_value = ("__label__otherfees", 0.9)

        # Upload a dummy file (replace with actual file upload logic)
        with open('Recording00002.wav', 'rb') as f:
            data = f.read()
            # Simulate file upload (modify based on your implementation)
            test_file = MagicMock()
            test_file.filename = 'Recording00002.wav'
            test_file.stream = data
            with self.app.test_request_context():
                request.files = {'audio': test_file}
                response = upload_audio()

                self.assertEqual(response.status_code, 302)  # Redirect expected
                self.assertEqual(response.mimetype, 'text/html')  # Redirect response

                # Verify internal calls (optional)
                mock_transcribe_audio.assert_called_once()
                mock_classify_text.assert_called_once()

    # Add tests for specific error scenarios during speech-to-text or text classification
    # ...

if __name__ == '__main__':
    unittest.main()