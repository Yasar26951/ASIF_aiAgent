from django import forms

class inputform(forms.Form):
    message= forms.Textarea(id="text-box")