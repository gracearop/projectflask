import os
import fasttext

# Get the path to the root directory (assuming this script is in the text_classifier_api folder)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Construct the full path to the model file
model_path = os.path.join(root_dir, "text_classifier_api", "model_intent.bin")

# Load the model
model = fasttext.load_model(model_path)

def classify_text(text):
    prediction = model.predict(text)
    label = prediction[0][0]
    probability = prediction[1][0]
    return label, probability

# Function to perform predictions
def predict_intent(txts):
    prediction = model.predict(txts)
    label = prediction[0][0]
    probability = prediction[1][0]
    return label, probability

# Example usage
if __name__ == "__main__":
    # Example text input
    txts = "I want to add another course to my registration."
    
    # Perform prediction
    label, probability = predict_intent(txts)
    
    # Display the results
    print(f"Predicted Label: {label}")
    print(f"Probability: {probability:.4f}")

# import fasttext

# # Load the pre-trained model
# model = fasttext.load_model("model_intent.bin")

# def classify_text(text):
#     # Perform classification
#     labels, probabilities = model.predict(text, k=1)  # k=1 for top label prediction
#     return labels[0], probabilities[0]

# if __name__ == "__main__":
#     # Example usage
#     text = "I want to clear my extra fee for portal charge"
#     label, probability = classify_text(text)
#     print(f"Text: {text}")
#     print(f"Predicted Label: {label}")
#     print(f"Probability: {probability}")
