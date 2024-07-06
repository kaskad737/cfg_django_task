from rest_framework import permissions
from .models import Portfolio


class IsOwnerOrSuperUser(permissions.BasePermission):
    '''
    Custom permission to only allow owners of a portfolio or superusers to view it.
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Check if the user is the creator of the object
        return obj.created_by == request.user


class IsOwnerOfPortfolioOrSuperUser(permissions.BasePermission):
    '''
    Custom permission to only allow owners of a portfolio or superusers to access the bonds.
    '''

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        # Check if the user is the creator of the related portfolio
        return obj.portfolio.created_by == request.user


class IsOwnerOfPortfolioInvestmentAnalysisOrSuperUser(permissions.BasePermission):
    '''
    Custom permission to only allow owners of a portfolio or superusers to access it.
    '''

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        portfolio_pk = request.data.get('portfolio_pk')
        if not portfolio_pk:
            return False

        try:
            portfolio = Portfolio.objects.get(pk=portfolio_pk)
        except Portfolio.DoesNotExist:
            return False

        # Check if the user is the creator of the portfolio or a superuser
        return request.user.is_superuser or portfolio.created_by == request.user
