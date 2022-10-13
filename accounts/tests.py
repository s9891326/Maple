from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models import CustomUser
from utils import error_msg

USER_DATA = dict(
    username="eddywang",
    password="eddywang",
    password2="eddywang",
    email="eddy@gmail.com",
    provider=CustomUser.Provider.Null,
    server_name=CustomUser.ServerName.Scania,
    contact=None,  # 只提供在更新(partial_update)下才能正常寫入
)


def set_user_credentials(client):
    """
    使用者登入
    :return:
    """
    response = client.post(reverse("accounts:user_api-list"), USER_DATA, format="json")
    result = response.data["result"]
    if not result:
        raise ValueError("user登入失敗")
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + result["access"])


class UserManagersTests(TestCase):
    def setUp(self) -> None:
        self.User = get_user_model()
        self.username = "eddy"
        self.user_email = "eddy@google.com"
        self.user_password = "eddy"
        
        self.superuser_name = "root"
        self.superuser_email = "root@google.com"
        self.superuser_password = "root_password"
    
    def test_create_user(self):
        user = self.User.objects.create_user(
            username=self.username,
            email=self.user_email,
            password=self.user_password
        )
        self.assertEqual(user.username, self.username)
        self.assertEqual(user.email, self.user_email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        
        with self.assertRaises(TypeError):
            self.User.objects.create_user()
        with self.assertRaises(ValueError):
            self.User.objects.create_user(username='')
    
    def test_create_superuser(self):
        superuser = self.User.objects.create_superuser(
            username=self.superuser_name,
            email=self.superuser_email,
            password=self.superuser_password
        )
        self.assertEqual(superuser.username, self.superuser_name)
        self.assertEqual(superuser.email, self.superuser_email)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        
        with self.assertRaises(ValueError):
            self.User.objects.create_superuser(
                username="test_root",
                email="root@google.com",
                password="root",
                is_superuser=False
            )


class CustomUserTestCase(APITestCase):
    def setUp(self) -> None:
        print("CustomUserTestCase setUp")
        self.client = APIClient()
        self.url = reverse('accounts:user_api-list')
        
        set_user_credentials(self.client)
        self.user_id = CustomUser.objects.get(username=USER_DATA["username"]).id
    
    def test_1_api_custom_user_create(self):
        """
        POST，創建新的使用者，最後塞token進client中
        輸入帳號、密碼字數是否有驗證
        :return:
        """
        print("test_1_api_custom_user_create")
        
        username_too_short_date = dict(
            username="eddy",
            password="eddyeddy",
            password2="eddyeddy",
            email="eddy@gmail.com",
        )
        response = self.client.post(self.url, username_too_short_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data["result"][0])

        password_too_short_date = dict(
            username="eddywang",
            password="eddy",
            password2="eddy",
            email="eddy@gmail.com",
        )
        response = self.client.post(self.url, password_too_short_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data["result"][0])

        password2_is_not_equal_password_date = dict(
            username="eddywang",
            password="eddywang",
            password2="eddywang2",
            email="eddy@gmail.com",
        )
        response = self.client.post(self.url, password2_is_not_equal_password_date)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(error_msg.PASSWORD_NOT_MATCH, response.data["result"][0])
    
    def test_2_api_custom_user_retrieve(self):
        """
        GET，透過token取得該使用者資訊
        :return:
        """
        print("test_2_api_custom_user_retrieve")
        
        response = self.client.get(self.url)
        result = response.data["result"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        for k, v in result.items():
            if k in ["id", "server_name"]:
                continue
            self.assertEqual(v, USER_DATA[k])
    
    def test_3_api_custom_user_partial_update(self):
        """
        PATCH。修改用戶資訊
        :return:
        """
        print("test_3_api_custom_user_partial_update")
        
        update_data = dict(
            server_name=CustomUser.ServerName.Janis,
            contact=[{"method": "line", "explanation": "lineid"}],
        )
        response = self.client.patch(f"{self.url}/{self.user_id}", update_data, format="json")
        result = response.data["result"]
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for k, v in update_data.items():
            if k == "server_name":
                self.assertEqual(result[k], v.label)
            else:
                self.assertEqual(result[k], v)
    
    def test_4_api_custom_user_delete(self):
        """
        DELETE。刪除使用者 => 禁止的403
        :return:
        """
        print("test_4_api_custom_user_delete")
        
        response = self.client.delete(f"{self.url}/{self.user_id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
