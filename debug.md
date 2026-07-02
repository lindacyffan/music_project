# Debug report
## run_crawler.py
### 1. API 请求遭遇拒绝 
#### 返回:

``` bash
{"msg":"服务器忙碌，请稍后再试！","code":-447}
```
#### 原因：请求头缺少 Referer 字段，被服务器识别为非浏览器请求。
#### 解决：在请求头中添加 "Referer": "https://music.163.com/"，模拟从网易云页面发起的请求。

### 2. JSON 解析时报错 `TypeError: 'method' object is not subscriptable`

#### 返回：

```bash
Traceback (most recent call last):
  File "run_crawler.py", line 19, in <module>
    print(data['result']['tracks'][0]['name'])
TypeError: 'method' object is not subscriptable
```

#### 原因：

将 `response.json`（方法本身）赋值给了 `data`，而不是调用方法 `response.json()`。缺少括号，导致 `data` 是一个方法对象，而非解析后的字典。

#### 解决：

将 `data = response.json` 改为 `data = response.json()`。

### 3. 循环只输出前两首歌

#### 现象：

使用 `for i, item in enumerate(data): print(data['result']['tracks'][i]['name'])` 只输出了"海屿你"和"玻璃"。

#### 原因：

`enumerate(data)` 遍历的是字典的顶层键（`result`、`code` 等），而不是歌曲列表 `tracks`。循环次数等于顶层键的数量（2次），所以只取到了前两首歌。


#### 解决：

改为直接遍历歌曲列表：

```python
tracks = data['result']['tracks']
for song in tracks:
    print(song['name'])
```