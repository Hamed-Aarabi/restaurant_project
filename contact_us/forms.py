from django import forms

from contact_us.models import Message


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

        widgets = {
            'name':forms.TextInput(attrs={'placeholder':'Name', 'class':'form-control'}),
            'email':forms.EmailInput(attrs={'placeholder':'Email', 'class':'form-control'}),
            'phone':forms.TextInput(attrs={'placeholder':'Phone', 'class':'form-control'}),
            'message':forms.Textarea(attrs={'placeholder':'Message', 'class':'form-control'})
        }