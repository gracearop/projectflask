# Intent Classifier

This project contains scripts to train and evaluate intent classifiers using Naive Bayes and BERT models.

## Setup

1. Create a virtual environment and activate it:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

2. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

3. Place your training data in `data/intent_data.csv`.

## Running the Classifiers

To train and evaluate the Naive Bayes classifier:
```sh
python models/naive_bayes_classifier.py
