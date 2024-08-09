# Import libraries
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# Load the data
data = pd.read_csv('data/intent_data.csv')

# Check for missing column (optional)
print(data.head())  # Print the first few rows to verify column names

# Train-test split (assuming 'Text' and 'Intent' columns)
X_train, X_test, y_train, y_test = train_test_split(data['Text'], data['Intent'], test_size=0.2, random_state=42)

# ... rest of your code for TF-IDF, Naive Bayes, etc.




# # Import libraries for Naive Bayes
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report, accuracy_score
# import pandas as pd


# # Import libraries for BERT (if needed)
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# from datasets import load_dataset

# # Load the data
# data = pd.read_csv('data/intent_data.csv')

# # Naive Bayes Model
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(data['text'], data['intent'], test_size=0.2, random_state=42)

# # Convert text data to TF-IDF features
# vectorizer = TfidfVectorizer()
# X_train_tfidf = vectorizer.fit_transform(X_train)
# X_test_tfidf = vectorizer.transform(X_test)

# # Train a Naive Bayes classifier
# classifier = MultinomialNB()
# classifier.fit(X_train_tfidf, y_train)

# # Predict the intents for the test set
# y_pred = classifier.predict(X_test_tfidf)

# # Evaluate the Naive Bayes Model
# print("Naive Bayes Model:")
# print("Accuracy:", accuracy_score(y_test, y_pred))
# print(classification_report(y_test, y_pred))

# # BERT Model (Optional)
# # ... Implement BERT model code here ...

