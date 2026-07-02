from django import forms

class UrlForm(forms.Form):

    longurl=forms.CharField(max_length=200)