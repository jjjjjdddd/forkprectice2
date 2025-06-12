from django import forms
from .models import Menu

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'total_servings', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        } 