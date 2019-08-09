from django.contrib import admin
# 下面四个是从模型类中导入的四个模型类：博客文章、分类、标签、评论
from Blog.models import BlogPost
from Blog.models import Category
from Blog.models import Tag
from comments.models import Comment

'''
备注：账户：MYSN，密码：1994218219A
'''
class CategoryAdmin(admin.ModelAdmin):
    '''博客分类的管理员类'''
    list_display = ['id', 'name']


class TagAdmin(admin.ModelAdmin):
    '''博客分类的管理员类'''
    list_display = ['id', 'name']


class PostAdmin(admin.ModelAdmin):
    '''创建博客文章的管理员类'''
    list_display = ['id', 'title', 'created_time', 'modified_time']


class CommentAdmin(admin.ModelAdmin):
    '''创建博客文章的管理员类'''
    list_display = ['id', 'name','email', 'post',  'created_time']



admin.site.register(BlogPost,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tag,TagAdmin)
admin.site.register(Comment,CommentAdmin)

