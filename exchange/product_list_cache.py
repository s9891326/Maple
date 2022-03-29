from exchange.models import ProductList


class ProductListCache(object):
    product_list = None
    
    def __init__(self):
        print("init")
        self.product_list = ProductList.objects.values(
            "category", "type", "name"
        ).order_by("category", "type", "name").distinct()
    
    def pee(self):
        return self.product_list[0]
