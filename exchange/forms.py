from django import forms

from exchange.models import Product


class ProductListForm(forms.Form):
    ordering = forms.CharField(required=False)
    category = forms.CharField()  # 必須輸入，避免資料撈太久
    type = forms.CharField()      # 必須輸入，避免資料撈太久
    stage_level = forms.IntegerField(required=False)
    star = forms.IntegerField(required=False)
    is_maple = forms.BooleanField(required=False)
    total_level = forms.IntegerField(required=False)
    maple_capability = forms.ChoiceField(choices=Product.MapleCapability.choices, required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)

