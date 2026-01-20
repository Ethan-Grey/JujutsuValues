from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Item, Category, ValueChangeRequest


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "category",
            "item_type",
            "rarity",
            "value",
            "demand",
            "trend",
            "is_limited",
            "featured",
            "obtained_from",
            "image_url",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={}),
            "category": forms.Select(attrs={}),
            "item_type": forms.Select(attrs={}),
            "rarity": forms.Select(attrs={}),
            "value": forms.NumberInput(attrs={}),
            "demand": forms.NumberInput(attrs={"min": 1, "max": 10}),
            "trend": forms.Select(attrs={}),
            "is_limited": forms.CheckboxInput(attrs={}),
            "featured": forms.CheckboxInput(attrs={}),
            "obtained_from": forms.TextInput(attrs={}),
            "image_url": forms.URLInput(attrs={"placeholder": "https://example.com/image.png or /media/Weapons/Item.png"}),
            "notes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all().order_by("name")


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Strip default help texts to keep the theme clean
        for field_name in ["username", "email", "password1", "password2"]:
            if field_name in self.fields:
                self.fields[field_name].help_text = ""


class ValueChangeRequestForm(forms.ModelForm):
    class Meta:
        model = ValueChangeRequest
        fields = ["requested_value", "reason"]
        widgets = {
            "requested_value": forms.NumberInput(attrs={"min": 1, "class": "form-control"}),
            "reason": forms.Textarea(attrs={"rows": 5, "class": "form-control", "placeholder": "Explain why this value should be changed..."}),
        }
        labels = {
            "requested_value": "New Value",
            "reason": "Reason for Change",
        }
