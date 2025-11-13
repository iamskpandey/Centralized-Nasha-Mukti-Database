from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', auth_views.LoginView.as_view(
        template_name='registry/login.html'
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('beneficiary/add/', views.add_beneficiary, name='add_beneficiary'),
    path('beneficiaries/', views.beneficiary_list, name='beneficiary_list'),
    path('beneficiary/<int:pk>/', views.beneficiary_detail, name='beneficiary_detail'),
    path('beneficiary/<int:pk>/edit/', views.edit_beneficiary, name='edit_beneficiary'),
    path('beneficiary/<int:pk>/delete/', views.delete_beneficiary, name='delete_beneficiary'),
    path('beneficiary/<int:pk>/history/', views.intervention_history, name='intervention_history'),
    
    path('intervention/<int:pk>/edit/', views.edit_intervention, name='edit_intervention'),
    path('intervention/<int:pk>/delete/', views.delete_intervention, name='delete_intervention'),

    path('reports/', views.reports_page, name='reports_page'),
]