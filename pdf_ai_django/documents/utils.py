"""
Utility functions for the documents app
"""
import os
import sys
from pathlib import Path
from django.conf import settings

# Add parent directory to path to import modules
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from pdf_loader import PDFLoader
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from qa_engine import QAEngine

# Global instances (singleton pattern)
_embedding_generator = None
_vector_store = None
_qa_engine = None


def get_embedding_generator():
    """Get or create embedding generator instance"""
    global _embedding_generator
    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator()
    return _embedding_generator


def get_vector_store():
    """Get or create vector store instance"""
    global _vector_store
    if _vector_store is None:
        persist_dir = str(settings.CHROMA_PERSIST_DIR)
        _vector_store = VectorStore(persist_directory=persist_dir)
    return _vector_store


def get_qa_engine():
    """Get or create QA engine instance"""
    global _qa_engine
    if _qa_engine is None:
        model = settings.OLLAMA_MODEL
        url = settings.OLLAMA_URL
        _qa_engine = QAEngine(model=model, ollama_url=url)
    return _qa_engine


def process_pdf(pdf_document):
    """
    Process a PDF document: extract text, create chunks, generate embeddings, store in vector DB

    Args:
        pdf_document: PDFDocument model instance

    Returns:
        tuple: (success: bool, message: str, chunks_count: int, pages_count: int)
    """
    try:
        # Get file path
        file_path = pdf_document.file.path

        # Load and process PDF
        loader = PDFLoader(file_path)
        chunks = loader.load_and_process(chunk_size=1000, overlap=200)

        if not chunks:
            return False, "No text could be extracted from PDF", 0, 0

        # Count pages (estimate from PyPDF2)
        import PyPDF2
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            pages_count = len(reader.pages)

        # Generate embeddings
        embedder = get_embedding_generator()
        chunks_with_embeddings = embedder.encode_chunks(chunks)

        # Store in vector database
        store = get_vector_store()
        store.add_documents(chunks_with_embeddings, pdf_document.get_filename())

        return True, "Success", len(chunks), pages_count

    except Exception as e:
        return False, str(e), 0, 0