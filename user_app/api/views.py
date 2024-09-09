
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from user_app.api.serializers import RegistrationSerializer
from user_app import models

# @api_view(['POST'])
# def logout_view(request):
# # if request.method=="POST":
#     #     request.user.auth_token.delete()
#     #     return Response(status=status.HTTP_200_OK)
#
#     if request.user.is_authenticated:
#         try:
#             request.user.auth_token.delete()
#         except Token.DoesNotExist:
#             pass  # Token might not exist, so ignore this error
#         return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
#     else:
#         return Response({"detail": "User is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except:
            return Response({"detail": "Logout failed."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def registration_view(request):
    if request.method=="POST":
        serializer=RegistrationSerializer(data=request.data)

        data={}

        if serializer.is_valid():
            account=serializer.save()

            data['response']="Registration Successfully"
            data['username']=account.username
            data['email']=account.email

            token=Token.objects.get(user=account).key
            data['token']=token
        else:
            data=serializer.errors


        return Response(data,status=status.HTTP_201_CREATED)





