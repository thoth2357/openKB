from django.urls import path
from kb.views import HomeView, SuggestView,LoginView,LogoutView

# urlpatterns
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("suggest/", SuggestView.as_view(), name="suggest"),
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),

]
