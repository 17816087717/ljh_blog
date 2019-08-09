from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from Blog.models import BlogPost,Category,Tag
from django.http import Http404
import markdown
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from comments.forms import CommentForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # 内置分页模块
from django.db.models import Q  # Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑。
# 进行归类整理的时候，在主页index和详情页detail中标题下的分类、发布时间、【作者、评论量、阅读量】进行URL指向，【】内的没有完成，有待完善，创建新的视图函数和分类函数

def index(request):
    '''显示首页'''
    post_list = BlogPost.objects.all().order_by('-created_time')
    p = Paginator(post_list, 2)  # 每一页的容量为2
    page = request.GET.get('page')
    try:
        pageshow = p.page(page)
    except PageNotAnInteger:
        # 如果用户请求的页码号不是整数，显示第一页
        pageshow = p.page(1)
    except EmptyPage:
        # 如果用户请求的页码号超过了最大页码号，显示最后一页
        pageshow = p.page(p.num_pages)

    context ={
        'post_list':post_list,
        'pageshow':pageshow
    }
    return render(request,'index.html',context)


def detail(request,id):
    post = get_object_or_404(BlogPost,id=id)
    post.increase_views()  # 阅读量+1
    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',  # 提供很多扩展
        'markdown.extensions.codehilite',  # 语法高亮扩展
        TocExtension(slugify=slugify), # 自动生成目录
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc
    form = CommentForm()
    comment_list = post.comment_set.all()  # 获取当前博客的所有评论数据
    context = {
        'post': post,
        'form':form,
        'comment_list':comment_list
    }
    return render(request,'detail.html',context)


def archives(request, year, month):
    '''归档视图函数，按照归档日期显示该归档下的所有博客文章'''
    post_list = BlogPost.objects.filter(created_time__year=year,created_time__month=month).order_by('-created_time')
    context = {
        'post_list': post_list
    }
    print(post_list)
    return render(request, 'index.html', context)


def category(request, id):
    '''分类视图函数，根据ID参数查找对应的分类属性，根据分类属性查找所有的博客'''
    cate = get_object_or_404(Category, id=id)
    post_list = BlogPost.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'index.html', context={'post_list': post_list})


def tags(request, id):
    '''标签云视图函数，根据ID参数查找对应的标签属性，根据标签属性查找所有的博客'''
    tag = get_object_or_404(Tag, id=id)
    tag_list = BlogPost.objects.filter(tags=tag).order_by('-created_time')
    return render(request, 'index.html', context={'post_list': tag_list})

