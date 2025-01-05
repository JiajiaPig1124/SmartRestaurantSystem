from django import forms
from .models import Cuisine, Dish

class CuisineForm(forms.ModelForm):
    class Meta:
        model = Cuisine
        fields = ['name', 'description']

class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = [
            'merchant',
            'cuisine',
            'name',
            'description',
            'price',
            'image',
            'stock',
            'is_available'
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'}) 