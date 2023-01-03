from django.forms import Form, DateField
from tempus_dominus.widgets import DatePicker


class YearAddingForm(Form):
    date = DateField(widget=DatePicker())

    class Meta:
        fields = ["date"]
