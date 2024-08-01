from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, authenticate, logout, get_user_model


from kb.forms import MDEditorForm, LoginForm, CustomUserCreationForm, EditUserForm,MyAccountForm
from kb.models import Article, CustomUser

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
    



from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class NewUserView(PermissionRequiredMixin, CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = 'users/new_user.html'
    permission_required = 'auth.add_user'
    success_url = reverse_lazy('edit-users')
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        user = form.save(commit=False)
        user.save()
        return super().form_valid(form)

class UserListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    context_object_name = 'users'
    template_name = 'users/edit_users.html'
    permission_required = 'auth.view_user'

class EditUserView(UpdateView):
    model = get_user_model()
    form_class = EditUserForm
    # fields = ['username', 'email', 'is_superuser']  # Customize as needed
    template_name = 'users/edit_user.html'
    success_url = reverse_lazy('edit-users')
    permission_required = 'auth.change_user'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.get_object()
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data['password1']
        if password:
            user.set_password(password)
        user.save()
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('auth.change_user') and self.get_object().pk != request.user.pk:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class DeleteUserView(DeleteView):
    model = get_user_model()
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('user-list')

class MyAccountView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = MyAccountForm
    template_name = 'users/my_account.html'
    success_url = reverse_lazy('home')  # Redirect to home or any other page

    def get_object(self, queryset=None):
        return self.request.user  # Returns the logged-in user object

    def form_valid(self, form):
        messages.success(self.request, "Account updated successfully.")
        return super().form_valid(form)