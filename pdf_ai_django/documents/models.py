from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PDFDocument(models.Model):
    """Model to store PDF document metadata"""

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(default=timezone.now)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    file_size = models.IntegerField(help_text="File size in bytes")
    num_pages = models.IntegerField(default=0, help_text="Number of pages in PDF")
    num_chunks = models.IntegerField(default=0, help_text="Number of text chunks created")
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = "PDF Document"
        verbose_name_plural = "PDF Documents"

    def __str__(self):
        return self.title

    def get_filename(self):
        """Get just the filename without path"""
        return self.file.name.split('/')[-1]


class Question(models.Model):
    """Model to store questions asked about documents"""

    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    question_text = models.TextField()
    answer_text = models.TextField()
    asked_at = models.DateTimeField(default=timezone.now)
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    response_time = models.FloatField(help_text="Response time in seconds", null=True, blank=True)

    class Meta:
        ordering = ['-asked_at']
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return f"{self.question_text[:50]}..."


class DocumentSummary(models.Model):
    """Model to store document summaries"""

    document = models.OneToOneField(PDFDocument, on_delete=models.CASCADE, related_name='summary')
    summary_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Document Summary"
        verbose_name_plural = "Document Summaries"

    def __str__(self):
        return f"Summary of {self.document.title}"