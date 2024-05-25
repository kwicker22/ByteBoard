from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CreateRecruiterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "city",
            "state",
            "job_type",
            "salary",
            "description",
            "date_published",
            "company_description",
        ]





class JobEditForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "city",
            "state",
            "job_type",
            "salary",
            "description",
            "date_published",
            "company_description",
        ]


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ["first_name", "last_name", "resume"]


# class SearchForm(forms.Form ):
