from django.urls import path
from .views import RegisterView, LoginView, UserDetailView, OrganizationListView, OrganizationDetailView, OrganizationCreateView, AddUserToOrganizationView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/users/<str:userId>/', UserDetailView.as_view(), name='user-detail'),
    path('api/organisations/', OrganizationListView.as_view(), name='organization-list'),
    path('api/organisations/<str:orgId>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('api/organisations/', OrganizationCreateView.as_view(), name='organization-create'),
    path('api/organisations/<str:orgId>/users/', AddUserToOrganizationView.as_view(), name='add-user-to-organization'),

]
