from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
from users.models import User


class Signupview(APIView):
    #회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


#로그인
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserView(APIView):
    # 사용자 정보
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #수정
    def put(self, request, id):
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "수정완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": f"{serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    def delete(self, request, id):
        user = User.objects.get(id=id)
        if request.user == user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다", status=status.HTTP_403_FORBIDDEN)



