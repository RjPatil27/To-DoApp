from django.urls import path
# from . import views
from .views import TaskList,TaskDetail,TaskCreate, TaskUpdate, TaskDelete, LogIn, RegisterPage
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.tasklist, name='tasks'),    # Base path
    path('login/',LogIn.as_view(),name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name="task-delete"),
]