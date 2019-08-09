from django.db import models
from django.urls import reverse
import  markdown
from django.utils.html import strip_tags


class Category(models.Model):
    """博客分类"""
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'category'
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Tag(models.Model):
    """博客标签"""
    name = models.CharField(max_length=100)
    class Meta:
        db_table = 'tag'
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class BlogPost(models.Model):
    """自定义文章类：标题，正文，创建时间，修改时间，摘要，分类，标签，阅读量【再加一个评论？】"""
    title = models.CharField(max_length=100)
    author=models.CharField('作者',max_length=16)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)  # 文章摘要，可为空
    category = models.ForeignKey(Category, on_delete=True)  # ForeignKey表示1对多（多个博文对应1个category）
    tags = models.ManyToManyField(Tag, blank=True)  # 多个博文对应多个标签
    views = models.PositiveIntegerField(default=0)  # 阅读量
    class Meta:
        ordering = ['-created_time']  # 在定义模型类的时候就将博客文章默认按照发布时间的逆序排列，需要说明的是ordering
                                    # 可以跟多个参数，表示的意思是如果按照第一个参数排序结果是一样的话就按照第二个参数排列
        db_table = 'blogpost'
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.title

    def increase_views(self):
        '''真实记录博客的阅读量'''
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        '''自动生成文章摘要'''
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(BlogPost, self).save(*args, **kwargs)

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        return reverse('Blog:detail', kwargs={'id': self.id})





'''
一、数据库的构建(M） 
首先，分析一个博客系统的功能： 
（1）一个博客可以有多个标签（多对多） 
（2）一个博客可以有多条评论(一对多） 
（3）一个博客只可以有一个类别（多对一） 
接下来，分析关系的属性： 
博客：标题，作者，内容，发布时间，分类（外键），标签（多对多）等 
标签：标签名 
类别：分类名 
评论：作者，博客（外键），邮箱，内容，发布时间等。
--------------------- 
原文：https://blog.csdn.net/a18852867035/article/details/66475879 
'''
