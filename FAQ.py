import nltk
import tkinter as tk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

# Download NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Initialize stemmer and tokenizer
stemmer = PorterStemmer()
tokenizer = RegexpTokenizer(r'\w+')

# Preprocessing function
def preprocess(text):
    text = text.lower()
    words = tokenizer.tokenize(text)
    stop_words = set(stopwords.words('english'))
    return ' '.join([stemmer.stem(w) for w in words if w not in stop_words])

# Sample FAQs
faqs = {
    "What is AI?": "AI stands for Artificial Intelligence. It is the simulation of human intelligence in machines.",
    "What is machine learning?": "Machine learning is a subset of AI that allows systems to learn from data and improve over time.",
    "What is deep learning?": "Deep learning is a part of machine learning using neural networks with many layers.",
    "What is NLP?": "NLP stands for Natural Language Processing, which enables machines to understand and respond in human language.",
    "What are neural networks?": "Neural networks are algorithms inspired by the human brain used to recognize patterns in data.",
    "How does this chatbot work?": "This chatbot uses TF-IDF and cosine similarity to match your question with known FAQs.",
    "Can you tell me about Python?": "Python is a popular programming language known for its readability and versatility.",
    "What is your name?": "I am an FAQ chatbot designed to answer your questions."}

# Preprocess FAQs
questions = list(faqs.keys())
answers = list(faqs.values())
preprocessed_questions = [preprocess(q) for q in questions]

# Vectorize using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(preprocessed_questions)

# Match user input to FAQs
def get_best_answer(user_input):
    user_input_processed = preprocess(user_input)
    if not user_input_processed.strip():
        return "Please ask a valid question."
    user_vec = vectorizer.transform([user_input_processed])
    similarities = cosine_similarity(user_vec, X)
    best_match = np.argmax(similarities)
    if similarities[0, best_match] < 0.45:  # Adjust threshold as needed
        return "Sorry, I couldn't understand your question."
    return answers[best_match]

# GUI using tkinter
def ask_bot():
    user_question = entry.get()
    response = get_best_answer(user_question)
    chat_log.insert(tk.END, "You: " + user_question + "\n")
    chat_log.insert(tk.END, "Bot: " + response + "\n\n")
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("FAQ Chatbot")

chat_log = tk.Text(root, height=20, width=60)
chat_log.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_log.yview)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

send_button = tk.Button(root, text="Ask", command=ask_bot)
send_button.pack()

entry.bind("<Return>", lambda event: ask_bot())

root.mainloop()
