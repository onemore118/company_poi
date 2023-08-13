## 项目说明
通过高德web api key 获取公司地址，然后通过folium绘制可交互地图

实例如下

![demo](https://raw.githubusercontent.com/onemore118/company_poi/ec1ee7f63f511a5ebed00dfb9a89bc79eca388c2/assets/demo.png)

## 启动说明
1. 新建一个.env在根目录
2. 新加如下几行数据
```shell
GAODE_KEY=申请的高德web api key
CHINESE_FONT_PATH=本地中文字体的路径 如'C:\\Windows\\Fonts\\simsun.ttc'
```

## 经纬度科普
https://blog.csdn.net/diandianxiyu_geek/article/details/126713942

## 备注
后来发现企查查其实有可拖拽查看企业的功能，而且筛选维度更丰富，效果更好