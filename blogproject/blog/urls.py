from django.conf.urls import url
from django.urls import path

from . import views
from blog.feeds import AllPostsRssFeed

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'index', views.HomeView.as_view(), name='home'),
    url(r'home', views.HomeView.as_view(), name='home'),
    url(r'blog', views.BlogView.as_view(), name='blog'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    path('tags/<int:pk>/', views.tag, name='tag'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'sitemap', views.SiteMapView.as_view(), name='sitemap'),
    #url(r'^archive/<int:year>/<int:month>/$', views.ArchivesView.as_view(), name='archives'),
    #url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^about$', views.about, name='about'),
    url(r'^search$', views.SearchView.as_view(), name='search'),
    path(r'contact', views.contact, name='contact'),
]

"""
url(r'^single/(?P<pk>[0-9]+)/$', views.SingleView.as_view(), name='blog_single'),
url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.ArchivesView.as_view(), name='archives'),
#url(r'^archives/<int:year>/<int:month>/$', views.ArchivesView.as_view(), name='archives'),
url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),

url(r'^photo$', views.photo, name='photo'),
url(r'^blog$', views.BlogView.as_view(), name='blog'),
#url(r'^$', views.IndexView.as_view(), name='index1'),
url(r'^index$', views.IndexView.as_view(), name='index2'),
url(r'^about$', views.about, name='about'),
#url(r'^post/(?P<pk>[0-9]+)/$', views.detail, name='detail'),
#path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
#path('categories/<int:pk>/', views.category, name='category'),
path('tags/<int:pk>/', views.tag, name='tag'),
path('index/<int:tag>/', views.IndexView.as_view(), name='index'),
#path('blog_category/<int:tag>/', views.blog_category, name='blog_category'),
path('blog_category/<int:tag>/', views.BlogCategoryView.as_view(), name='blog_category'),
path('single_blog/<int:tag>/', views.single_blog, name='single_blog'),
path('archives/<int:tag>/', views.archives, name='archives'),
path('authors', views.authors, name='authors'),
path('contact', views.contact, name='contact'),
path('coming-soon', views.coming_soon, name='coming_soon'),
path('404', views.udf_404, name='404'),
path('rss', AllPostsRssFeed(), name='rss'),
#path('search/', views.search, name='search'),
path('search/', views.SearchView.as_view(), name='search'),
"""
