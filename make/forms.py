from django import forms

class MakeForm(forms.Form):
    file = forms.FileField()
    