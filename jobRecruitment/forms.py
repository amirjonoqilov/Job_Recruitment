from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from .models import Candidate, Company, JobPosting, Interview

class BaseStyledModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

class CandidateForm(BaseStyledModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '')
        if phone and (not phone.startswith("998") or len(phone) != 12):
            raise ValidationError("Phone number must be in format: 998XXXXXXXXX")
        return phone

class CompanyForm(BaseStyledModelForm):
    class Meta:
        model = Company
        fields = '__all__'

class JobPostingForm(BaseStyledModelForm):
    class Meta:
        model = JobPosting
        fields = '__all__'

class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['candidate', 'job', 'interviewer', 'interview_time', 'status', 'notes']
        widgets = {
            'interview_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes...'
            }),
        }
