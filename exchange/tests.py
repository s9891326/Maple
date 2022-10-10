import copy
import datetime

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from rest_framework.test import APITestCase, APIClient

from accounts.models import CustomUser
from accounts.tests import set_user_credentials, USER_DATA
from exchange.models import ProductList, Product
from utils.util import get_one_week_ago, DATETIME_FORMAT


PRODUCT_LIST_DATA = dict(
    category="武器",
    type="雙手劍",
    name="普錫杰勒雙手劍",
    stage_level=1
)
PRODUCT_MIN_DATA = dict(
    star=10,
    level=10,
    total_level=20,
    cut_num=0,
    attack=0,
    potential_level=Product.Potential.Null.value,
    potential_capability="",
    spark_level=Product.Spark.Null.value,
    spark_capability="",
    is_equippable_soul=False,
    is_maple=True,
    maple_capability=Product.MapleCapability.CriticalDamage.value,
    maple_level=10,
    price=87,
    explanation="",
    server_name=CustomUser.ServerName.Janis,
)
PRODUCT_MAX_DATA = dict(
    star=15,
    level=15,
    total_level=25,
    cut_num=10,
    attack=100,
    potential_level=Product.Potential.Blue.value,
    potential_capability="最大MP:330,命中力8",
    spark_level=Product.Spark.Gold.value,
    spark_capability="經驗值比例轉魔攻,經驗值比例轉物攻",
    is_equippable_soul=True,
    soul_capability="靈魂能力",
    is_maple=False,
    maple_capability=Product.MapleCapability.Null.value,
    maple_level=0,
    price=8877,
    explanation="說明",
    server_name=CustomUser.ServerName.Scania,
)
PRODUCT_DATA = dict(
    PRODUCT_MIN_DATA=PRODUCT_MIN_DATA,
    PRODUCT_MAX_DATA=PRODUCT_MAX_DATA
)

