import os
import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

class FeedbackRAG:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Ruta absoluta al archivo DB
        db_path = r"C:\Users\lizzi\Documents\Django\django\db.sqlite3"

        self.model = SentenceTransformer(model_name)
        self.index = None
        self.data = []
        self.load_data(db_path)

    def load_data(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT user_message, bot_response FROM api_feedbackgpt WHERE status = 'approved'")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return

        self.data = rows
        embeddings = self.model.encode([row[0] for row in rows], convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def search(self, query, top_k=1):
        if not self.index:
            return None

        query_embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(query_embedding, top_k)

        if I[0][0] == -1 or D[0][0] > 0.3:
            return None

        result_idx = I[0][0]
        return self.data[result_idx][1]
