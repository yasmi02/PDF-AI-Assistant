from django import forms
from .models import PDFDocument, Question


# ASK QUESTIONS VE UPLOAD PFD

#PDF UPLOADER
class PDFUploadForm(forms.ModelForm):
    """Form for uploading PDF documents"""

    class Meta:
        model = PDFDocument
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf'
            })
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file extension
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')

            # Check file size
            if file.size > 100 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 100MB.')

        return file


# Ask Questions

class QuestionForm(forms.Form):
    """Form for asking questions about documents"""

    question = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ask a question about your document...'
        }),
        label='Your Question',
        max_length=1000
    )

    top_k = forms.IntegerField(
        initial=5,
        min_value=1,
        max_value=20,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'style': 'width: 100px;'
        }),
        label='Number of chunks to retrieve',
        help_text='Higher numbers provide more context but slower responses'
    )