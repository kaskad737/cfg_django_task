from django.urls import path

from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    RegisterView,
    UsersListView,
    PortfolioListCreateView,
    PortfolioInvestmentAnalysisView,
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    path('user_register/', RegisterView.as_view(), name='user_register'),
    path('users/', UsersListView.as_view(), name='users'),
    path("portfolio/", PortfolioListCreateView.as_view(), name='portfolio'),
    path('portfolio_investment_analysis/', PortfolioInvestmentAnalysisView.as_view(),
         name='portfolio_investment_analysis'),
]
