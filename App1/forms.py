from django import forms
from .models import Stuff

class StuffForm(forms.ModelForm):
    class Meta:
        model = Stuff
        fields = ['Firstname', 'Lastname', 'Position', 'Year', 'Phone', 'Address']
        labels = {
            'Firstname': 'Họ',
            'Lastname': 'Tên',
            'Position': 'Vị trí',
            'Year': 'Năm sinh',
            'Phone': 'Số điện thoại',
            'Address': 'Địa chỉ',
        }