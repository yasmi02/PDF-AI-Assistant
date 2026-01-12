import PyPDF2
import pdfplumber
from typing import List, Dict
import re


class PDFLoader:
    """Load and clean text from PDF files"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path

    def extract_text(self, method: str = "pypdf2") -> str:
        """
        Extract text from PDF using specified method
        Args:
            method: 'pypdf2' or 'pdfplumber'
        Returns:
            Extracted text as string
        """
        if method == "pypdf2":
            return self._extract_with_pypdf2()
        elif method == "pdfplumber":
            return self._extract_with_pdfplumber()
        else:
            raise ValueError(f"Unknown method: {method}")

    def _extract_with_pypdf2(self) -> str:
        """Extract text using PyPDF2"""
        text = ""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text

    def _extract_with_pdfplumber(self) -> str:
        """Extract text using pdfplumber (better for complex layouts)"""
        text = ""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:\;\(\)]', '', text)
        # Remove multiple periods
        text = re.sub(r'\.{2,}', '.', text)
        return text.strip()

    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, any]]:
        """
        Split text into overlapping chunks
        Args:
            text: Input text to chunk
            chunk_size: Target size of each chunk (in characters)
            overlap: Overlap between chunks
        Returns:
            List of dicts with chunk text and metadata
        """
        words = text.split()
        chunks = []

        # Calculate words per chunk based on average word length
        avg_word_length = sum(len(word) for word in words[:100]) / min(100, len(words))
        words_per_chunk = int(chunk_size / (avg_word_length + 1))
        words_overlap = int(overlap / (avg_word_length + 1))

        for i in range(0, len(words), words_per_chunk - words_overlap):
            chunk_words = words[i:i + words_per_chunk]
            chunk_text = ' '.join(chunk_words)

            chunks.append({
                'text': chunk_text,
                'chunk_id': len(chunks),
                'start_word': i,
                'end_word': i + len(chunk_words)
            })

            if i + words_per_chunk >= len(words):
                break

        return chunks

    def load_and_process(self, method: str = "pdfplumber",
                         chunk_size: int = 1000,
                         overlap: int = 200) -> List[Dict[str, any]]:
        """
        Complete pipeline: extract, clean, and chunk PDF
        Returns:
            List of processed text chunks with metadata
        """
        # Extract text
        raw_text = self.extract_text(method=method)

        # Clean text
        cleaned_text = self.clean_text(raw_text)

        # Chunk text
        chunks = self.chunk_text(cleaned_text, chunk_size=chunk_size, overlap=overlap)

        # Add source metadata
        for chunk in chunks:
            chunk['source'] = self.pdf_path

        return chunks