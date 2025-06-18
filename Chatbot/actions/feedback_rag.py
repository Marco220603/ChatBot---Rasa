import faiss
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

class FeedbackRAG:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.data = []

    def load_data(self, db_path):
        # Conectamos a la base de datos SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Recuperamos los mensajes y respuestas aprobados
        cursor.execute("SELECT user_message, bot_response FROM api_feedbackgpt")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return

        self.data = rows
        embeddings = self.model.encode([row[0] for row in rows], convert_to_numpy=True)  # Codificamos los mensajes
        dim = embeddings.shape[1]  # Dimensión del espacio de embeddings
        self.index = faiss.IndexFlatL2(dim)  # Creamos el índice FAISS
        self.index.add(embeddings)  # Añadimos los embeddings al índice

    def search(self, query, top_k=1):
        # Si no hay índice, retornamos None
        if not self.index:
            return None

        query_embedding = self.model.encode([query], convert_to_numpy=True)  # Codificamos la consulta
        D, I = self.index.search(query_embedding, top_k)  # Realizamos la búsqueda en FAISS

        # Si la distancia es alta o el resultado es inválido, retornamos None
        if I[0][0] == -1 or D[0][0] > 0.3:
            return None

        result_idx = I[0][0]
        return self.data[result_idx][1]  # Devolvemos la respuesta asociada