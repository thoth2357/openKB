from django.urls import path

from kb.views import (AddArticleView, ArticleDetailView, ArticleListView,
                      DeleteArticleView, DeleteUserView, EditArticleView,
                      EditUserView, HomeView, LoginView, LogoutView,
                      MyAccountView, NewUserView,
                      SuggestView, UserListView, toggle_publish,
                      validate_permalink, vote_article, ArticleSettingsView,
                      DisplaySettingsView, StyleSettingsView, WebsiteSettingsView,
                      FileManagementView)

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
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail_by_pk'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),

    # Admin urls
    # path('settings/', SettingsUpdateView.as_view(), name='settings'),
    path('settings/website/', WebsiteSettingsView.as_view(), name='website_settings'),
    path('settings/article/', ArticleSettingsView.as_view(), name='article_settings'),
    path('settings/display/', DisplaySettingsView.as_view(), name='display_settings'),
    path('settings/style/', StyleSettingsView.as_view(), name='style_settings'),


    # Files url
    path('files/', FileManagementView.as_view(), name='file_management'),
    
    # Misc Urls
    path('validate_permalink/', validate_permalink, name='validate_permalink'),
    path('article/<int:pk>/vote/', vote_article, name='article_vote'),

]
