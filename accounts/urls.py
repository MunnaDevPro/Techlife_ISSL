from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_form, name="signup"),
    path("verify/<uidb64>/<token>/", views.verify_email, name="verify-email"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("reset-password/", views.reset_password, name="password-reset"),
    path(
        "reset-password-confirm/<uidb64>/<token>/",
        views.reset_password_confirm,
        name="password_reset_confirm",
    ),
    path("set-new-password/", views.set_new_password, name="new-password"),
    path("user_dashboard/" , views.user_dashboard_view , name= "user_dashboard"),
    path("contact_us/" , views.contact_us_view , name= "contact_us")
]
