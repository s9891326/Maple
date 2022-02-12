from enum import Enum


class StatusMessage(Enum):
    HTTP_200_OK = "Ok"
    HTTP_201_CREATED_REGISTER = "User successfully registered!"
    HTTP_204_NO_CONTENT = "No Content"
    HTTP_400_BAD_REQUEST_SERIALIZABLE = "Not serializable"
    HTTP_400_BAD_VERIFY_TIME = "Verification time expired"
    HTTP_400_BAD_VERIFY_CODE = "Verification code error"
    HTTP_400_BAD_FORM_VALID = "Form valid error"
    HTTP_401_UNAUTHORIZED = "No active account found with the given credentials"
