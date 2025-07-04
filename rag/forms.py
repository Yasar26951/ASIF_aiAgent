from django import forms

class box(forms.Form):
    YOU = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': 'boxy',
            'placeholder': 'Type your message here...',
            'rows': 4,
            'cols': 60
        })
    )
