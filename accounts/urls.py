from django.urls import path
from . import views


urlpatterns = [
    path("auth/signup", views.SignupUser.as_view(), name="signup"),
    path("auth/login", views.LoginUser.as_view(), name="login"),
    path("auth/profile", views.CurrentUser.as_view(), name="user"),
    path("enroll/new", views.NewEnroll.as_view(), name="enrollment"),
    path("enrollments", views.MyEnrolls.as_view(), name="myenrollments"),
    path("enroll/update/<int:id>", views.UpdateEnroll.as_view())
]
