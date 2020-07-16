from django.shortcuts import render, get_object_or_404
import re

# Create your views here.
import markdown

from .models import Category, Post, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.views.generic import ListView, DetailView, View
from comments.forms import CommentForm
from pure_pagination.mixins import PaginationMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q


class HomeView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 6

class BlogView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'post_list'
    paginate_by = 6
    #http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']

class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 6


# 记得在顶部导入 DetailView
class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            #'markdown.extensions.extra',
            #'markdown.extensions.codehilite',
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ])
        md.convert(post.body)
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list
        })
        return context

class SiteMapView(ListView):
    model = Post
    template_name = 'blog/sitemap.html'
    context_object_name = 'post_list'

class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 6

    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return super(ArchivesView, self).get_queryset().filter(created_time__year=year, created_time__month=month)

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

class CategoryView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 6

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

def about(request):
    return render(request, 'blog/about.html')

def index(request, tag):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index' + str(tag) +'.html',  context={'post_list': post_list})

def blog_category(request, tag):
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/blog-category' + str(tag) +'.html')

class BlogCategoryView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/category1.html'
    context_object_name = 'post_list'
    paginate_by = 6
    #http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    def get(self, request, tag=None, *args, **kwargs):
        if tag:
            self.template_name = 'blog/blog-category' + str(tag) + '.html'
        return super(BlogCategoryView, self).get(request)


def single_blog(request, tag):
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/single-blog' + str(tag) +'.html')

def archives(request, tag):
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/archives' + str(tag) +'.html')

def authors(request):
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/authors.html')

def contact(request):
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/contact.html')

def coming_soon(request):
    #post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/coming-soon.html')

def udf_404(request):
    return render(request, '404.html')

def search(request):
    q = request.GET.get('q')

    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})

class SearchView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 6

    def get_queryset(self):
        q = self.request.GET.get('q')
        return super(SearchView, self).get_queryset().filter(Q(title__icontains=q) | Q(body__icontains=q))

class IncreaseLikesView(View):
    def post(self, request, *args, **kwargs):
        article = ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes += 1
        article.save()
        return HttpResponse('success')
