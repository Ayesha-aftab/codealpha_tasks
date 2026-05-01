import nltk
import customtkinter as ctk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Download NLTK resources
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# ==================== 50+ DETAILED FAQ DATA ====================
faq_data = {
    "What is Artificial Intelligence (AI)?": "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems. It includes learning, reasoning, problem-solving, perception, and language understanding.",
    
    "What is Machine Learning (ML)?": "Machine Learning is a subset of AI that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can analyze data and make predictions.",
    
    "What is the difference between AI and Machine Learning?": "AI is the broad field of creating intelligent machines. Machine Learning is a specific technique within AI that allows systems to learn from data and improve automatically.",
    
    "What is Deep Learning?": "Deep Learning is a subset of Machine Learning that uses artificial neural networks with multiple layers (deep networks) to learn complex patterns from large amounts of data.",
    
    "What are the main types of Machine Learning?": "The three main types are: 1) Supervised Learning, 2) Unsupervised Learning, and 3) Reinforcement Learning.",
    
    "What is Supervised Learning?": "Supervised Learning trains models on labeled data, where both input and correct output are provided. It is used for classification and regression tasks.",
    
    "What is Unsupervised Learning?": "Unsupervised Learning works with unlabeled data to discover hidden patterns, groupings, or structures. Common use cases include clustering and association.",
    
    "What is Reinforcement Learning?": "Reinforcement Learning is a type of ML where an agent learns to make decisions by interacting with an environment and receiving rewards or penalties.",
    
    "What is overfitting?": "Overfitting happens when a model learns the training data too well, including noise and outliers, and fails to generalize to new, unseen data.",
    
    "How can we prevent overfitting?": "Overfitting can be prevented using techniques like cross-validation, regularization (L1/L2), dropout, early stopping, and increasing the size of training data.",
    
    "What is underfitting?": "Underfitting occurs when a model is too simple to capture the underlying patterns in the data, resulting in poor performance on both training and test data.",
    
    "What is Python used for in AI?": "Python is the most popular language for AI and ML because of its simplicity and rich ecosystem of libraries like TensorFlow, PyTorch, Scikit-learn, and Pandas.",
    
    "Which libraries are important for Machine Learning?": "Key libraries include Scikit-learn, TensorFlow, PyTorch, Keras, Pandas, NumPy, Matplotlib, and Seaborn.",
    
    "What is a Neural Network?": "A Neural Network is a computational model inspired by the human brain, consisting of interconnected nodes (neurons) organized in layers.",
    
    "What is a Convolutional Neural Network (CNN)?": "CNNs are deep neural networks primarily used for image and video analysis because they can automatically detect spatial features.",
    
    "What is Natural Language Processing (NLP)?": "NLP is a branch of AI that helps machines understand, interpret, and generate human language in a useful way.",
    
    "What are real-world applications of AI?": "AI is used in virtual assistants (Siri, Alexa), recommendation systems (Netflix, Amazon), self-driving cars, medical diagnosis, fraud detection, and chatbots.",
    
    "What is Generative AI?": "Generative AI refers to systems that can create new content such as text, images, music, or code. Popular examples are ChatGPT and DALL·E.",
    
    "What is RAG in AI?": "RAG stands for Retrieval-Augmented Generation. It improves the accuracy of large language models by retrieving relevant information before generating a response.",
    
    "How can a beginner start learning AI?": "Start with Python programming, then learn Mathematics (Linear Algebra, Statistics, Calculus), followed by Machine Learning basics and hands-on projects.",
    
    "Do I need a degree for AI jobs?": "No. Many professionals succeed in AI through self-learning, online courses (Coursera, Udacity), bootcamps, and building strong project portfolios.",
    
    "What skills are needed for an AI internship?": "Strong Python skills, understanding of basic ML concepts, problem-solving ability, familiarity with Git, and eagerness to learn.",
    
    "What is Transfer Learning?": "Transfer Learning is a technique where a pre-trained model is reused for a new but related task, saving time and computational resources.",
    
    "What is bias in AI?": "Bias in AI occurs when a model produces unfair or prejudiced results due to biased training data or flawed algorithm design.",
    
    "How do we evaluate Machine Learning models?": "Common metrics are Accuracy, Precision, Recall, F1-Score for classification, and Mean Squared Error (MSE) for regression tasks.",
    
    "What is the difference between ML and DL?": "Machine Learning uses traditional algorithms, while Deep Learning uses multi-layered neural networks to automatically learn features from raw data.",
    
    "What is an LLM?": "LLM stands for Large Language Model. These are very large neural networks trained on massive text datasets, like GPT models.",
    
    "Why is data important in AI?": "Data is the fuel of AI. The quality, quantity, and diversity of data directly impact how well an AI model performs.",
    
    "What is computer vision?": "Computer Vision is a field of AI that enables machines to interpret and understand visual information from the world, such as images and videos.",
    
    "What is the future of AI?": "The future of AI includes more advanced generative models, better human-AI collaboration, ethical AI development, and integration into every industry.",
    
    "What is ethics in AI?": "AI ethics involves ensuring fairness, transparency, accountability, and avoiding harm when developing and deploying AI systems.",
}

