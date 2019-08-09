from django import template
from django.db.models.aggregates import Count
from Blog.models import BlogPost, Category, Tag

register = template.Library()


@register.simple_tag
def get_recent_posts(num=5):
    '''自定义最新模板标签函数'''
    return BlogPost.objects.all().order_by('-created_time')[:num]


@register.simple_tag
def archives():
    '''归档模板标签函数，对date函数的参数说明如下
    created_time：按照博客的创建时间进行归档
    month：归档精度是月
    DESC：降序排列
    '''
    return BlogPost.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    '''分类模板标签函数，
    说明：annotate方法类似于上面的all方法，会返回数据库的全部category的记录
    然后根据给出的参数进行筛选出想要的结果，blogpost是与category相关联的外键模型参数名，所以获取与blogpost相关的所有分类的记录信息
    筛选掉数量为0的数据
    '''
    return Category.objects.annotate(num_posts=Count('blogpost')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    return Tag.objects.annotate(num_posts=Count('blogpost')).filter(num_posts__gt=0)
