from django import forms
# from multi_email_field.forms import MultiEmailField
from .models import Aktiviti
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from datetime import datetime

# Change Input from Text to Date Type
# Source : https://stackoverflow.com/questions/22846048/django-form-as-p-datefield-not-showing-input-type-as-date
class DateInput(forms.DateInput):
    input_type = 'date'
    input_formats=('%d-%m-%Y %H:%M',)

# Change Input from Text to Date Time local Type
class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'
    input_formats=('%d-%m-%Y %H:%M',)

# Aktiviti Add/Edit form
# Use input='date' for modern browser only 
class AktivitiForm(forms.ModelForm):
    
    mula = forms.DateTimeField(widget=DateTimeInput())
    akhir = forms.DateTimeField(widget=DateTimeInput())

    # Verify Masa mula mestilah lebih awal daripada masa akhir
    def clean(self):
        data = self.cleaned_data
        # print(str(self.cleaned_data['mula'])[:-9],self.cleaned_data['akhir'])
        if datetime.strptime(str(self.cleaned_data['mula'])[:-9],'%Y-%m-%d %H:%M') >= datetime.strptime(str(self.cleaned_data['akhir'])[:-9],'%Y-%m-%d %H:%M'):
            raise forms.ValidationError("Masa tarikh / masa mula mestilah lebih awal daripada tarikh / masa akhir !") 
        return data

    class Meta:
        model = Aktiviti
        fields = ('mula', 'akhir', 'tajuk','hadpeserta','tempat','penceramah','penganjur','status',)

# Jemputan Aktiviti form
class JemputanForm(forms.Form):
    tojemput = forms.EmailField(label='Emel Penerima Jemputan',required=True)
    subjemput = forms.CharField(label='Subjek',max_length=100,required=True)
    msgjemput = forms.CharField(label='Mesej',widget=forms.Textarea,required=True)
    