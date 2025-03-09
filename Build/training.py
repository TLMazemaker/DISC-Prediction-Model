# Import libraries
from gensim.models import Word2Vec
from sklearn.preprocessing import normalize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from scipy.sparse import csr_matrix
import joblib
import os
import pandas as pd
import preprocess
import numpy as np

# Function to load data from CSV files in a folder
def load_data(folder_path):
    data = []
    labels = []

    for category in categories:
        category_folder = os.path.join(folder_path, category)
        for file_name in os.listdir(category_folder):
            if file_name.endswith(".csv"):
                file_path = os.path.join(category_folder, file_name)
                df = pd.read_csv(file_path, delimiter=';', encoding='latin1')
                data.extend(df['text'])  # Change 'Text' to the actual column name in your CSV
                labels.extend([category] * len(df))

    return data, labels

categories = ['Dominance', 'Influence', 'Steadiness', 'Compliance']

# Load data
folder_path = 'dataset/'
tweets, labels = load_data(folder_path)

# Tokenize and preprocess tweets
tweets = [preprocess.preprocess_tweet(tweet) for tweet in tweets]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(tweets, labels, test_size=0.2, random_state=42)

# Train Word2Vec model
word2vec_model = Word2Vec(X_train, min_count=1)  # Adjust parameters as needed

# Extract features using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_tfidf = tfidf_vectorizer.fit_transform(X_train)

# Get feature names (vocabulary)
feature_names = tfidf_vectorizer.get_feature_names_out()

def calculate_document_embeddings(tokenized_tweets, word2vec_model, tfidf_vectorizer):
    document_embeddings = []
    for tokenized_tweet in tokenized_tweets:
        word_embeddings = []
        for token in tokenized_tweet:
            if token in word2vec_model.wv:
                word_embeddings.append(word2vec_model.wv[token])
        if word_embeddings:
            # Calculate TF-IDF scores for the tokens in the current tweet
            tfidf_scores = tfidf_vectorizer.transform([' '.join(tokenized_tweet)]).toarray()[0]
            # Ensure tfidf_scores length matches word_embeddings
            tfidf_scores = tfidf_scores[:len(word_embeddings)]
            # Check if all TF-IDF scores are zero
            if np.sum(tfidf_scores) == 0:
                document_embeddings.append(np.zeros(word2vec_model.vector_size))
            else:
                # Calculate the weighted average of word embeddings using TF-IDF scores
                weighted_avg = np.average(word_embeddings, axis=0, weights=tfidf_scores)
                document_embeddings.append(weighted_avg)
        else:
            # If no tokens have embeddings, append a zero vector
            document_embeddings.append(np.zeros(word2vec_model.vector_size))
    return np.array(document_embeddings)

# Calculate document embeddings
document_embeddings = calculate_document_embeddings(X_train, word2vec_model, tfidf_vectorizer)

# Normalize document embeddings
normalized_document_embeddings = normalize(document_embeddings, norm='l2')

# Combine TF-IDF and Word2Vec embeddings
X_combined = np.hstack((X_tfidf.toarray(), normalized_document_embeddings))

# Ensure the number of samples in X_combined matches y_train
assert X_combined.shape[0] == len(y_train), "Number of samples in X_combined and y_train are not consistent."

# Define the K-fold cross-validation object
k_folds = 10  # You can adjust this value as needed
cv = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)

# Initialize Multinomial Naive Bayes model
nb_model = MultinomialNB()

# Combine TF-IDF and Word2Vec embeddings
X_combined = np.hstack((X_tfidf.toarray(), normalized_document_embeddings))  # Assuming normalized_document_embeddings is available

# Perform K-fold cross-validation
train_accuracies = cross_val_score(nb_model, X_combined, y_train, cv=cv, scoring='accuracy')

# Print training accuracies for each fold
for fold, accuracy in enumerate(train_accuracies, 1):
    print(f"Training Accuracy - Fold {fold}: {accuracy * 100:.2f}%")

# Calculate and print the mean training accuracy
mean_train_accuracy = train_accuracies.mean()
print(f"\nMean Training Accuracy: {mean_train_accuracy * 100:.2f}%")

# Train the model on the entire training set
nb_model.fit(X_combined, y_train)

# Predict on the testing set
X_test_tfidf = tfidf_vectorizer.transform(X_test)
X_test_combined = np.hstack((X_test_tfidf.toarray(), calculate_document_embeddings(X_test, word2vec_model, tfidf_vectorizer)))
y_pred_test = nb_model.predict(X_test_combined)

# Compute accuracy on the testing set
accuracy_test = accuracy_score(y_test, y_pred_test)
print(f"\nTest Accuracy: {accuracy_test * 100:.2f}%")

# Save the TF-IDF vectorizer
joblib.dump(tfidf_vectorizer, 'fe/tfidf_vectorizer.joblib')

# Save Word2Vec model
word2vec_model.save("model/word2vec_model.bin")

# Save the trained Naive Bayes model
joblib.dump(nb_model, 'model/nb_model.joblib')
