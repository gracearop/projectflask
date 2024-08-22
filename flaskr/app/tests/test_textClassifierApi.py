import unittest
import os
import fasttext
import sys

# Adding the root directory to the sys.path to allow importing the predict_intent function
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from text_classifier_api.text_classifier_api import predict_intent  # Import the function from the text_classifier_api.py file

# Define the root directory and model path correctly
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
model_path = os.path.join(root_dir, "text_classifier_api", "model_intent.bin")

class TestPredictIntent(unittest.TestCase):
    def setUp(self):
        # Load the model for the test
        self.model = fasttext.load_model(model_path)

        # Create a test dataset with expected labels
        self.test_data = {
            "text1": "I want to add another course to my registration.",
            "text2": "I want to pay for my matriculation fees?",
            "text3": "i want to get a hostel accommodation?"
        }
        self.expected_labels = ["__label__coursereg", "__label__otherfees", "__label__accommodation"]

    def test_predict_intent(self):
        for text, expected_label in zip(self.test_data.values(), self.expected_labels):
            predicted_label, probability = predict_intent(text)
            self.assertEqual(predicted_label, expected_label)
            # You can also add assertions for probability thresholds or other metrics

if __name__ == '__main__':
    unittest.main()
