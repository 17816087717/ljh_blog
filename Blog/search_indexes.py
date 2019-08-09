from haystack import indexes
from Blog.models import BlogPost

'''
1、search_indexes.py 命名不要随便写，就是这个格式，如： search_index.py就会报错
2、模块功能：告诉django haystack使用哪些数据建立索引以及如何存放索引。
3、这是 django haystack 的规定。要想对某个 app 下的数据进行全文检索，就要在该 app 下
    创建一个 search_indexes.py 文件，然后创建一个 XXIndex 类（XX 为含有被检索数据的模型，
    如这里的 BlogPost），并且继承 SearchIndex 和 Indexable。
4、参数讲解：【建立数据模板】
    （1）每个索引里面必须有且只能有一个字段为 document=True，这代表 django haystack 和搜索引擎将使用此字段
        的内容作为索引进行检索(primary field)。注意，如果使用一个字段设置了document=True，则一般约定此字段名为
        text，这是在 SearchIndex 类里面一贯的命名
    （2）haystack 提供了use_template=True 在 text 字段中，这样就允许我们使用数据模板去建立搜索引擎索引的文件，
        说得通俗点就是索引里面需要存放一些什么东西
5、对第四点的解读：
    （1）数据模板的作用是对 BlogPost.title、BlogPost.body 这两个字段建立索引，当检索的时候会对这两个字段做全
        文检索匹配，然后将匹配的结果排序后作为搜索结果返回。
    （2）同时在工程文件下的templates下创建对应的text.txt文件，正确路径如下：/search/indexes/Blog/blogpost_text.txt
6、使用python manage.py rebuild_index创建索引，setting中配置的'PATH': os.path.join(BASE_DIR, 'whoosh_index'),表示
    会在根目录下创建索引文件 whoosh_index 文件夹，这个不用自己创建，在创建索引时会自动创建。
'''
class BlogPostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return BlogPost

    def index_queryset(self, using=None):
        return self.get_model().objects.all()