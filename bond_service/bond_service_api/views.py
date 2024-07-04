# from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
# , OpenApiParameter, OpenApiExample
# from drf_spectacular.types import OpenApiTypes
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UsersListSerializer,
)


@extend_schema_view(
    post=extend_schema(
        tags=['tokens'],
        summary='Refresh JWT Token',
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'refresh': {'type': 'string'},
                    'access': {'type': 'string'},
                },
            },
        },
    ),
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UsersListView(ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all().order_by('pk')


class PortfolioInvestmentAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={}, status=status.HTTP_200_OK)
