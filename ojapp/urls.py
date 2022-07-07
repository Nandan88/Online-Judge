from django.contrib import admin
from django.urls import path
from ojapp import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path("",views.index,name='home'),
    path("login",LoginView.as_view(),name="login_url"),
    path("register",views.register,name="register"),
    path("logout",LogoutView.as_view(),name="logout"),
    path("dashboard",views.dashboard,name="dashboard"),
    # path("problems",views.problems,name='problem_detail')
    path("dashboard/<int:problem_id>/",views.problemDetail,name="problem_detail"),
    path("dashboard/<int:problem_id>/submit",views.submitProblem,name="submit"),
    path("leaderboard",views.leaderboard,name="leaderboard"),
    # path("verdict/<int:solution_id>/",views.verdict,name="verdict"),
    path("problem1",views.problem1,name='problem1')
]
