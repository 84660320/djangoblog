from django import template

from ..models import Post, Category, Tag
from django.db.models import Count
from django.db.models.functions import ExtractYear, ExtractMonth

register = template.Library()

@register.inclusion_tag('blog/inclusions/_recent_posts.html', takes_context=True)
def show_recent_posts(context, num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog/inclusions/_archives.html', takes_context=True)
def show_archives(context):
    query = "select title, id, to_char(created_time, 'YYYYMM') as post_month, created_time from blog_post order by created_time desc"
    name_map = {'title': 'title', 'pk': 'id', 'post_month':'post_month', 'created_time':'created_time'}
    posts = Post.objects.raw(query, translations=name_map)

    #date_list = Post.objects.annotate(year=ExtractYear('created_time'), month=ExtractMonth('created_time')) \
    #    .values('year', 'month').order_by('year', 'month').annotate(num_posts=Count('id'))

    #print(date_list)

    query = "select id, to_char(created_time, 'YYYYMM') as post_month from blog_post"
    name_map = {'pk':'id', 'post_month': 'post_month'}
    rows = Post.objects.raw(query, translations=name_map)

    date_list = []
    for row in rows:
        if row.post_month not in date_list:
            date_list.append(row.post_month)
    print(date_list)

    return {
        #'date_list': Post.objects.dates('created_time', 'month', order='DESC'),
        'posts': posts,
        'post_months': date_list
    }

@register.inclusion_tag('blog/inclusions/_categories.html', takes_context=True)
def show_categories(context):
    category_list = Category.objects.annotate(count=Count('post')).filter(count__gt=0)
    #query = "select c.id, c.name, count(1) from blog_post p left join blog_category c on p.category_id=c.id group by c.id, c.name"
    #name_map = {'name': 'name', 'pk': 'id', 'count':'count'}
    #objs = Post.objects.raw(query, translations=name_map)

    return {
        'category_list': category_list,
    #return {
    #    'category_list':  Post.objects.raw(query, translations=name_map),
    }

@register.inclusion_tag('blog/inclusions/_tags.html', takes_context=True)
def show_tags(context):
    #return {
    #    'tag_list': Tag.objects.all(),
    #}
    tag_list = Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    return {
        'tag_list': tag_list,
    }

@register.inclusion_tag('blog/inclusions/_our_pages.html', takes_context=True)
def show_our_pages(context):
    return {}

@register.inclusion_tag('blog/inclusions/_widget_area.html', takes_context=True)
def show_widget_area(context):
    return {}

@register.inclusion_tag('blog/inclusions/_advertise.html', takes_context=True)
def show_advertise(context):
    return {}

@register.inclusion_tag('blog/inclusions/_instagram.html', takes_context=True)
def show_instagram(context):
    return {}

@register.inclusion_tag('blog/inclusions/_author.html', takes_context=True)
def show_author(context):
    return {}

@register.inclusion_tag('blog/inclusions/_search.html', takes_context=True)
def show_search(context):
    return {}
