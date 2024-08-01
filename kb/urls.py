from django.urls import path
from kb.views import HomeView, SuggestView,LoginView,LogoutView, NewUserView, EditUserView, MyAccountView, UserListView, DeleteUserView


# urlpatterns
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("suggest/", SuggestView.as_view(), name="suggest"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    
    # users url
    path('users/new/', NewUserView.as_view(), name='new-user'),
    path('users/edit/', UserListView.as_view(), name='edit-users'),
    path('users/<int:pk>/', EditUserView.as_view(), name='edit-user'),
    path('users/myaccount/', MyAccountView.as_view(), name='my-account'),
    path('users/edit/<int:pk>/', EditUserView.as_view(), name='edit-user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
    path('users/my-account/', MyAccountView.as_view(), name='my-account'),

]
