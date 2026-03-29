from sentence_transformers import SentenceTransformer
import numpy as np
from vector_utils import cosine_sim

class VectorGraft:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        
    def embed_text(self, texts):
        return self.model.encode(texts)

    def compute_similarity(self, code_vec, doc_vecs):
        best_i = -1
        best_sim = -1.0
        # code_vec usually comes as (1, dim), doc_vecs as (N, dim)
        flat_code_vec = code_vec[0] if len(code_vec.shape) > 1 else code_vec
        for i, doc_vec in enumerate(doc_vecs):
            sim = cosine_sim(flat_code_vec, doc_vec)
            if sim > best_sim:
                best_sim = sim
                best_i = i
        # Returning list to match faiss unpacking expectations
        return [best_i], [best_sim]