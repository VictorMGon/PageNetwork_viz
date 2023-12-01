from django import forms

class url_form(forms.Form):
    url = forms.URLField(label="Starting URL",max_length=200)