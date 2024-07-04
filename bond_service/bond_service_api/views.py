from django.contrib.auth.models import User
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UsersListSerializer,
    PortfolioSerializer,
    BondSerializer,
    PortfolioInvestmentAnalysisSerializer,
)
from .models import Portfolio, Bond
from .utils import get_portfolio_analysis
from django.shortcuts import get_object_or_404


@extend_schema_view(
    post=extend_schema(
        tags=['token'],
        summary='Get JWT Token',
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


@extend_schema_view(
    post=extend_schema(
        tags=['token'],
        summary='Get JWT Token pair',
    ),
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=['token'],
        summary='Verify JWT Token',
    ),
)
class CustomTokenVerifyView(TokenVerifyView):
    permission_classes = [AllowAny]


@extend_schema_view(
    post=extend_schema(
        tags=['user'],
        summary='User registration',
    ),
)
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


@extend_schema_view(
    get=extend_schema(
        tags=['user'],
        summary='List all users',
    ),
)
class UsersListView(ListAPIView):
    serializer_class = UsersListSerializer
    queryset = User.objects.all().order_by('pk')


@extend_schema_view(
    get=extend_schema(
        tags=['portfolio'],
        parameters=[PortfolioSerializer],
    ),
    post=extend_schema(
        tags=['portfolio'],
        parameters=[PortfolioSerializer],
    ),
)
class PortfolioListCreateView(ListCreateAPIView):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()


@extend_schema_view(
    post=extend_schema(
        tags=['portfolio'],
        parameters=[PortfolioInvestmentAnalysisSerializer],
        summary='Get portfolio analysis',
        responses={
            200: {
                "type": "object",
                "properties": {
                    "average_interest_rate": {"type": "float", "description": "Link to file", "example": "1.23"},
                    "nearest_maturity_bond": {"type": "string", "description": "Link to file"},
                    "total_value": {"type": "string", "description": "Link to file", "example": "100"},
                    "future_value": {"type": "string", "description": "Link to file", "example": "100"},
                },
            },
            404: {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "description": "Error message", "example": "Portfolio not found"},
                },
            },
        },

    ),
)
class PortfolioInvestmentAnalysisView(GenericAPIView):
    serializer_class = PortfolioInvestmentAnalysisSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        portfolio_pk = self.request.data.get('portfolio_pk')
        portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
        data = get_portfolio_analysis(portfolio=portfolio)
        return Response(data=data, status=status.HTTP_200_OK)


@extend_schema_view(
    get=extend_schema(
        tags=['bond'],
        parameters=[BondSerializer],
    ),
    post=extend_schema(
        tags=['bond'],
        parameters=[BondSerializer],
    ),
)
class ListCreateBondView(ListCreateAPIView):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()
    # permission_classes = [IsAuthenticated]


@extend_schema_view(
    get=extend_schema(
        tags=['bond'],
        parameters=[BondSerializer],
    ),
    put=extend_schema(
        tags=['bond'],
        parameters=[BondSerializer],
    ),
    patch=extend_schema(
        tags=['bond'],
        parameters=[BondSerializer],
    ),
    delete=extend_schema(
        tags=['bond'],
        parameters=[BondSerializer],
    ),
)
class RetrieveUpdateDestroyBondView(RetrieveUpdateDestroyAPIView):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()
    # permission_classes = [IsAuthenticated]
