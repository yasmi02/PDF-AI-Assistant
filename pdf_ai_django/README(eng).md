# PDF AI Assistant

PDF AI Assistant is an AI-powered website that generates a summary after you upload a PDF and allows you to ask questions about the uploaded PDF/document.

# Things to Know

* Built using Ollama
* Site design was updated with the help of ClaudeAI

# Requirements

* Python 3.11 or 3.12 (other versions may cause issues)
* Ollama
* 8GB+ RAM
* 5GB+ free disk space

# How to Run?

**First:** Install everything listed in the `requirements.txt` file
(`pip install -r requirements.txt`)

**First bash:**

```
python manage.py makemigrations documents
```

**Second bash:**

```
python manage.py migrate
```

**Last bash:**

```
python manage.py runserver
```

**Extra:**

```
python manage.py createsuperuser
```

# Features

* Upload PDFs (up to 100MB)
* Automatic title generation based on file name
* Page & chunk tracking
* Easy document management

# AI-Powered Features

* **Automatic Summary Generation:** If you upload a document without asking a question during upload, the system automatically starts by generating a summary of the PDF.

* **Question & Answer Feature:** When you ask a question, you receive answers based strictly on the information contained in the uploaded PDF.

# Chat Interface

* A chatbot conversation panel inspired by the Pop-AI website
* Real-time chat bubbles: just like messaging
* Question history tracking: you can view your previous questions and conversations

# Admin Panel

* Django admin
* Manage all documents
* View all questions

# How to Use the Site?

* First, upload any PDF file from the **"Upload&Process"** section on the left side of the site and click the button
* Wait for the AI to respond
* If you have a question, type it into the chat panel that appears
* In the **Ask Questions** section, the chunk count can be adjusted
* If you enter a question in the **Ask Questions** section before uploading the PDF, the system will return the answer to your question instead of a summary
