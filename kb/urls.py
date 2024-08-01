from django.urls import path
from kb.views import HomeView, SuggestView

# urlpatterns
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("suggest/", SuggestView.as_view(), name="suggest"),
]
