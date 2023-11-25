from django.urls import path

from cabinet.views import *

urlpatterns = [
    path('', HomeView.as_view(template_name="home.html"), name="home"),
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(template_name="register.html"), name="register"),
    path('application/create/', ApplicationCreateView.as_view(template_name="application_create.html"),
         name="create_application"),
    path('profile/', ProfileView.as_view(template_name="profile.html"), name="profile"),
    path("profile/filter/", FilterProfileView.as_view(template_name="profile.html"), name='profile-filter'),
    path('application/delete/<int:pk>', ApplicationDeleteView.as_view(template_name="application_delete.html"),
         name="application_delete"),
    path('application/delete/confirm/<int:pk>',
         ApplicationDeleteConfirmView.as_view(template_name="application_delete.html"),
         name="application_delete_confirm"),
    path('applications/list/', ApplicationListView.as_view(template_name="applications_list.html"),
         name="applications_list"),
    path('application/done/change/<int:pk>/', ApplicationDoneChangeStatusView.as_view(
        template_name="application_done_change_status.html"), name="application_done_change_status"),
    path('application/work/change/<int:pk>/', ApplicationWorkChangeStatusView.as_view(
        template_name="application_work_change_status.html"), name="application_work_change_status"),
    path('categories/list/', CategoryListView.as_view(template_name="categories_list.html"), name="categories_list"),
    path('category/create/', CategoryCreateView.as_view(template_name="category_create.html"), name="create_category"),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name="category_delete"),
]