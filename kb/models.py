from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from mdeditor.fields import MDTextField


# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=255)
    content = MDTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    keywords = models.CharField(max_length=255)
    published = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)  # Added field for tracking views
    votes = models.IntegerField(default=0)
    permalink = models.SlugField(max_length=255, default='', null=True)
    seo_title = models.CharField(max_length=255, default='')
    seo_description = models.TextField(default='')
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True)
    featured = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        if self.permalink:
            return reverse('article_detail', kwargs={'slug': self.permalink})
        else:
            return reverse('article_detail_by_pk', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title
    
    


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 
    
    def __str__(self):
        return self.email
    

class WebsiteSettings(models.Model):
    website_title = models.CharField(max_length=255, blank=True, default='openKB')
    website_description = models.TextField(blank=True, default='openKB is an Open Source Django Markdown based knowledge base/FAQ/Wiki app.')
    show_website_logo = models.BooleanField(default=True)
    website_context_base_url = models.URLField(blank=True, default='http://127.0.0.1:4444/openkb/')
    allow_api_access = models.BooleanField(default=False)
    api_access_token = models.CharField(max_length=255, blank=True)
    password_protect = models.BooleanField(default=False)
    index_article_body = models.BooleanField(default=False)
    select_theme = models.CharField(max_length=255, blank=True)
    select_language = models.CharField(max_length=10, default='en', choices=[('en', 'English')])
    show_logon_link = models.BooleanField(default=True)
    date_format = models.CharField(max_length=50, default='d/m/Y H:iA')
    article_suggestions_allowed = models.BooleanField(default=True)
    google_analytics_code = models.TextField(blank=True)

    def __str__(self):
        return "Site Settings"


class ArticleSettings(models.Model):
    allow_voting = models.BooleanField(default=True, verbose_name='Allow voting')
    show_article_meta = models.BooleanField(default=True, verbose_name='Show article meta data')
    show_author_email = models.BooleanField(default=True, verbose_name='Show author email')
    article_links_open_new_page = models.BooleanField(default=True, verbose_name='Article links open new page')
    add_header_anchors = models.BooleanField(default=False, verbose_name='Add header anchors')
    enable_editor_spellchecker = models.BooleanField(default=True, verbose_name='Enable editor spellchecker')
    allow_article_versioning = models.BooleanField(default=False, verbose_name='Allow article versioning')
    allow_mermaid = models.BooleanField(default=False, verbose_name='Allow Mermaid')
    allow_mathjax = models.BooleanField(default=False, verbose_name='Allow MathJax')

    def __str__(self):
        return "Article Settings"


class DisplaySettings(models.Model):
    number_of_top_articles = models.IntegerField(default=10)
    show_published_date = models.BooleanField(default=True)
    show_view_count = models.BooleanField(default=True)
    update_view_count_when_logged_in = models.BooleanField(default=True)
    show_featured_articles = models.BooleanField(default=True)
    show_featured_articles_when_viewing_article = models.BooleanField(default=False)
    featured_article_count = models.IntegerField(default=4)
    
    def __str__(self):
        return "Display Settings"



class StyleSettings(models.Model):
    header_background_color = models.CharField(max_length=7, blank=True, default='#2D3E50')
    header_text_color = models.CharField(max_length=7, blank=True, default='#FFFFFF')
    footer_background_color = models.CharField(max_length=7, blank=True, default='#343a40')
    footer_text_color = models.CharField(max_length=7, blank=True, default='#ffffff')
    button_background_color = models.CharField(max_length=7, blank=True, default='#007bff')
    button_text_color = models.CharField(max_length=7, blank=True, default='#7a3838')
    link_color = models.CharField(max_length=7, blank=True, default='#0f000c')
    page_text_color = models.CharField(max_length=7, blank=True, default='#212529')
    page_font = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "Style Settings"
