from sentence_transformers import SentenceTransformer
import numpy as np
import json
from pathlib import Path
import os

class ItemEmbeddings:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.embeddings_file = Path("data/item_embeddings.npy")
        self.items_file = Path("data/DB.json")
        self.items = None
        self.embeddings = None
        
    def load_items(self):
        with open(self.items_file, 'r', encoding='utf-8') as f:
            all_items = json.load(f)
            # Filter out items with "(altered)" in their names
            self.items = [item for item in all_items if "(altered)" not in item['name']]
            
    def generate_embeddings(self):
        if not self.items:
            self.load_items()
            
        texts = []
        for item in self.items:
            # Combine name and description for better context
            text = f"{item['name']} {item['description']}"
            texts.append(text)
            
        self.embeddings = self.model.encode(texts)
        np.save(self.embeddings_file, self.embeddings)
        
    def load_embeddings(self):
        if self.embeddings_file.exists():
            self.embeddings = np.load(self.embeddings_file)
        else:
            self.generate_embeddings()
            
    def get_similar_items(self, item_name, top_k=5):
        if not self.items or not self.embeddings:
            self.load_items()
            self.load_embeddings()
            
        # Find the index of the item
        item_index = next((i for i, item in enumerate(self.items) if item['name'] == item_name), None)
        if item_index is None:
            return []
            
        # Get the embedding for the query item
        query_embedding = self.embeddings[item_index]
        
        # Calculate cosine similarity
        similarities = np.dot(self.embeddings, query_embedding) / (
            np.linalg.norm(self.embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top k similar items (excluding the query item itself)
        top_indices = np.argsort(similarities)[-top_k-1:-1][::-1]
        
        return [self.items[i] for i in top_indices]

# Test code that runs when the file is executed directly
if __name__ == "__main__":
    print("Testing ItemEmbeddings...")
    embeddings = ItemEmbeddings()
    
    # Test with Alberich's Robe
    test_item = "Alberich's Robe"
    print(f"\nFinding similar items to: {test_item}")
    print("----------------------------------------")
    
    similar_items = embeddings.get_similar_items(test_item)
    for item in similar_items:
        print(f"Name: {item['name']}")
        print(f"Description: {item['description']}")
        print("---") 