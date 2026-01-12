import chromadb
from chromadb.config import Settings
from typing import List, Dict
import os
from datetime import datetime


class VectorStore:
    """Manage vector database for document chunks"""

    def __init__(self, collection_name: str = "pdf_documents",
                 persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB vector store
        Args:
            collection_name: Name of the collection
            persist_directory: Where to save the database
        """
        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Create directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )

        print(f"Vector store initialized: {collection_name}")
        print(f"Current documents: {self.collection.count()}")

    def add_documents(self, chunks: List[Dict], pdf_name: str) -> None:
        """
        Add document chunks to the vector store
        Args:
            chunks: List of chunk dicts with 'text' and 'embedding' fields
            pdf_name: Name of the source PDF
        """
        if not chunks:
            print("No chunks to add")
            return

        # Prepare data for ChromaDB
        ids = []
        embeddings = []
        documents = []
        metadatas = []

        timestamp = datetime.now().isoformat()

        for chunk in chunks:
            # Create unique ID
            chunk_id = f"{pdf_name}_{chunk['chunk_id']}"
            ids.append(chunk_id)

            # Extract embedding
            embeddings.append(chunk['embedding'].tolist())

            # Store text
            documents.append(chunk['text'])

            # Store metadata
            metadata = {
                'source': pdf_name,
                'chunk_id': chunk['chunk_id'],
                'uploaded_at': timestamp
            }
            metadatas.append(metadata)

        # Add to ChromaDB
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )

        print(f"Added {len(chunks)} chunks from {pdf_name}")

    def search(self, query_embedding: List[float], top_k: int = 5,
               filter_source: str = None) -> Dict:
        """
        Search for similar documents
        Args:
            query_embedding: Query vector
            top_k: Number of results to return
            filter_source: Optional filter by source PDF name
        Returns:
            Dict with ids, documents, distances, and metadatas
        """
        where_filter = None
        if filter_source:
            where_filter = {"source": filter_source}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter
        )

        return results

    def delete_by_source(self, pdf_name: str) -> None:
        """
        Delete all chunks from a specific PDF
        Args:
            pdf_name: Name of the PDF to remove
        """
        self.collection.delete(
            where={"source": pdf_name}
        )
        print(f"Deleted all chunks from {pdf_name}")

    def get_all_sources(self) -> List[str]:
        """Get list of all PDF sources in the database"""
        results = self.collection.get()
        if not results['metadatas']:
            return []

        sources = set(meta['source'] for meta in results['metadatas'])
        return list(sources)

    def clear_collection(self) -> None:
        """Delete all documents from the collection"""
        self.client.delete_collection(self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Cleared collection: {self.collection_name}")

    def get_stats(self) -> Dict:
        """Get statistics about the vector store"""
        total_docs = self.collection.count()
        sources = self.get_all_sources()

        return {
            'total_chunks': total_docs,
            'total_pdfs': len(sources),
            'sources': sources
        }


if __name__ == "__main__":
    # Test the vector store
    import numpy as np

    store = VectorStore()

    # Test data
    test_chunks = [
        {
            'text': 'This is chunk 1',
            'embedding': np.random.rand(384),
            'chunk_id': 0
        },
        {
            'text': 'This is chunk 2',
            'embedding': np.random.rand(384),
            'chunk_id': 1
        }
    ]

    store.add_documents(test_chunks, 'test.pdf')

    # Test search
    query_emb = np.random.rand(384).tolist()
    results = store.search(query_emb, top_k=2)
    print(f"Search results: {results}")

    # Get stats
    stats = store.get_stats()
    print(f"Stats: {stats}")