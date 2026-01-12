"""
QA Engine using Ollama (FREE local LLM)
No API key needed, runs completely on your computer
"""

import requests
import json
from typing import List, Dict
from embeddings import EmbeddingGenerator
from vector_store import VectorStore


class QAEngine:
    """Question Answering engine using Ollama"""

    def __init__(self, model: str = "llama3.2", ollama_url: str = "http://localhost:11434"):
        """
        Initialize QA engine with Ollama
        Args:
            model: Ollama model to use (llama3.2, mistral, phi, etc.)
            ollama_url: Ollama API endpoint
        """
        self.model = model
        self.ollama_url = ollama_url

        # Initialize components
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore()

        # Test Ollama connection
        self._test_ollama_connection()

        print(f"QA Engine initialized with Ollama model: {model}")

    def _test_ollama_connection(self):
        """Test if Ollama is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                available_models = [m['name'] for m in models]
                print(f"✅ Ollama connected! Available models: {available_models}")

                if self.model not in available_models and f"{self.model}:latest" not in available_models:
                    print(f"⚠️  Model '{self.model}' not found. Downloading...")
                    print(f"Run: ollama pull {self.model}")
            else:
                print("⚠️  Ollama is not responding")
        except requests.exceptions.ConnectionError:
            print("❌ Ollama is not running!")
            print("Please install and start Ollama:")
            print("1. Download from: https://ollama.ai")
            print(f"2. Run: ollama pull {self.model}")
            print("3. Ollama will start automatically")
        except Exception as e:
            print(f"⚠️  Error connecting to Ollama: {e}")

    def answer_question(self, question: str, top_k: int = 5,
                        pdf_source: str = None) -> Dict:
        """
        Answer a question using RAG with Ollama
        Args:
            question: User's question
            top_k: Number of relevant chunks to retrieve
            pdf_source: Optional - search only in specific PDF
        Returns:
            Dict with answer and metadata
        """
        # Step 1: Generate embedding for the question
        question_embedding = self.embedding_generator.encode_text(question)

        # Step 2: Search for relevant chunks
        search_results = self.vector_store.search(
            query_embedding=question_embedding.tolist(),
            top_k=top_k,
            filter_source=pdf_source
        )

        if not search_results['documents'][0]:
            return {
                'answer': "I couldn't find any relevant information in the uploaded documents.",
                'sources': [],
                'context_used': []
            }

        # Step 3: Prepare context from retrieved chunks
        retrieved_chunks = search_results['documents'][0]
        distances = search_results['distances'][0]
        metadatas = search_results['metadatas'][0]

        context = "\n\n".join([
            f"[Chunk {i + 1}]:\n{chunk}"
            for i, chunk in enumerate(retrieved_chunks)
        ])

        # Step 4: Create prompt
        prompt = self._create_prompt(question, context)

        # Step 5: Get answer from Ollama
        try:
            answer = self._query_ollama(prompt)
        except Exception as e:
            return {
                'answer': f"Error getting response from Ollama: {str(e)}. Make sure Ollama is running and the model is downloaded.",
                'sources': [],
                'context_used': []
            }

        # Step 6: Prepare response with metadata
        return {
            'answer': answer,
            'sources': [meta['source'] for meta in metadatas],
            'context_used': retrieved_chunks,
            'relevance_scores': [1 - d for d in distances]
        }

    def _query_ollama(self, prompt: str, stream: bool = False) -> str:
        """
        Query Ollama API
        Args:
            prompt: The prompt to send
            stream: Whether to stream the response
        Returns:
            Generated text
        """
        url = f"{self.ollama_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
            }
        }

        try:
            response = requests.post(url, json=payload, timeout=120)

            if response.status_code == 200:
                result = response.json()
                return result.get('response', '')
            else:
                raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            raise Exception("Ollama request timed out. The model might be downloading or processing is slow.")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to Ollama. Make sure it's running at " + self.ollama_url)

    def _create_prompt(self, question: str, context: str) -> str:
        """Create prompt for Ollama with question and context"""
        prompt = f"""You are a helpful AI assistant that answers questions based on provided document context.

Context from the document:
{context}

Question: {question}

Instructions:
- Answer the question based ONLY on the information provided in the context above
- If the context doesn't contain enough information to answer the question, say so
- Be concise but thorough
- Quote relevant parts of the context when appropriate
- If multiple chunks provide relevant information, synthesize them into a coherent answer

Answer:"""
        return prompt

    def summarize_document(self, pdf_source: str = None, max_length: int = 500) -> str:
        """
        Generate a summary of the document(s)
        Args:
            pdf_source: Optional - summarize specific PDF only
            max_length: Target length of summary
        Returns:
            Summary text
        """
        # Get sample of chunks to summarize
        all_chunks = self.vector_store.collection.get(
            where={"source": pdf_source} if pdf_source else None,
            limit=10
        )

        if not all_chunks['documents']:
            return "No documents found to summarize."

        # Combine chunks
        content = "\n\n".join(all_chunks['documents'][:5])

        # Create summary prompt
        prompt = f"""Please provide a comprehensive summary of the following document excerpt. 
The summary should be approximately {max_length} words and capture the main points and key information.

Document excerpt:
{content}

Summary:"""

        try:
            summary = self._query_ollama(prompt)
            return summary
        except Exception as e:
            return f"Error generating summary: {str(e)}"

    def get_available_documents(self) -> List[str]:
        """Get list of all available PDF documents"""
        return self.vector_store.get_all_sources()


if __name__ == "__main__":
    # Test the QA engine
    engine = QAEngine()

    # Test question
    result = engine.answer_question("What is machine learning?")
    print(f"Answer: {result['answer']}")
    print(f"Sources: {result['sources']}")