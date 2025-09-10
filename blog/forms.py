from django import forms
from .models import ContactSubmission


class ContactSubmissionForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['submission_type', 'name', 'email', 'title', 'description', 'region', 'content']
        widgets = {
            'submission_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'submission_type'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'aledariabr@gmail.com'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Title of your recipe or story'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Brief description of what you want to share...'
            }),
            'region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Country or region of origin'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Full recipe with ingredients and instructions, or your complete story...'
            }),
        }
        labels = {
            'submission_type': 'What would you like to share?',
            'name': 'Your Name',
            'email': 'Email Address',
            'title': 'Title',
            'description': 'Short Description',
            'region': 'Country/Region',
            'content': 'Full Content',
        }
