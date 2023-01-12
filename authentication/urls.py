from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView


from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view, name="login"),
    #path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    #path('activate/<uidb64>/<token>/', activate, name='activate'),
]
