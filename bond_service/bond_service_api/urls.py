from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    UserRegisterView,
    UsersListView,
    UserRetrieveUpdateDestroyView,
    PortfolioListCreateView,
    PortfolioRetrieveUpdateDestroyView,
    PortfolioInvestmentAnalysisView,
    BondListCreateView,
    BondRetrieveUpdateDestroyView
)

app_name = 'bond_service_api'

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('user_register/', UserRegisterView.as_view(), name='user_register'),
    path('users/', UsersListView.as_view(), name='users'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user_details'),
    path('portfolio/', PortfolioListCreateView.as_view(), name='portfolio'),
    path('portfolio/<int:pk>/', PortfolioRetrieveUpdateDestroyView.as_view(), name='portfolio_details'),
    path('portfolio_investment_analysis/', PortfolioInvestmentAnalysisView.as_view(),
         name='portfolio_investment_analysis'),
    path('bonds/', BondListCreateView.as_view(), name='bond'),
    path('bonds/<int:pk>/', BondRetrieveUpdateDestroyView.as_view(), name='bond_details'),
]
