from django import forms

PRODUCT_COUNT_CHOICES = [
    (number, str(number)) for number in range(1, 6)
]


class CartAddProductForm(forms.Form):
    product_count = forms.TypedChoiceField(
        choices=PRODUCT_COUNT_CHOICES,
        coerce=int,
        widget=forms.Select(
            attrs={
                'class': 'input-select',
            }
        )
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
