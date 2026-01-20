from django import forms
from .models import Item, Category


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            'name',
            'category',
            'item_type',
            'rarity',
            'value',
            'demand',
            'trend',
            'is_limited',
            'featured',
            'obtained_from',
            'image_url',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={}),
            'category': forms.Select(attrs={}),
            'item_type': forms.Select(attrs={}),
            'rarity': forms.Select(attrs={}),
            'value': forms.NumberInput(attrs={}),
            'demand': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'trend': forms.Select(attrs={}),
            'is_limited': forms.CheckboxInput(attrs={}),
            'featured': forms.CheckboxInput(attrs={}),
            'obtained_from': forms.TextInput(attrs={}),
            'image_url': forms.URLInput(attrs={'placeholder': '/media/Weapons/Item.png'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().order_by('name')
