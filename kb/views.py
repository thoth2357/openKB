from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from kb.forms import MDEditorForm

# Create your views here.
class HomeView(View):
    """
    Class based view for the home page.
    """
    def get(self, request):
        return render(request, "index.html")


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
