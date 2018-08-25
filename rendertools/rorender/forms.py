from django import forms

from .module.network import LocalNetworkScanner


class find_by_hostname(forms.Form):
    hostname = forms.CharField(label='', max_length=100)

class scan_ip(forms.Form):
    local_ip = LocalNetworkScanner().get_local_data()['ip'].split('.')

    ip_one = forms.IntegerField(label='', max_value=255, min_value=1, widget=forms.TextInput(attrs={'placeholder':local_ip[0]}))
    ip_two = forms.IntegerField(label='', max_value=255, min_value=1, widget=forms.TextInput(attrs={'placeholder':local_ip[1]}))
    ip_three = forms.IntegerField(label='', required=False, max_value=255, min_value=1, widget=forms.TextInput(attrs={'placeholder':local_ip[2]}))
    ip_four = forms.IntegerField(label='', required=False, max_value=255, min_value=1, widget=forms.TextInput(attrs={'placeholder':local_ip[3]}))