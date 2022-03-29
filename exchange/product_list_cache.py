from exchange.models import ProductList


class ProductListCache(object):
    def __init__(self):
        print("init")

        self.product_list = ProductList.objects.values(
            "category", "type", "name"
        ).order_by("category", "type", "name")
        self.product_list_distinct = self.product_list.distinct()

    def get_product_list_distinct(self):
        return self.product_list_distinct

    def pee(self):
        return self.product_list_distinct[0]
