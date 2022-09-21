from django import forms

from exchange.models import Product

class ListWidgets(forms.TextInput):
    def __init__(self):
        super(ListWidgets, self).__init__()

    def value_from_datadict(self, data, files, name):
        return data.getlist(name)


class ListField(forms.Field):
    def __init__(self, *, convert_type=eval, empty_value=None, **kwargs):
        if empty_value is None:
            empty_value = []
        self.convert_type = convert_type
        self.empty_value = empty_value
        self.widget = ListWidgets
        super().__init__(**kwargs)
    
    def to_python(self, value):
        """Return a string."""
        if value == self.empty_values:
            return self.empty_value
        return [self.convert_type(v) for v in value]


class ProductListForm(forms.Form):
    """對應的參數可去model找對應"""
    ordering = forms.CharField(required=False)
    category = forms.CharField()  # 必須輸入，避免資料撈太久
    type = forms.CharField()      # 必須輸入，避免資料撈太久
    name = forms.CharField(required=False)
    stage_level = ListField(required=False)
    min_star = forms.IntegerField(required=False)
    max_star = forms.IntegerField(required=False)
    is_maple = forms.BooleanField(required=False)
    total_level = forms.IntegerField(required=False)
    maple_capability = forms.ChoiceField(choices=Product.MapleCapability.choices, required=False)
    min_price = forms.IntegerField(required=False)
    max_price = forms.IntegerField(required=False)
    career = forms.CharField(required=False)
    server_name = forms.CharField(required=False)

