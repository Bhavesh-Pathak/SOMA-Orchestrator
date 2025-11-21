import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer
from groq import Groq
import asyncio

class KnowledgeAgent:
    def __init__(self, data_dir='data', index_path='data/faiss_index'):
        self.data_dir = data_dir
        self.index_path = index_path
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        api_key = os.getenv("GROQ_API_KEY")
        self.use_grok = api_key is not None
        if self.use_grok:
            self.client = Groq(api_key=api_key)
        if not os.path.exists(self.index_path + '.index'):
            self._build_index()
        else:
            self.index = faiss.read_index(self.index_path + '.index')
            with open(self.index_path + '.chunks', 'rb') as f:
                self.chunks = pickle.load(f)

    def _build_index(self):
        texts = []
        for file in os.listdir(self.data_dir):
            if file.endswith('.txt'):
                with open(os.path.join(self.data_dir, file), 'r', encoding='utf-8') as f:
                    texts.append(f.read())
        # Simple chunking: 500 chars
        chunks = []
        for text in texts:
            for i in range(0, len(text), 500):
                chunk = text[i:i+500].strip()
                if chunk:
                    chunks.append(chunk)
        if not chunks:
            chunks = ["No knowledge data available."]
        embeddings = self.embedder.encode(chunks)
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings.astype('float32'))
        faiss.write_index(self.index, self.index_path + '.index')
        with open(self.index_path + '.chunks', 'wb') as f:
            pickle.dump(chunks, f)
        self.chunks = chunks

    def _get_answer_from_grok(self, query: str, context: str) -> str:
        prompt = f"""Based on the following context, answer the question. If the context doesn't contain relevant information, provide a general answer.

Context:
{context}

Question: {query}

Answer:"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating answer: {e}"

    def run(self, query: str) -> str:
        query_emb = self.embedder.encode([query])[0]
        D, I = self.index.search(query_emb.reshape(1, -1), 3)
        relevant_chunks = [self.chunks[i] for i in I[0] if i < len(self.chunks)]
        context = ' '.join(relevant_chunks)
        if not context.strip():
            context = "No relevant knowledge found in the database."
        if self.use_grok:
            # Generate intelligent answer using Grok
            answer = self._get_answer_from_grok(query, context)
        else:
            # Fallback to simple retrieval
            answer = f"Based on knowledge base: {context}"
        return answer