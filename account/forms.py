from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core import validators
from django.core.exceptions import ValidationError
from .models import Client, Otp, Address


def password_validator(value):
    if value.isnumeric() or value.isalpha():
        raise ValidationError('Password must be contain letters and numbers', code='letter_error')


class ClientCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', validators=[validators.MinLengthValidator(8),password_validator],widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Create Your Password'}))
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Your Password'}))

    class Meta:
        model = Client
        fields = ('phone',)

        widgets = {
            'phone':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Phone Number'}),
            # 'username':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Username'}),
            # 'profile_pic':forms.FileInput(attrs={'class':'form-control'}),
            # 'email':forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Your Email Address'}),

        }

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        phone = self.cleaned_data.get('phone')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords Not Match', code='pass_not_match')
        if Client.objects.filter(phone=phone).exists():
            raise ValidationError('This phone already exist.', code='phone_exist')


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ClientChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = Client
        fields = ('email','phone','username','profile_pic')




class OtpCreationForm(forms.ModelForm):

    password2_otp = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Your Password'}))
    password1_otp = forms.CharField(validators=[validators.MinLengthValidator(8), password_validator], widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create Your Password'}))
    class Meta:
        model = Otp
        fields = ('phone',)

        widgets= {
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),

        }

    def clean(self):
        pass1 = self.cleaned_data.get('password1_otp')
        pass2 = self.cleaned_data.get('password2_otp')
        phone = self.cleaned_data.get('phone')
        if pass1 and pass2 and pass1 != pass2:
            raise ValidationError('Passwords Not Match', code='pass_not_match_otp')
        if Client.objects.filter(phone=phone).exists():
            raise ValidationError('This phone already exist.', code='phone_exist_otp')


class OtpForm(forms.Form):
    otp_input = forms.CharField(validators=[validators.MinLengthValidator(4), validators.MaxLengthValidator(4)],widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter One Time Code'}))

    def clean(self):
        otp_input = self.cleaned_data.get('otp_input')
        if not Otp.objects.filter(otp_code=otp_input, expired=False).exists():
            raise ValidationError('One Time Password is not valid!!')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if authenticate(username=username, password=password) is None:
            raise ValidationError('Wrong Password or Username!!', code='wrong_password_username')

class AddressForm(forms.ModelForm):
    client = forms.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ('state','city','address')

        widgets = {
            'state':forms.TextInput(attrs={'placeholder':'Enter your state...'}),
            'city':forms.TextInput(attrs={'placeholder':'Enter your city...'}),
            'address':forms.Textarea(attrs={'placeholder':'Enter your address...'})
        }