from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import CreateUserSerializer,MyTokenObtainPairSerializer

class CreateUserAPIView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        serializer=CreateUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    queryset = ''