# Prepare questions list
questions = list(faq_data.keys())
lemmer = nltk.stem.WordNetLemmatizer()

def LemNormalize(text):
    tokens = nltk.word_tokenize(text.lower().translate(str.maketrans('', '', string.punctuation)))
    return [lemmer.lemmatize(token) for token in tokens]

def get_bot_response(user_input):
    if not user_input.strip():
        return "Please ask a question."
    
    questions.append(user_input)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(questions)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    questions.pop()
    
    if req_tfidf == 0:
        return "I'm sorry, I don't have an answer for that yet. Feel free to ask anything related to Artificial Intelligence or Machine Learning!"
    return faq_data[questions[idx]]

# ====================== UI ======================
class AIChatbot(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AI & ML Assistant - CodeAlpha Internship")
        self.geometry("1100x720")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================== Wider Blue Sidebar ====================
        self.sidebar = ctk.CTkFrame(self, width=600, corner_radius=0, fg_color="#1e40af")  # Increased width
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.logo = ctk.CTkLabel(self.sidebar, text="🤖", font=("Segoe UI", 65))
        self.logo.pack(pady=(60, 15))

        self.title_label = ctk.CTkLabel(self.sidebar, text="AI & ML Assistant", 
                                      font=("Segoe UI", 26, "bold"), text_color="white")
        self.title_label.pack(pady=8)

        self.subtitle = ctk.CTkLabel(self.sidebar, text="Task 2: FAQ Chatbot\nCodeAlpha AI Internship",
                                   font=("Segoe UI", 14), text_color="#bfdbfe", wraplength=280, justify="center")
        self.subtitle.pack(pady=10)

        # ==================== Main Chat Area ====================
        self.chat_frame = ctk.CTkFrame(self, fg_color="#f8fafc")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=12, pady=12)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)

        self.text_area = ctk.CTkTextbox(self.chat_frame, font=("Segoe UI", 14.5), corner_radius=15, 
                                      fg_color="white", text_color="#1e2937")
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=15, pady=(15, 10))

        self.text_area.insert("0.0", "👋 Welcome to the AI & Machine Learning Assistant! \n\n"
                                     "You can ask me anything about Artificial Intelligence, Machine Learning, "
                                     "Deep Learning, or career tips in AI.\n\n"
                                     "Example: What is overfitting?\n\n" + "─"*80 + "\n\n")
        self.text_area.configure(state="disabled")

        # Bottom Input Area
        self.bottom_frame = ctk.CTkFrame(self.chat_frame, fg_color="transparent")
        self.bottom_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=10)

        self.entry = ctk.CTkEntry(self.bottom_frame, placeholder_text="Ask a question about AI or ML...",
                                 height=52, font=("Segoe UI", 14), corner_radius=25)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.clear_btn = ctk.CTkButton(self.bottom_frame, text="Clear History", width=130, height=52,
                                     corner_radius=25, font=("Segoe UI", 13), fg_color="#64748b",
                                     command=self.clear_history)
        self.clear_btn.pack(side="right", padx=(8, 0))

        self.send_btn = ctk.CTkButton(self.bottom_frame, text="Send", width=120, height=52,
                                    corner_radius=25, font=("Segoe UI", 14, "bold"),
                                    command=self.send_message)
        self.send_btn.pack(side="right")

        # Footer
        self.footer = ctk.CTkLabel(self, text="Created by Ayesha Aftab 💙/code alpha",
                                 font=("Segoe UI", 15), text_color="black", height=40)
        self.footer.grid(row=1, column=0, columnspan=2, sticky="ew", pady=8)

    def send_message(self):
        user_input = self.entry.get().strip()
        if user_input:
            self.display_message("You", user_input, "#1e40af")
            response = get_bot_response(user_input)
            self.display_message("Assistant", response, "#334155")
            self.entry.delete(0, 'end')

    def display_message(self, sender, message, color):
        self.text_area.configure(state="normal")
        self.text_area.insert("end", f"{sender}: ", (color,))
        self.text_area.insert("end", f"{message}\n\n")
        self.text_area.configure(state="disabled")
        self.text_area.see("end")

    def clear_history(self):
        self.text_area.configure(state="normal")
        self.text_area.delete("1.0", "end")
        self.text_area.insert("0.0", "👋 Chat history cleared!\n\nWelcome back! Ask me anything about AI & Machine Learning.\n\n" + "─"*80 + "\n\n")
        self.text_area.configure(state="disabled")

if __name__ == "__main__":
    app = AIChatbot()
    app.mainloop()