from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np


class EmbeddingGenerator:
    """Generate embeddings for text using sentence transformers"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embedding model
        Args:
            model_name: HuggingFace model name. Options:
                - 'all-MiniLM-L6-v2' (fast, 384 dimensions) - RECOMMENDED
                - 'all-mpnet-base-v2' (better quality, 768 dimensions)
                - 'multi-qa-MiniLM-L6-cos-v1' (optimized for Q&A)
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.dimension}")

    def encode_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        Args:
            text: Input text string
        Returns:
            Numpy array of embeddings
        """
        return self.model.encode(text, convert_to_numpy=True)

    def encode_batch(self, texts: List[str], batch_size: int = 32,
                     show_progress: bool = True) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        Args:
            texts: List of text strings
            batch_size: Number of texts to process at once
            show_progress: Show progress bar
        Returns:
            Numpy array of shape (len(texts), embedding_dim)
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True
        )
        return embeddings

    def encode_chunks(self, chunks: List[dict]) -> List[dict]:
        """
        Add embeddings to chunk dictionaries
        Args:
            chunks: List of chunk dicts with 'text' field
        Returns:
            Same chunks with added 'embedding' field
        """
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.encode_batch(texts)

        for i, chunk in enumerate(chunks):
            chunk['embedding'] = embeddings[i]

        return chunks

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two embeddings
        Args:
            embedding1, embedding2: Embedding vectors
        Returns:
            Similarity score (0 to 1)
        """
        return np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

    def find_most_similar(self, query_embedding: np.ndarray,
                          chunk_embeddings: np.ndarray,
                          top_k: int = 5) -> List[tuple]:
        """
        Find most similar chunks to a query
        Args:
            query_embedding: Query embedding vector
            chunk_embeddings: Array of chunk embeddings
            top_k: Number of top results to return
        Returns:
            List of (index, similarity_score) tuples
        """
        similarities = np.dot(chunk_embeddings, query_embedding) / (
                np.linalg.norm(chunk_embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = [(int(idx), float(similarities[idx])) for idx in top_indices]
        return results


if __name__ == "__main__":
    # Test the embedding generator
    generator = EmbeddingGenerator()

    test_texts = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with many layers.",
        "Python is a popular programming language."
    ]

    embeddings = generator.encode_batch(test_texts)
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Embedding shape: {embeddings.shape}")

    # Test similarity
    sim = generator.similarity(embeddings[0], embeddings[1])
    print(f"Similarity between first two texts: {sim:.3f}")