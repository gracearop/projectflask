import fasttext
import re

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r"([.\!?,'/()])", r" \1 ", text)
    text = text.lower()
    return text

# Load and preprocess the formatted data
with open('formatted_data.txt', 'r') as file:
    lines = file.readlines()

# Preprocess each line
lines = [preprocess_text(line) for line in lines]

# Define the split sizes
train_size = 200
valid_size = len(lines) - train_size

# Split the data
train_data = lines[:train_size]
valid_data = lines[-valid_size:]

# Save the splits
with open('intent.train', 'w') as file:
    file.writelines(train_data)

with open('intent.valid', 'w') as file:
    file.writelines(valid_data)

# Train the model with advanced parameters
model = fasttext.train_supervised(
    input="intent.train",
    lr=1.0,
    epoch=25,
    wordNgrams=2,
    bucket=200000,
    dim=50,
    loss='hs'
)

# Save the model
model.save_model("model_intent.bin")

# Test the model on the validation set
result = model.test("intent.valid")
print(f"Number of samples: {result[0]}")
print(f"Precision at 1: {result[1]}")
print(f"Recall at 1: {result[2]}")

# Example prediction
prediction = model.predict("I want to clear my extra fee for portal charge")
print(f"Predicted Label: {prediction[0][0]}")
print(f"Probability: {prediction[1][0]}")


# import fasttext
# # Load the formatted data
# with open('formatted_data.txt', 'r') as file:
#     lines = file.readlines()

# # Define the split sizes
# train_size = 200
# valid_size = len(lines) - train_size

# # Split the data
# train_data = lines[:train_size]
# valid_data = lines[-valid_size:]

# # Save the splits
# with open('intent.train', 'w') as file:
#     file.writelines(train_data)

# with open('intent.valid', 'w') as file:
#     file.writelines(valid_data)

# # Train the model
# model = fasttext.train_supervised(input="intent.train")

# # Save the model
# model.save_model("model_intent.bin")

# # Test the model on the validation set
# result = model.test("intent.valid")
# print(f"Validation Results: {result}")

# # Example prediction
# print(model.predict("I want to make a fee payment."))
