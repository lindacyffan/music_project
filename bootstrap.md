# BootStrap

## 1.表格相关
`table class="table table-striped table-hover"`
`table`:`Bootstrap 的表格基础样式，去掉默认边框，增加间距`
`table-striped`:`奇数行和偶数行颜色不同（斑马纹），便于阅读`
`table-hover`:`鼠标悬停时行背景变色，提示可点击`
### 表头
`<thead class="table-dark">`
`表头背景色为深色，文字白色，突出显示`
`<td> class="center` `文字居中`
`<td colspan="3" class="text-center">`
`这个单元格横跨 3 列（用于“暂无数据”时占满整行）`
### 分页相关
`<ul class="pagination justify-content-center">`
`pagination`:`Bootstrap 分页组件的容器，让里面的项横向排列`
`justify-content-center`	`让分页组件居中显示`
`<li class="page-item">`:`分页的每一项（一个按钮或数字）`
`<li class="page-item active">`:`表示当前所在页，按钮会高亮显示（蓝色背景）`
`<li class="page-item disabled">`:`按钮不可点击，颜色变灰（用于首页/上一页在边界时）`
`<a class="page-link" href="...">`
`分页按钮的样式，去掉下划线，加圆角和间距`
### 卡片相关——搜索结果页
`<div class="row">`:`栅格行，里面的列会水平排列`
`<div class="col-md-3 mb-3">`
`	在中等屏幕（电脑）上占 3/12 = 25% 宽度，一行放 4 个,下边距 1rem，让卡片之间有空隙`
`<div class="card">`
`卡片容器，带边框、圆角、阴影`
`<img class="card-img-top" style="height: 150px; object-fit: cover;">`
card-img-top	| 卡片顶部的图片，紧贴卡片上边缘
height: 150px;| 	固定图片高度
object-fit: cover;	| 图片裁剪填满，不变形