from django.shortcuts import render, get_object_or_404, redirect
from Blog.models import BlogPost

from .models import Comment
from comments.forms import CommentForm


# 注意：从URL获取的参数，不要随便瞎改，直接使用URL传过来的参数变量就好
def blog_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)  # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # commit=False 利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment.post = post  # 将评论和被评论的文章关联起来。
            comment.save()  # 最终将评论数据保存进数据库，调用模型实例的 save 方法

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)  # ???是不是可以改成'Blog:detail'，未成功
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            comment_list = post.comment_set.all()
            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)


'''
下面是作者对上面的 post.comment_set.all()作出的解析：
    post.comment_set.all() 也等价于 Comment.objects.filter(post=post)，即根据 post 来过滤该 post 下的全部评论。
    但既然我们已经有了一个 Post 模型的实例 post（它对应的是 Post 在数据库中的一条记录），那么获取和 post 关联的评论
    列表有一个简单方法，即调用它的 xxx_set 属性来获取一个类似于 objects 的模型管理器，然后调用其 all 方法来返回这个 post 关联
    的全部评论。 其中 xxx_set 中的 xxx 为关联模型的类名（小写）。
    例如 获取cate分类下的所有博客：Post.objects.filter(category=cate) 也可以等价写为 cate.post_set.all()。

'''