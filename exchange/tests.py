from django.test import TestCase

from rest_framework.test import APITestCase, APIClient

from exchange.models import ProductList


class ProductListTestCase(APITestCase):
    
    def setUp(self) -> None:
        print("setUp")
        
        self.client = APIClient()
        self.url = "/exchange/product-list"
        self.request_data = dict(
            category="武器",
            type="雙手劍",
            name="普錫杰勒雙手劍2",
            stage_level=1
        )
        self.product_list = ProductList.objects.create(**self.request_data)
    
    def test_api_product_list_create(self):
        print("test_api_product_list_create")
        self.response = self.client.post(self.url, self.request_data, format="json")
        print(self.response)
