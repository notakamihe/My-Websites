from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import datetime

from .models import ForumUser

class DateInput(forms.DateInput):
    input_type = 'date'


class CreateUserForm (UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'form-control bg-transparent focus-thicken', 'id': key })

            if key == 'password1':
                value.widget.attrs.update({'placeholder': 'Enter your password'})
            elif key == 'password2':
                value.widget.attrs.update({'placeholder': 'Confirm password here'})
            else:
                value.widget.attrs.update({'placeholder': f'Enter the {key}'})


class ForumUserForm (forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = ['first_name', 'surname', 'email', 'phone', 'dob', 'location']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].widget = DateInput()

        for key, value in self.fields.items():
            value.widget.attrs.update({'class': 'form-control bg-transparent focus-thicken', 'id': key })

            if key == 'first_name':
                value.widget.attrs.update({'placeholder': 'Enter your first name'})
            elif key == 'phone':
                value.widget.attrs.update({'placeholder': 'Enter your phone number'})
            else:
                value.widget.attrs.update({'placeholder': f'Enter the {key}'})

    def clean_phone (self):
        phone = self.cleaned_data.get('phone')

        if not all(letter.isdigit() for letter in phone):
            raise ValidationError('Invalid phone-number.')

        return phone

    def clean_dob (self):
        dob = self.cleaned_data.get('dob')

        if dob.year < 1899 or dob > datetime.datetime.now().date():
            raise ValidationError('Invalid date.')
        if datetime.datetime.now().year - dob.year < 13:
            raise ValidationError('Too young. You must be at least 13.')

        return dob
