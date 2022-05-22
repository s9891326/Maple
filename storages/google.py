import json
import os

from django_gcloud_storage import DjangoGCloudStorage, storage
from django.conf import settings
from google.oauth2 import service_account


class CustomGCS(DjangoGCloudStorage):
    def __init__(self, project=None, bucket=None, credentials=None):
        self._client = None
        self._bucket = None
        
        if bucket is not None:
            self.bucket_name = bucket
        else:
            self.bucket_name = settings.GCS_BUCKET
        
        if credentials is not None:
            self.credentials = credentials
        else:
            # 從Django setting中取得參數GCS_CREDENTAILS作為認證依據
            # 這個參數可以是JSON檔案路徑，或者是JSON字串
            self.credentials = settings.GCS_CREDENTIALS
        
        if project is not None:
            self.project_name = project
        else:
            self.project_name = settings.GCS_PROJECT
        
        self.bucket_subdir = ''
    
    @property
    def client(self):
        if not self._client:
            # 認證的過程中，若認證字串是一個檔案的話
            # 則嘗試用JSON檔案認證的方式
            # 這是原本的認證方式
            if os.path.isfile(self.credentials):
                self._client = storage.Client.from_service_account_json(
                    self.credentials, project=self.project_name)
            else:
                # 若認證自傳不是檔案路徑的話，嘗試用json解成dictionary
                # 接著用oauth2client.service_account中的API嘗試認證
                cred_dict = json.loads(self.credentials)
                credentials = service_account.Credentials.from_service_account_info(cred_dict)
                self._client = storage.Client(project=self.project_name, credentials=credentials)
        return self._client
