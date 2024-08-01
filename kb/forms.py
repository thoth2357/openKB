from django import forms
from django.core.exceptions import ValidationError
from mdeditor.fields import MDTextFormField
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


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