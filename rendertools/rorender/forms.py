from django import forms

class find_by_hostname(forms.Form):
    hostname = forms.CharField(label='', max_length=100)