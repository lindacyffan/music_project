# DJANGO
``` bash
mysite/
├── manage.py                # 启动、管理项目的命令行工具，不需要修改
├── mysite/                  # 项目配置文件夹
│   ├── __init__.py
│   ├── settings.py          # 项目配置：时区、语言、安装的应用、模板路径等
│   ├── urls.py              # URL路由：告诉Django哪个网址交给哪个视图处理
│   └── wsgi.py              # 部署相关，不需要管
└── musicapp/                # 应用文件夹：你写业务逻辑的地方
    ├── __init__.py
    ├── admin.py             # 后台管理相关，用不上
    ├── apps.py              # 应用配置，用不上
    ├── models.py            # 数据库模型，你用不上（因为用的是CSV）
    ├── tests.py             # 测试，用不上
    ├── views.py             # 视图函数：接收请求，处理数据，返回响应
    └── urls.py              # 应用内部路由（你手动创建的）
```
# · mysite/（项目根目录）：负责管理配置/URL/安全

## ·mysite/ (项目配置文件夹)
### `settings.py`
#### 存放项目配置，我在`Installed_Apps`里添加了`musicapp`让Django知道这个应用的存在。
### `urls.py`
#### 应用级的URL路由表（手动创建的），其中`path('', views.song_list, name='song_list')`，当用户访问`musicapp`对应的根路径时，调用`views.py`的`song_list`函数。
## ·musicapp/ (应用)
### `views.py`
```bash
def song_list(request):
    df = pd.read_csv("C:/Users/53125/Desktop/music_project/data/lyrics_data_all.csv",encoding='utf-8-sig')

    songs = df.to_dict('records')

    paginator = Paginator(songs, 20)
    page_number = request.GET.get('page',1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'musicapp/song_list.html',{'page_obj':page_obj})
```
### ·templates/musicapp/ (应用)
#### ·song_list.html
| page_obj 的属性                | 值（举例）                     |
| ----------------------------- | ------------------------------ |
| page_obj.object_list          | 当前页 20 首歌                 |
| page_obj.number               | 当前页码，比如 1               |
| page_obj.has_previous         | True / False                   |
| page_obj.has_next             | True / False                   |
| page_obj.paginator.num_pages  | 总页数，比如 80                 |
| page_obj.paginator.page_range | 所有页码的列表，比如 [1,2,3,...,80] |
```markdown
# 分页执行流程
songs（全部数据）
    ↓
Paginator(songs, 20)  →  切成每页 20 条
    ↓
request.GET.get('page', 1)  →  用户想看第几页？
    ↓
paginator.get_page(page_number)  →  取出那一页的数据
    ↓
page_obj（包含当前页数据和分页信息）→  传给模板
```
#### 视图函数
