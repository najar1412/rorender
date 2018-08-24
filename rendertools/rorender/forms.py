from django import forms


class find_by_hostname(forms.Form):
    hostname = forms.CharField(label='', max_length=100)

class scan_ip(forms.Form):
    ip_one = forms.IntegerField(label='')
    ip_two = forms.IntegerField(label='')
    ip_three = forms.IntegerField(label='')
    ip_four = forms.IntegerField(label='')