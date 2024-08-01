from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout


from kb.forms import MDEditorForm, LoginForm
from kb.models import Article

# Create your views here.
class HomeView(View):
    """
    Class based view for the home page.
    """
    def get(self, request):
        context = {
            "published_articles":Article.objects.filter(published=True)
        }
        return render(request, "index.html", context)


class SuggestView(View):
    """
    Class based view for the suggest page.
    """
    def get(self, request):
        context = {
            "form": MDEditorForm()
        }
        return render(request, "suggest.html", context)

    def post(self, request):
        form = MDEditorForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, 'Suggestion successfully saved.')
            return redirect('home')  # Redirect to the home page
        
        context = {
            "form": form
        }
        return render(request, "suggest.html", context)


class LoginView(View):
    """
    Class based view for the login page.
    """
    def get(self, request):
        context = {
            "form": LoginForm()
        }
        return render(request, "login.html", context)

    def post(self, request):
        print("hrer")
        username = request.POST["username"]
        password = request.POST["password"]
        # print(username, password, 'dtals')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            form = LoginForm()
            messages.error(request, 'Invalid email or password.')
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    """
    Class based view for the logout page.
    """
    def get(self, request):
        logout(request)
        return redirect('home')