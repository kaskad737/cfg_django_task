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
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, extend_schema_view
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    UsersListSerializer,
    UserSerializer,
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
            status.HTTP_200_OK: {
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
        tags=['user_registration'],
        summary='User registration',
    ),
)
class UserRegisterView(CreateAPIView):
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
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        tags=['user'],
    ),
    put=extend_schema(
        tags=['user'],
    ),
    patch=extend_schema(
        tags=['user'],
    ),
    delete=extend_schema(
        tags=['user'],
    ),
)
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('pk')
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema_view(
    get=extend_schema(
        tags=['portfolio'],
    ),
    post=extend_schema(
        tags=['portfolio'],
    ),
)
class PortfolioListCreateView(ListCreateAPIView):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        '''
        Get the current user from the request
        Filter portfolios based on portfolios created by the current user,
        to restrict access to non-creators
        '''
        current_user = self.request.user
        if current_user.is_superuser:
            queryset = Portfolio.objects.all().order_by('pk')
        else:
            queryset = Portfolio.objects.filter(
                created_by=current_user).order_by('pk')
        return queryset


@extend_schema_view(
    get=extend_schema(
        tags=['portfolio'],
    ),
    put=extend_schema(
        tags=['portfolio'],
    ),
    patch=extend_schema(
        tags=['portfolio'],
    ),
    delete=extend_schema(
        tags=['portfolio'],
    ),
)
class PortfolioRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''
        Get the current user from the request
        Filter portfolios based on portfolios created by the current user,
        to restrict access to non-creators
        '''
        current_user = self.request.user
        if current_user.is_superuser:
            queryset = Portfolio.objects.all().order_by('pk')
        else:
            queryset = Portfolio.objects.filter(
                created_by=current_user).order_by('pk')
        return queryset


@extend_schema_view(
    get=extend_schema(
        tags=['portfolio'],
        parameters=[PortfolioInvestmentAnalysisSerializer],
        summary='Get portfolio analysis',
        responses={
            status.HTTP_200_OK: {
                'type': 'object',
                'properties': {
                    'average_interest_rate': {'type': 'float', 'description': '', 'example': '100.5'},
                    'nearest_maturity_bond': {'type': 'string', 'description': '', 'example': 'bond_name'},
                    'total_value': {'type': 'string', 'description': '', 'example': '100'},
                    'future_value': {'type': 'string', 'description': '', 'example': '100'},
                },
            },
            status.HTTP_204_NO_CONTENT: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'description': 'Portfolio contains no bonds.',
                        'example': 'Portfolio contains no bonds.'
                    },
                },
            },
            status.HTTP_404_NOT_FOUND: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'description': 'Error message', 'example': 'Not found.'},
                },
            },
        },

    ),
)
class PortfolioInvestmentAnalysisView(GenericAPIView):
    serializer_class = PortfolioInvestmentAnalysisSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        portfolio_pk = self.request.GET.get('portfolio_pk')
        portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
        user = self.request.user
        if (portfolio.created_by == user) or (user.is_superuser):
            data = get_portfolio_analysis(portfolio=portfolio)
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You do not have permission to see analysis of this portfolio.")


@extend_schema_view(
    get=extend_schema(
        tags=['bond'],
        responses={
            status.HTTP_200_OK: BondSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: None,
            status.HTTP_403_FORBIDDEN: None,
        },
    ),
    post=extend_schema(
        tags=['bond'],
        responses={
            status.HTTP_201_CREATED: BondSerializer,
            status.HTTP_400_BAD_REQUEST: None,
            status.HTTP_401_UNAUTHORIZED: None,
            status.HTTP_403_FORBIDDEN: None,
        },
    ),
)
class BondListCreateView(ListCreateAPIView):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''
        Get the current user from the request
        Filter bonds details based on portfolios created by the current
        user, to restrict access to non-creators
        '''
        current_user = self.request.user
        if current_user.is_superuser:
            queryset = Bond.objects.all()
        else:
            queryset = Bond.objects.filter(
                portfolio__created_by=current_user)
        return queryset

    def perform_create(self, serializer):
        current_user = self.request.user
        portfolio_id = self.request.data.get('portfolio', None)
        if portfolio_id:
            portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
            if portfolio.created_by == current_user:
                serializer.save(portfolio=portfolio)
                return
        raise PermissionDenied('You do not have permission to create a bond in this portfolio.')


@extend_schema_view(
    get=extend_schema(
        tags=['bond'],
    ),
    put=extend_schema(
        tags=['bond'],
    ),
    patch=extend_schema(
        tags=['bond'],
    ),
    delete=extend_schema(
        tags=['bond'],
    ),
)
class BondRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = BondSerializer
    queryset = Bond.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        '''
        Get the current user from the request
        Filter bonds details based on portfolios created by the current
        user, to restrict access to non-creators
        '''
        current_user = self.request.user
        if current_user.is_superuser:
            queryset = Bond.objects.all()
        else:
            queryset = Bond.objects.filter(
                portfolio__created_by=current_user)
        return queryset
