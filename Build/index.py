# Import Libraries
import tkinter as tk
from tkinter import ttk
import numpy as np
import requests
import joblib
import emoji
import pandas as pd
import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gensim.models import Word2Vec
from sklearn.preprocessing import normalize
import gensim
import preprocess
import training

def load_resources():
    # Load model Machine Learning
    model = joblib.load('model/nb_model.joblib') # Load the model
    vectorizer = joblib.load('fe/tfidf_vectorizer.joblib') # Load Vectorizer
    word2vec_model = Word2Vec.load('model/word2vec_model.bin') # Load NLP model
    return model, vectorizer, word2vec_model

def plot_distribution(df, frame):
    # Calculate counts of each category
    category_counts = df['prediction'].value_counts()
    
    # Create a pie chart
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Prediksi Kategori DISC')
    
    # Embed the plot in tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def predict_result(model, vectorizer, input_data, word2vec_model):
    # Load vectorizer to transform data
    X_new = vectorizer.transform(input_data)

    # Calculate document embeddings using Word2Vec and TF-IDF
    document_embeddings = training.calculate_document_embeddings(input_data, word2vec_model, vectorizer)
            
    # Normalize document embeddings
    normalized_document_embeddings = normalize(document_embeddings, norm='l2')
            
    # Combine TF-IDF features and document embeddings
    X_combined = np.hstack((X_new.toarray(), normalized_document_embeddings))

    # Load model untuk memprediksi kategori DISC
    prediction = model.predict(X_combined)
    return prediction

def send_tweet_harvest_request(entry_var, label_var, frame, tree):
    username = entry_var.get()
    url = 'http://localhost:3000/tweet-harvest' # Node.js port
    data = {'username': username}

    # Update label
    label_var.set("Mengambil Tweet... Harap tunggu...")
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Request sent successfully")
        # Update label text
        label_var.set("Twitter harvest selesai!")

        # Prediction
        model, vectorizer, word2vec_model = load_resources()

        # Preprocess Tweet
        new_df = pd.read_csv(f"tweets-data/tweet_{username}.csv", delimiter=',', encoding='latin1')
        new_tweets = new_df['full_text'].tolist()
        new_tweets = [preprocess.preprocess_tweet(tweet) for tweet in new_tweets]
        new_df['text'] = new_tweets

        if new_tweets is not None:
            new_df['prediction'] = predict_result(model, vectorizer, new_tweets, word2vec_model)
            new_df.to_csv(f"new_df/new_tweet_{username}.csv", index=False)
            
            # Display
            print(new_df[['text', 'prediction']])

            # Display tweets and predictions in the table
            for index, row in new_df.iterrows():
                tweet_text = row['text']
                prediction = row['prediction']

                # Add a number for each row
                row_number = index + 1

                tree.insert("", "end", values=(row_number, tweet_text, prediction))
            
            # Plot prediction
            plot_distribution(new_df, frame)

    else:
        # Update label
        label_var.set("Error mengirim request.")
        print("Error sending request")

def go_button_clicked(entry_var, label_var, frame, tree):
    send_tweet_harvest_request(entry_var, label_var, frame, tree)

def main():
    # Create GUI
    root = tk.Tk()
    root.title("DISC by Jetrich Khowanto")
    
    # Settings to make the UI responsive
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set window size
    window_width = 600
    window_height = 500
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # Message Widget
    message_style = ("Helvetica", 16, "bold")
    message = tk.Message(root, text="Masukkan username akun Twitter", width=500, font=message_style)
    message.pack(pady=(50,10))
    entry_var = tk.StringVar()
    
    # Entry Widget
    entry_style = ("Helvetica", 12)
    entry = tk.Entry(root, textvariable=entry_var, font=entry_style)
    entry.pack(pady=10)
    
    # Button Widget
    button_style = ("Helvetica", 14, "bold")
    go_button = tk.Button(root, text="Mulai", command=lambda: go_button_clicked(entry_var, label_var, frame, tree), font=button_style)
    go_button.pack(pady=10)
    
    label_var = tk.StringVar()
    label_var.set("")
    status_label = tk.Label(root, textvariable=label_var, font=entry_style)
    status_label.pack(pady=10)

    # Table Widget
    table_frame = tk.Frame(root)
    table_frame.pack(pady=10)

    # Treeview Widget
    columns = ("No", "Tweet", "Prediksi")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
    tree.heading("No", text="No")
    tree.heading("Tweet", text="Tweet")
    tree.heading("Prediksi", text="Prediksi")
    tree.column("No", width=50)
    tree.column("Tweet", width=400)
    tree.column("Prediksi", width=85)
    tree.pack()

    # Canvas to show graph
    frame = tk.Frame(root)
    frame.pack(expand=True, fill=tk.BOTH)
    
    # Run the App
    root.mainloop()

main()
