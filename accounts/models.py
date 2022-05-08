from django.db import models
from agenda.models import Contact
from django import forms

# Create your models here.
class FormContact(forms.ModelForm):
  class Meta:
    model = Contact
    exclude = ()