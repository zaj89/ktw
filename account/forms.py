from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')
        return cd['password2']


class ProfileRegisterForm(forms.ModelForm):
    phone_number = forms.CharField(label='Numer Telefonu')

    class Meta:
        model = Profile
        fields = ('gender', 'phone_number', 'city',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'phone_number', 'city',)


class EventForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'phone_number', 'city',)


class AdminToUserMailForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
