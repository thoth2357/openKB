import os

from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError

from kb.models import (Article, ArticleSettings, DisplaySettings,
                       StyleSettings, WebsiteSettings)


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


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()  # Fetches your custom user model
        fields = ("email", "username")  # Includes email and username

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True


class EditUserForm(UserChangeForm):
    password1 = forms.CharField(label='User password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), required=False)
    password2 = forms.CharField(label='Password confirm', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}), required=False)
    is_superuser = forms.BooleanField(label='Admin status', required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2', 'is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class MyAccountForm(UserChangeForm):
    password1 = forms.CharField(label='New Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,  # Removes default help texts
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password1 != password2:
            raise ValidationError("Passwords don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class ArticleForm(forms.ModelForm):
    permalink = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Permalink for the article'
    }))
    status = forms.ChoiceField(choices=[('draft', 'Draft'), ('published', 'Published')], widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Article
        fields = ['title', 'content', 'keywords', 'permalink', 'status', 'seo_title', 'seo_description', 'featured']

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        # Update form field attributes here as needed
        # Setting initial values based on instance attributes
        if self.instance and self.instance.pk:
            self.fields['status'].initial = 'published' if self.instance.published else 'draft'

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter article title'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'form-control markdown-editor',
            'placeholder': 'Write your article content here...'
        })
        self.fields['keywords'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter keywords separated by commas'
        })
        self.fields['seo_title'].widget.attrs.update({'class': 'form-control'})
        self.fields['seo_description'].widget.attrs.update({'class': 'form-control'})

        self.fields['keywords'].required = False
        self.fields['seo_title'].required = False
        self.fields['seo_description'].required = False

    def clean_permalink(self):
        permalink = self.cleaned_data.get('permalink', '').strip()
        if permalink and Article.objects.filter(permalink=permalink).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This permalink is already in use. Please use another one.')
        # Allow empty permalink to clear the field
        return permalink
    

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('The title must be at least 5 characters long.')
        return title
    
    def save(self, commit=True):
        instance = super(ArticleForm, self).save(commit=False)
        # Set permalink to None if cleaned data is empty
        instance.permalink = self.cleaned_data['permalink'] if self.cleaned_data['permalink'] else None
        if commit:
            instance.save()
        return instance
    

