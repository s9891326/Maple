from django import forms

from exchange.models import Product


class ProductListForm(forms.Form):
    category = forms.CharField(required=False)
    type = forms.CharField(required=False)
    stage_level = forms.CharField(required=False)
    star = forms.IntegerField(required=False)
    is_maple = forms.BooleanField(required=False)
    total_level = forms.IntegerField(required=False)
    maple_capability = forms.ChoiceField(choices=Product.MapleCapability.choices, required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)

