from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('create-card/', views.create_card_view, name='create_card'),
    path('delete-card/<int:card_id>/', views.delete_card_view, name='delete_card'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]