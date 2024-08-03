import json

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, FormView)

from kb.forms import (ArticleForm, ArticleSettingsForm, CustomUserCreationForm,
                      EditUserForm, LoginForm, MDEditorForm, MyAccountForm,
                      WebsiteSettingsForm,DisplaySettingsForm, StyleSettingsForm)
from kb.models import Article, ArticleSettings, Settings

# Create your views here.

def validate_permalink(request):
    permalink = request.GET.get('permalink', None)
    data = {
        'is_taken': Article.objects.filter(permalink=permalink).exists()
    }
    return JsonResponse(data)


@csrf_exempt
def vote_article(request, pk):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            article = Article.objects.get(pk=pk)
            if data['isPositive']:
                article.votes += 1
            else:
                article.votes -= 1
            article.save()
            return JsonResponse({'votes': article.votes})
        except Article.DoesNotExist:
            return JsonResponse({'error': 'Article not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


@require_POST
@csrf_exempt  # Only use csrf_exempt if you are handling CSRF token in another way for AJAX calls
@login_required
def toggle_publish(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        article.published = not article.published
        article.save()
        return JsonResponse({'status': 'success', 'published': article.published})
    except Article.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Article not found'}, status=404)
    
class HomeView(View):
    """
    Class based view for the home page.
    """
    def get(self, request):
        context = {
            "published_articles":Article.objects.filter(published=True),
            "featured_articles": Article.objects.filter(featured=True)
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


class AddArticleView(SuccessMessageMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/add_article.html'
    success_url = reverse_lazy('article_list')  # Adjust the redirect URL as needed
    success_message = "Article added successfully!"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Adjust the published status based on the status field if necessary
        self.object.published = form.cleaned_data['status'] == 'published'
        self.object.author = self.request.user
        self.object.save()
        messages.success(self.request, "New article added successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        # Additional handling for when the form is not valid
        print("got here o00", form.errors)
        return super().form_invalid(form)


class ArticleListView(ListView):
    model = Article
    template_name = 'articles/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_value = self.request.GET.get('filter', '')

        # Adding order by to sort articles by the most recent
        queryset = queryset.order_by('-updated')  # Replace 'updated' with 'created' if that's your field

        if filter_value:
            queryset = queryset.filter(title__icontains=filter_value)

        return queryset

class EditArticleView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'articles/edit_article.html'
    context_object_name = 'article'

    def get_success_url(self):
        return reverse_lazy('edit_article', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        # Set the article's published state based on the status field
        self.object.published = form.cleaned_data['status'] == 'published'
        self.object.save()
        messages.success(self.request, "Article updated successfully!")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Re-render the form with errors
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))
    

class DeleteArticleView(DeleteView):
    model = Article
    template_name = 'articles/confirm_delete.html'
    context_object_name = 'article'
    success_url = reverse_lazy('article_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Article deleted successfully!")
        return super().delete(request, *args, **kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        # Enhanced to use 'pk' or 'slug' from URL kwargs
        queryset = queryset or self.get_queryset()
        if 'slug' in self.kwargs:
            # Fetch by permalink if 'slug' is in kwargs
            obj = get_object_or_404(queryset, permalink=self.kwargs['slug'])
        elif 'pk' in self.kwargs:
            # Fetch by primary key if 'pk' is in kwargs
            obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        else:
            # If neither 'pk' nor 'slug', raise Http404
            raise Http404("No Article matches the given query.")
        

        # Increment the view count on successful retrieval
        obj.view_count += 1
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['absolute_url'] = self.request.build_absolute_uri()
        context['is_article_detail'] = True  # Add this line

        # Add article settings to context
        settings = ArticleSettings.objects.first()  # Assuming only one settings object exists
        context['settings'] = settings
        
        return context


class SettingsUpdateView(UpdateView):
    model = Settings
    form_class = WebsiteSettingsForm
    template_name = 'admin/settings.html'
    success_url = reverse_lazy('settings')  # Redirect after POST

    def get_object(self, queryset=None):
        # This ensures we always work with a single settings instance.
        return Settings.objects.first() or Settings()

    def form_valid(self, form):
        # You can add any logic after the form is saved here.
        response = super().form_valid(form)
        # Example: Set a success message
        messages.success(self.request, "Settings updated successfully.")
        return response


class ArticleSettingsView(UpdateView):
    model = ArticleSettings
    template_name = 'settings/article_settings.html'
    form_class = ArticleSettingsForm
    success_url = '/settings/article/'
   
    
    def get_object(self, queryset=None):
        # This ensures we always work with a single settings instance.
        return ArticleSettings.objects.first() or ArticleSettings()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings_instance = ArticleSettings.objects.first()  # Ensure you handle case where no settings exist yet
        context['active_tab'] = 'article'

        return context

    def form_valid(self, form):
        # Assuming there's only one settings object, or creating a new one if none exist
        settings = ArticleSettings.objects.first()
        if not settings:
            settings = ArticleSettings()
        for field in form.cleaned_data:
            setattr(settings, field, form.cleaned_data[field])
        settings.save()
        return super().form_valid(form)


class WebsiteSettingsView(FormView):
    template_name = 'settings/website_settings.html'
    form_class = WebsiteSettingsForm
    success_url = '/settings/website/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'website'
        return context

# class ArticleSettingsView(UpdateView):
#     template_name = 'settings/article_settings.html'
#     form_class = ArticleSettingsForm
#     success_url = '/settings/article/'
    
#     def form_valid(self, form):
#         print("form", form.cleaned_data)
    
#     def form_invalid(self, form):
#         print("form", form.errors)
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['active_tab'] = 'article'
#         return context

class DisplaySettingsView(FormView):
    template_name = 'settings/display_settings.html'
    form_class = DisplaySettingsForm
    success_url = '/settings/display/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'display'
        return context

class StyleSettingsView(FormView):
    template_name = 'settings/style_settings.html'
    form_class = StyleSettingsForm
    success_url = '/settings/style/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_tab'] = 'style'
        return context
