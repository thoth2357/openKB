from django import forms
from django.core.exceptions import ValidationError
from mdeditor.fields import MDTextFormField
from kb.models import Article

class MDEditorForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'keywords']

    def __init__(self, *args, **kwargs):
        super(MDEditorForm, self).__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter article title',
            'minlength': '5'  # HTML5 attribute to enforce minimum length
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control markdown-editor',
            'placeholder': 'Write your article content here...'
        })
        self.fields['keywords'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
        self.fields['keywords'].required = False  # Set keywords as not required

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('The title must be at least 5 characters long.')
        return title

    def save(self, commit=True):
        instance = super(MDEditorForm, self).save(commit=False)
        instance.title = self.cleaned_data.get('title', '') + "(SUGGESTION)" 
        instance.published = False
        if commit:
            instance.save()
        return instance
