from django.contrib import admin
from .models import PDFDocument, Question, DocumentSummary


@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'uploaded_at', 'uploaded_by', 'num_pages', 'num_chunks', 'processed']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['title']
    readonly_fields = ['uploaded_at', 'file_size', 'num_pages', 'num_chunks']

    fieldsets = (
        ('Document Info', {
            'fields': ('title', 'file', 'uploaded_by')
        }),
        ('Processing Status', {
            'fields': ('processed', 'processing_error')
        }),
        ('Statistics', {
            'fields': ('file_size', 'num_pages', 'num_chunks', 'uploaded_at')
        }),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_question', 'document', 'asked_at', 'asked_by', 'response_time']
    list_filter = ['asked_at', 'document']
    search_fields = ['question_text', 'answer_text']
    readonly_fields = ['asked_at', 'response_time']

    def short_question(self, obj):
        return obj.question_text[:50] + '...' if len(obj.question_text) > 50 else obj.question_text

    short_question.short_description = 'Question'


@admin.register(DocumentSummary)
class DocumentSummaryAdmin(admin.ModelAdmin):
    list_display = ['document', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['document__title', 'summary_text']