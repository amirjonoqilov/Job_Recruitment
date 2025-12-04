from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

# Base classes to add Bootstrap styling
class BaseStyledForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

class BaseStyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

# User registration form
class CustomUserCreationForm(BaseStyledModelForm, UserCreationForm):
    ROLE_CHOICES = (
        ('candidate', 'Candidate'),
        ('company', 'Company')
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(), label="Register as")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']
        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

# Login form
class CustomLoginForm(BaseStyledForm, AuthenticationForm):
    class Meta:
        username = forms.CharField(label="Username")
        password = forms.CharField(label="Password", widget=forms.PasswordInput())
