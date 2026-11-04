
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User, Donation


# ==========================================
# USER REGISTRATION FORM
# ==========================================

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    first_name = forms.CharField(max_length=150, required=True)

    last_name = forms.CharField(max_length=150, required=True)

    role = forms.ChoiceField(
        choices=[
            ('DONOR', 'Food Donor'),
            ('NGO', 'NGO / Food Bank'),
        ]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'password1',
            'password2',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.role = self.cleaned_data['role']

        if commit:
            user.save()

        return user


# ==========================================
# FOOD DONATION FORM
# ==========================================

class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation

        exclude = [
            'donor',
            'status',
            'created_at',
            'updated_at',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter food donation title'
            }),

            'food_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'dietary_suitability': forms.Select(attrs={
                'class': 'form-select'
            }),

            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01'
            }),

            'unit': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'allergens': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'food_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'use_by': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),

            'collection_location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'collection_start': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),

            'collection_end': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),

            'contact_person': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'contact_phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'collection_instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        use_by = cleaned_data.get('use_by')
        start = cleaned_data.get('collection_start')
        end = cleaned_data.get('collection_end')
        quantity = cleaned_data.get('quantity')

        if quantity is not None and quantity <= 0:
            self.add_error(
                'quantity',
                'Quantity must be greater than zero.'
            )

        if use_by and start and start > use_by:
            self.add_error(
                'collection_start',
                'Collection cannot start after the use-by time.'
            )

        if start and end and end <= start:
            self.add_error(
                'collection_end',
                'Collection end must be after collection start.'
            )

        if use_by and end and end > use_by:
            self.add_error(
                'collection_end',
                'Collection must finish before the use-by time.'
            )

        return cleaned_data
