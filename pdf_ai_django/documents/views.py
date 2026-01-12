from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import time
import os

from .models import PDFDocument, Question, DocumentSummary
from .forms import PDFUploadForm, QuestionForm
from .utils import process_pdf, get_qa_engine


def home(request):
    """Home page with upload and question forms"""
    upload_form = PDFUploadForm()
    question_form = QuestionForm()

    # Get recent documents
    recent_docs = PDFDocument.objects.filter(processed=True)[:5]

    # Get recent questions
    recent_questions = Question.objects.all()[:10]

    # Get statistics
    total_docs = PDFDocument.objects.filter(processed=True).count()
    total_questions = Question.objects.count()

    context = {
        'upload_form': upload_form,
        'question_form': question_form,
        'recent_docs': recent_docs,
        'recent_questions': recent_questions,
        'total_docs': total_docs,
        'total_questions': total_questions,
    }

    return render(request, 'documents/home.html', context)


def upload_pdf(request):
    """Handle PDF upload"""
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_doc = form.save(commit=False)

            # Auto-generate title from filename
            filename = pdf_doc.file.name
            pdf_doc.title = filename.replace('.pdf', '').replace('_', ' ')

            # Set file size
            pdf_doc.file_size = pdf_doc.file.size

            # Set uploader
            if request.user.is_authenticated:
                pdf_doc.uploaded_by = request.user

            pdf_doc.save()

            # Process PDF in background
            try:
                success, message, chunks_count, pages_count = process_pdf(pdf_doc)

                if success:
                    pdf_doc.processed = True
                    pdf_doc.num_chunks = chunks_count
                    pdf_doc.num_pages = pages_count
                    pdf_doc.save()

                    # Auto-generate summary
                    try:
                        engine = get_qa_engine()
                        summary_text = engine.summarize_document(pdf_source=pdf_doc.get_filename())

                        # Save summary
                        DocumentSummary.objects.create(
                            document=pdf_doc,
                            summary_text=summary_text
                        )

                        messages.success(request, f'✅ PDF processed! {chunks_count} chunks from {pages_count} pages.')
                    except Exception as e:
                        messages.success(request, f'✅ PDF processed! {chunks_count} chunks from {pages_count} pages.')

                    # Redirect to chat page
                    return redirect('document_detail', pk=pdf_doc.pk)
                else:
                    pdf_doc.processing_error = message
                    pdf_doc.save()
                    messages.error(request, f'❌ Error: {message}')
                    return redirect('home')

            except Exception as e:
                pdf_doc.processing_error = str(e)
                pdf_doc.save()
                messages.error(request, f'❌ Error: {str(e)}')
                return redirect('home')
    else:
        form = PDFUploadForm()

    return render(request, 'documents/upload.html', {'form': form})


def ask_question(request):
    """Handle question asking"""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question']
            top_k = form.cleaned_data.get('top_k', 5)

            # Document ID'yi POST'tan al (hidden input'tan)
            document_id = request.POST.get('document')
            document = None
            if document_id:
                try:
                    document = PDFDocument.objects.get(pk=document_id)
                except PDFDocument.DoesNotExist:
                    document = None

            # Get QA engine
            engine = get_qa_engine()

            # Start timer
            start_time = time.time()

            # Get answer
            try:
                pdf_source = document.get_filename() if document else None
                result = engine.answer_question(
                    question=question_text,
                    top_k=top_k,
                    pdf_source=pdf_source
                )

                # Calculate response time
                response_time = time.time() - start_time

                # Save question and answer
                question_obj = Question.objects.create(
                    document=document,
                    question_text=question_text,
                    answer_text=result['answer'],
                    response_time=response_time,
                    asked_by=request.user if request.user.is_authenticated else None
                )

                # For AJAX requests
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': True,
                        'answer': result['answer'],
                        'sources': result['sources'],
                        'response_time': response_time
                    })

                # If question was asked about specific document, go to that document's chat page
                if document:
                    messages.success(request, '✅ Question answered!')
                    return redirect('document_detail', pk=document.pk)

                # Otherwise, show answer on separate page
                context = {
                    'question': question_text,
                    'answer': result['answer'],
                    'sources': result['sources'],
                    'response_time': response_time,
                    'form': QuestionForm()
                }
                return render(request, 'documents/answer.html', context)

            except Exception as e:
                messages.error(request, f'❌ Error: {str(e)}')
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': str(e)})
                return redirect('home')

    return redirect('home')



def document_list(request):
    """List all documents"""
    documents = PDFDocument.objects.filter(processed=True)

    context = {
        'documents': documents
    }

    return render(request, 'documents/document_list.html', context)


def document_detail(request, pk):
    """View document details and ask questions about it"""
    document = get_object_or_404(PDFDocument, pk=pk)

    # Get questions about this document
    questions = document.questions.all()[:20]

    # Get or create summary
    try:
        summary = document.summary
    except DocumentSummary.DoesNotExist:
        summary = None

    context = {
        'document': document,
        'questions': questions,
        'summary': summary,
        'question_form': QuestionForm(initial={'document': document})
    }

    return render(request, 'documents/document_detail.html', context)


def generate_summary(request, pk):
    """Generate summary for a document"""
    document = get_object_or_404(PDFDocument, pk=pk, processed=True)

    # Check if summary already exists
    try:
        summary = document.summary
        messages.info(request, 'Summary already exists!')
        return redirect('document_detail', pk=pk)
    except DocumentSummary.DoesNotExist:
        pass

    # Generate summary (kendi kendine)
    try:
        engine = get_qa_engine()
        summary_text = engine.summarize_document(pdf_source=pdf_doc.get_filename())

        # Save summary
        DocumentSummary.objects.create(
            document=pdf_doc,
            summary_text=summary_text
        )

        messages.success(request, f'✅ PDF processed! {chunks_count} chunks from {pages_count} pages. Summary ready!')
    except Exception as e:
        # Don't fail if Ollama is not running
        messages.warning(request,
                         f'✅ PDF processed! {chunks_count} chunks. (Summary generation failed - make sure Ollama is running)')

    return redirect('document_detail', pk=pk)


def delete_document(request, pk):
    """Delete a document"""
    document = get_object_or_404(PDFDocument, pk=pk)

    if request.method == 'POST':
        # Delete from vector store
        try:
            from .utils import get_vector_store
            store = get_vector_store()
            store.delete_by_source(document.get_filename())
        except Exception as e:
            print(f"Error deleting from vector store: {e}")

        # Delete file
        if document.file:
            if os.path.isfile(document.file.path):
                os.remove(document.file.path)

        # Delete from database
        document.delete()

        messages.success(request, '✅ Document deleted successfully!')
        return redirect('document_list')

    return render(request, 'documents/document_confirm_delete.html', {'document': document})


def question_history(request):
    """View all questions asked"""
    questions = Question.objects.all()

    context = {
        'questions': questions
    }

    return render(request, 'documents/question_history.html', context)