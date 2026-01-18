import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import json

class VectorStore:
    def __init__(self, index_file="src/memory/faiss_index.bin", metadata_file="src/memory/metadata.json"):
        self.index_file = index_file
        self.metadata_file = metadata_file
        self.dim = 384  # Default for all-MiniLM-L6-v2
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.metadata = []

        if os.path.exists(index_file) and os.path.exists(metadata_file):
            self.index = faiss.read_index(index_file)
            with open(metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.save()

    def add(self, text, meta=None):
        embedding = self.model.encode([text])
        self.index.add(np.array(embedding).astype('float32'))
        self.metadata.append({"text": text, "meta": meta})
        self.save()

    def search(self, query, k=3):
        if self.index.ntotal == 0:
            return []
            
        embedding = self.model.encode([query])
        D, I = self.index.search(np.array(embedding).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(I[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    "text": self.metadata[idx]["text"],
                    "meta": self.metadata[idx]["meta"],
                    "distance": float(D[0][i])
                })
        return results

    def save(self):
        faiss.write_index(self.index, self.index_file)
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f)
