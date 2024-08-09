import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset

# Load the data
data = pd.read_csv('intent_data.csv')

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data['text'], data['intent'], test_size=0.2, random_state=42)

# Convert text data to TF-IDF features
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train a Naive Bayes classifierfrom transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
from sklearn.model_selection import train_test_split

# Load data from CSV
data = pd.read_csv("data/intent_data.csv")
X = data["Text"].tolist()
y = data["Intent"].tolist()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess data
def preprocess_function(examples):
  return tokenizer(examples["Text"], padding="max_length", truncation=True)

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
train_encodings = tokenizer(X_train, padding=True, truncation=True, return_tensors="pt")
test_encodings = tokenizer(X_test, padding=True, truncation=True, return_tensors="pt")

# Create Datasets objects
train_dataset = load_dataset("text", data_files={"train": train_encodings})
test_dataset = load_dataset("text", data_files={"test": test_encodings})

# Define model (modify num_labels based on your intent classes)
num_labels = len(set(y))  # Automatically determine number of labels from data
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=num_labels)

# Training
from transformers import Trainer

trainer = Trainer(
    model=model,
    args=TrainingArguments(output_dir="./results", per_device_train_batch_size=8),
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

trainer.train()

# Evaluation
predictions = trainer.predict(test_dataset)
logits = predictions.predictions
predicted_labels = np.argmax(logits, axis=-1)

# Print Evaluation Metrics (you can implement your desired metrics here)
from sklearn.metrics import accuracy_score, classification_report

accuracy = accuracy_score(y_test, predicted_labels)
report = classification_report(y_test, predicted_labels)

print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:")
print(report)


classifier = MultinomialNB()
classifier.fit(X_train_tfidf, y_train)

# Predict the intents for the test set
y_pred = classifier.predict(X_test_tfidf)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
