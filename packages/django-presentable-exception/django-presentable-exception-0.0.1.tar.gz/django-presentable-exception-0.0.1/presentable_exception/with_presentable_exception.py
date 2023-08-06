
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from presentable_exception.presentable_exception import PresentableClientException, PresentableServerException
from presentable_exception import PresentableException

class WithPresentableException:

    def handle_exception(self, exc):
        if not isinstance(exc, PresentableException):
            return super().handle_exception(exc)

        if isinstance(exc, PresentableClientException):
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        # TODO: do some logging here

        return Response(exc.log_entry, status=status_code)