class WebsiteSettingsForm(forms.ModelForm):
    class Meta:
        model = WebsiteSettings
        fields = '__all__'
        widgets = {
            'website_title': forms.TextInput(attrs={'class': 'form-control'}),
            'website_description': forms.Textarea(attrs={'class': 'form-control'}),
            'show_logo': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'base_url': forms.TextInput(attrs={'class': 'form-control'}),
            'allow_api': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'api_token': forms.TextInput(attrs={'class': 'form-control'}),
            'password_protect': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'index_article_body': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'select_theme': forms.Select(choices=[("darkly", 'Darkly'), (None, 'Default')], attrs={'class': 'form-control'}),
            'select_language': forms.Select(choices=[("en", "English"), ("fr", "French")], attrs={'class': 'form-control'}),
            'show_logon_link': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'date_format': forms.TextInput(attrs={'class': 'form-control'}),
            'article_suggestions_allowed': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'google_analytics_code': forms.Textarea(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'website_title': 'The title of your website.',
            'website_description': 'A short description that appears in search engine results.',
            'show_logo': 'Toggle to show or hide the website logo.',
            'base_url': 'The root URL where your site is hosted. Eg: http://example.com/',
            'allow_api': 'Allow external systems to access site data via API.',
            'api_token': 'The security token others will use to access your API.',
            'password_protect': 'Require users to log in before accessing the site.',
            'index_article_body': 'Include the text of articles in the search index.',
            'select_theme': 'The visual theme for the site. Leave blank for default styling.',
            'select_language': 'The language the site interface will appear in.',
            'show_logon_link': 'Display a link for users to log on if needed.',
            'date_format': 'Format in which dates are displayed on the site.',
            'article_suggestions_allowed': 'Allow users to submit articles for potential inclusion.',
            'google_analytics_code': 'Google Analytics code to track site usage.',
        }


class ArticleSettingsForm(forms.ModelForm):
    class Meta:
        model = ArticleSettings
        fields = '__all__'
        widgets = {
            'allow_voting': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'show_article_meta': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'show_author_email': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'article_links_open_new_page': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'add_header_anchors': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'enable_editor_spellchecker': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'allow_article_versioning': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'allow_mermaid': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'allow_mathjax': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
        }
        help_texts = {
            'allow_voting': 'Whether to allow users to vote on an article.',
            'show_article_meta': 'Whether to show article meta data including published date, last updated date, author etc.',
            'show_author_email': 'Controls whether the authors email address is displayed in the meta. Requires "Show article meta data".',
            'article_links_open_new_page': 'Controls whether links within articles open a new page (tab).',
            'add_header_anchors': 'Whether to add HTML anchors to all heading tags for linking within articles or direct linking from other pages.',
            'enable_editor_spellchecker': 'Controls whether to enable the editor spellchecker.',
            'allow_article_versioning': 'Whether to track article versions with each save of the editor.',
            'allow_mermaid': 'Whether to enable mermaid.',
            'allow_mathjax': 'Whether to enable MathJax.',
        }


class DisplaySettingsForm(forms.ModelForm):
    class Meta:
        model = DisplaySettings
        fields = '__all__'
        help_texts = {
            'number_of_top_articles': 'Sets the number of results shown on the home page.',
            'show_published_date': 'Shows the published date next to the results on the homepage and search.',
            'show_view_count': 'Shows the view count next to the results on the homepage and search.',
            'update_view_count_when_logged_in': 'Updates the view count also when users are logged in.',
            'show_featured_articles': 'Whether to show any articles set to featured in a sidebar.',
            'show_featured_articles_when_viewing_article': 'Whether to show any articles set to featured in a sidebar when viewing an article.',
            'featured_article_count': 'The number of featured articles shown.',
        }
        widgets = {
            'number_of_top_articles': forms.NumberInput(attrs={'class': 'form-control'}),
            'show_published_date': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'show_view_count': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'update_view_count_when_logged_in': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'show_featured_articles': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'show_featured_articles_when_viewing_article': forms.Select(choices=[(True, 'True'), (False, 'False')], attrs={'class': 'form-control'}),
            'featured_article_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StyleSettingsForm(forms.ModelForm):
    class Meta:
        model = StyleSettings
        fields = '__all__'
        widgets = {
            'header_background_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'header_text_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'footer_background_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'footer_text_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'button_background_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'button_text_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'link_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'page_text_color': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'page_font': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'header_background_color': 'Set the background color for the header using HEX code.',
            'header_text_color': 'Set the text color for the header using HEX code.',
            'footer_background_color': 'Set the background color for the footer using HEX code.',
            'footer_text_color': 'Set the text color for the footer using HEX code.',
            'button_background_color': 'Set the background color for buttons using HEX code.',
            'button_text_color': 'Set the text color for buttons using HEX code.',
            'link_color': 'Set the color for hyperlinks using HEX code.',
            'page_text_color': 'Set the text color for the page using HEX code.',
            'page_font': 'Set the font used on the page.',
        }


class FileUploadForm(forms.Form):
    file = forms.FileField(label='Select file', widget=forms.ClearableFileInput(attrs={"class": "form-control",'allow_multiple_selected': True}))
    upload_directory = forms.ChoiceField(label='Upload directory', required=True, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    
    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        # Set the directory choices after initialization
        self.fields['upload_directory'].choices = self.get_directory_choices()

    def get_directory_choices(self):
        # List directories from the base path
        base_path = os.path.join(settings.MEDIA_ROOT, 'uploads')  # Replace with your actual path
        try:
            directories = ["/"+f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]
            directory_choices = [(os.path.join(base_path, d), d) for d in directories]
        except FileNotFoundError:
            directory_choices = []
        return directory_choices
    
class DirectoryForm(forms.Form):
    new_directory = forms.CharField(label='New directory', required=True,widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter new directory name'
    }))