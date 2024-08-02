from django.urls import path
from kb.views import HomeView, SuggestView,LoginView,LogoutView, NewUserView, EditUserView, MyAccountView, UserListView, DeleteUserView, AddArticleView, validate_permalink, ArticleListView,EditArticleView,DeleteArticleView, toggle_publish


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

    # Articles url
    path('articles/add/', AddArticleView.as_view(), name='add_article'),
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<int:pk>/edit/', EditArticleView.as_view(), name='edit_article'),
    path('articles/<int:pk>/delete/', DeleteArticleView.as_view(), name='delete_article'),
    path('articles/<int:pk>/toggle-publish/', toggle_publish, name='toggle_publish'),
    # Misc Urls
    path('validate_permalink/', validate_permalink, name='validate_permalink'),

]
