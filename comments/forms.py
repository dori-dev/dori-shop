from django import forms

from . import models


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = models.ProductComment
        fields = (
            'body',
        )
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'class': 'input',
                    'placeholder': 'نظر شما ...',
                }
            )
        }
