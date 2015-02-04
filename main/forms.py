from django import forms
from main.models import Entry
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        widgets = {
            'author': forms.HiddenInput(),
            'title': forms.HiddenInput(),
            'pub_date': forms.HiddenInput(),
            'last_edited': forms.HiddenInput(),
            'positivevoters': forms.HiddenInput(),
            'negativevoters': forms.HiddenInput()
            }

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'ornek@domain.com'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user
