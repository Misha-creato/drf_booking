from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from areas.models import Area


class AreaAdminForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = [
            'name',
            'description',
            'address',
            'available',
            'price',
            'capacity',
            'width',
            'length',
        ]
        widgets = {
            'description': CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"},
                config_name='extends'
            ),
        }