"""
撰寫API TestCase主要針對以下幾種methods進行偵測
GETS、GET、PATCH、POST、DELETE
"""
class ProductListTestCase(APITestCase):
    def setUp(self) -> None:
        print("ProductListTestCase setUp")
        
        self.client = APIClient()
        self.url = reverse('exchange:product_list_api-list')
        self.url_product_column = reverse("exchange:product_list_api-get-product-column")
        
        set_user_credentials(self.client)
        user = CustomUser.objects.get(username=USER_DATA["username"])
        self.product_list = ProductList.objects.create(**PRODUCT_LIST_DATA)
        self.product_min = Product.objects.create(
            product_list_id=self.product_list.product_list_id,
            create_by=user,
            **PRODUCT_MIN_DATA
        )
        self.product_max = Product.objects.create(
            product_list_id=self.product_list.product_list_id,
            create_by=user,
            **PRODUCT_MAX_DATA
        )
    
    def test_1_api_product_list_create(self):
        """
        POST，增加商品列
        :return:
        """
        print("test_1_api_product_list_create")
        
        request = copy.deepcopy(PRODUCT_LIST_DATA)
        request["name"] = f"{request['name']}2"
        response = self.client.post(self.url, request, format="json")
        result = response.data["result"]
        
        self.assertEqual(ProductList.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(result["zh_stage_level"], ProductList.Stage.White.label)
        self.assertEqual(result["category"], request["category"])
        self.assertEqual(result["type"], request["type"])
        self.assertEqual(result["name"], request["name"])
        self.assertEqual(result["stage_level"], request["stage_level"])
    
    def test_2_api_product_list_retrieve(self):
        """
        GET，取得並驗證初始化增加的單個商品列內容
        :return:
        """
        print("test_2_api_product_list_retrieve")
        
        response = self.client.get(f"{self.url}/{self.product_list.product_list_id}")
        result = response.data["result"]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["zh_stage_level"], ProductList.Stage.White.label)
        
        for k, v in PRODUCT_LIST_DATA.items():
            self.assertEqual(result[k], v)
    
    def test_3_api_product_list_list(self):
        """
        GETS，取得並驗證初始化增加所有商品列內容
        :return:
        """
        print("test_3_api_product_list_list")
        
        category = PRODUCT_LIST_DATA["category"]
        _type = PRODUCT_LIST_DATA["type"]
        response = self.client.get(self.url, {"category": category, "type": _type})
        result = response.data["result"][0]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result["zh_stage_level"], ProductList.Stage.White.label)
        self.assertEqual(result["count"], 2)
        self.assertEqual(result["min_price"], PRODUCT_MIN_DATA["price"])
        self.assertEqual(result["max_price"], PRODUCT_MAX_DATA["price"])
        
        for k, v in PRODUCT_LIST_DATA.items():
            self.assertEqual(result[k], v)
    
    def test_4_api_product_list_partial_update(self):
        """
        PATCH，更改並驗證初始化的商品列內容
        :return:
        """
        print("test_4_api_product_list_partial_update")
        
        update_data = dict(
            name="普錫杰勒雙手劍2",
            stage_level=2
        )
        response = self.client.patch(f"{self.url}/{self.product_list.product_list_id}", update_data)
        result = response.data["result"]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for k, v in update_data.items():
            self.assertEqual(result[k], v)
    
    def test_4_1_api_get_product_column(self):
        """
        GET，獲取所有商品列類別-種類
        :return:
        """
        print("test_4_1_api_get_product_column")
        response = self.client.get(self.url_product_column)
        result = response.data["result"]
        
        self.assertIn(PRODUCT_LIST_DATA["category"], result.keys())
        self.assertIn(PRODUCT_LIST_DATA["type"], result[PRODUCT_LIST_DATA["category"]])
    
    def test_4_2_api_get_product_column(self):
        """
        GET，獲取所有商品列類別-種類-裝備名稱
        :return:
        """
        print("test_4_2_api_get_product_column")
        response = self.client.get(self.url_product_column, {"has_display_name": 1})
        result = response.data["result"]
        
        self.assertIn(PRODUCT_LIST_DATA["category"], result.keys())
        self.assertIn(PRODUCT_LIST_DATA["type"], result[PRODUCT_LIST_DATA["category"]].keys())
        self.assertIn(PRODUCT_LIST_DATA["name"], result[PRODUCT_LIST_DATA["category"]][PRODUCT_LIST_DATA["type"]])
    
    def test_5_api_product_list_delete(self):
        """
        DELETE，刪除並驗證初始化建立的商品列
        :return:
        """
        print("test_5_api_product_list_delete")
        
        response = self.client.delete(f"{self.url}/{self.product_list.product_list_id}")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductTestCase(APITestCase):
    def setUp(self) -> None:
        print("ProductTestCase setUp")
        
        self.client = APIClient()
        self.url = reverse('exchange:product_api-list')
        self.url_sell_product = reverse('exchange:product_api-get-sell-product')
        
        set_user_credentials(self.client)
        user = CustomUser.objects.get(username=USER_DATA["username"])
        self.product_list = ProductList.objects.create(**PRODUCT_LIST_DATA)
        self.product_min = Product.objects.create(
            product_list_id=self.product_list.product_list_id,
            create_by=user,
            **PRODUCT_MIN_DATA
        )
        self.product_max = Product.objects.create(
            product_list_id=self.product_list.product_list_id,
            create_by=user,
            **PRODUCT_MAX_DATA
        )
    
    def test_1_api_product_create(self):
        """
        POST，增加商品
        :return:
        """
        print("test_1_api_product_create")
        
        request = copy.deepcopy(PRODUCT_MIN_DATA)
        request["product_list"] = self.product_list.product_list_id
        response = self.client.post(self.url, request)
        result = response.data["result"]
        
        self.assertEqual(Product.objects.count(), 3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # todo: 增加main_attribute、soul_capability是否等於None的判斷
        for k, v in PRODUCT_MIN_DATA.items():
            if k in ["potential_capability", "spark_capability"]:
                v = v.split(",")
            self.assertEqual(result[k], v)
    
    def test_2_api_product_retrieve(self):
        """
        GET，取得並驗證初始化增加的高低價商品內容
        :return:
        """
        print("test_2_api_product_retrieve")
        self.api_product_retrieve(self.product_min, PRODUCT_MIN_DATA)
        self.api_product_retrieve(self.product_max, PRODUCT_MAX_DATA)
    
    def api_product_retrieve(self, product, product_data):
        response = self.client.get(f"{self.url}/{product.product_id}")
        result = response.data["result"]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for k, v in product_data.items():
            if k in ["potential_capability", "spark_capability"]:
                v = v.split(",")
            self.assertEqual(result[k], v)
    
    def test_3_api_product_list(self):
        """
        GETS，取得並驗證初始化增加的高低價商品內容
        :return:
        """
        print("test_3_api_product_list")
        
        # todo: 增加其他欄位的params
        response = self.client.get(self.url, {"product_list_id": self.product_list.product_list_id})
        results = response.data["result"]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for i, data in enumerate(PRODUCT_DATA.items()):
            for k, v in data[1].items():
                if k in ["potential_capability", "spark_capability"]:
                    v = v.split(",")
                self.assertEqual(results[i][k], v)
    
    def test_4_api_product_partial_update(self):
        """
        PATCH，把min_data -> max_data
        :return:
        """
        print("test_4_api_product_partial_update")
        
        response = self.client.patch(f"{self.url}/{self.product_min.product_id}", PRODUCT_MAX_DATA)
        result = response.data["result"]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for k, v in PRODUCT_MAX_DATA.items():
            # fixme: 這兩個欄位因為是SerializerMethodField所以無法進行修改
            if k in ["potential_capability", "spark_capability"]:
                continue
            self.assertEqual(result[k], v)
    
    def test_4_1_api_product_sell_product(self):
        """
        GET，取得該使用者上架的商品，排除已經下架的商品
        :return:
        """
        print("test_4_1_api_product_sell_product")
        response = self.client.get(self.url_sell_product)
        result = response.data["result"]
        one_week_ago = get_one_week_ago()
        
        self.assertEqual(len(result), len(PRODUCT_DATA))
        for r in result:
            self.assertGreaterEqual(r["update_date"], str(one_week_ago))
    
    def test_5_api_product_delete(self):
        """
        DELETE，刪除並驗證初始化建立的商品
        :return:
        """
        print("test_5_api_product_delete")
        
        response = self.client.delete(f"{self.url}/{self.product_min.product_id}")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
