from rest_framework import status
from ..translations.translate import get_translated_text as _


class ResultMessageStructure:
    def __init__(self, code: int, message: str, is_success_result: bool, http_code=status.HTTP_200_OK):
        self.code, self.message, self.is_success_result, self.http_code = code, message, is_success_result, http_code


class ResultMessages:
    GET_SUCCESSFULLY = ResultMessageStructure(2000, _('Done'), True, status.HTTP_200_OK)
    SUBMIT_SUCCESSFULLY = ResultMessageStructure(2001, _('Submit'), True, status.HTTP_201_CREATED)
    PAGE_NOT_FOUND = ResultMessageStructure(4004, _('Page Not Found'), False, status.HTTP_404_NOT_FOUND)
    UNDEFINED_ERROR = ResultMessageStructure(5000, _('Undefined Error.'), False, status.HTTP_500_INTERNAL_SERVER_ERROR)
    ENTERED_DATA_NOT_VALID = ResultMessageStructure(4006, _('Entered Data Is Not Valid'), False,
                                                    status.HTTP_406_NOT_ACCEPTABLE)
    BAD_REQUEST = ResultMessageStructure(4000, _('Bad Request'), False, status.HTTP_400_BAD_REQUEST)
    UNDEFINED_METHOD = ResultMessageStructure(4005, _('Invalid Method'), False, status.HTTP_405_METHOD_NOT_ALLOWED)
    INVALID_CONTENT_TYPE = ResultMessageStructure(4015, _('Invalid Content-Type'), False,
                                                  status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    AUTHENTICATION_FAIL = ResultMessageStructure(4001, _('Unauthorized'), False, status.HTTP_401_UNAUTHORIZED)
    FORBIDDEN = ResultMessageStructure(4003, _('Forbidden'), False, status.HTTP_403_FORBIDDEN)
