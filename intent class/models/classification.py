import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Sample data (replace with your actual data)
# data = pd.read_csv("intent_data.csv")
data = pd.read_csv("data/intent_data.csv")


# Assuming your CSV has headers named "Text" and "Intent"
X = data['Text']
y = data['Intent']

# Create pandas DataFrame
df = pd.DataFrame(data, columns=["Text", "Intent"])

# Clean text (optional - you can explore more cleaning techniques)
df['Text'] = df['Text'].str.lower()  # Convert to lowercase

# Separate features (text) and labels (intent)
X = df['Text']
y = df['Intent']

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer(max_features=2000)  # Adjust max_features as needed

# Transform text data into numerical features
X_features = vectorizer.fit_transform(X)

# Split data into training and testing sets (e.g., 80%/20% split)
X_train, X_test, y_train, y_test = train_test_split(X_features, y, test_size=0.2, random_state=42)

# Create a Multinomial Naive Bayes classifier
model = MultinomialNB()

# Train the model on the training data
model.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = model.predict(X_test)

# Evaluate model performance (classification report)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Example new sentence
new_text = "Check results"

# Transform new text into features
new_features = vectorizer.transform([new_text])

# Predict intent for the new sentence
predicted_intent = model.predict(new_features)[0]

print("Predicted Intent for new sentence:", predicted_intent)
