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


# SCREENSHOTS
<img width="1229" height="831" alt="Ekran Resmi 2026-01-12 14 12 57" src="https://github.com/user-attachments/assets/1fe88ad0-4db5-427e-815c-167bae9f227b" />
<img width="1229" height="831" alt="Ekran Resmi 2026-01-12 14 12 48" src="https://github.com/user-attachments/assets/4328ed07-02f4-4c71-854a-ad6db2f2819f" />
<img width="1229" height="831" alt="Ekran Resmi 2026-01-12 14 12 42" src="https://github.com/user-attachments/assets/6f6bdfa0-124b-4813-948b-0cd92ccff19d" />
<img width="1229" height="831" alt="Ekran Resmi 2026-01-12 14 12 30" src="https://github.com/user-attachments/assets/9dd2b7ac-ee86-4d1b-92b0-d7b6f1e3294b" />
<img width="1229" height="831" alt="Ekran Resmi 2026-01-12 14 11 58" src="https://github.com/user-attachments/assets/3dbaeb18-d008-48f2-8ca1-dfd44e41a88a" />

