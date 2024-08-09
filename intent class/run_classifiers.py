import subprocess

print("Running Naive Bayes Classifier...")
subprocess.run(["python", "models/naive_bayes_classifier.py"])

print("\nRunning BERT Classifier...")
subprocess.run(["python", "models/bert_classifier.py"])
