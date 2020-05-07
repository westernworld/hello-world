# 面向携程旅游信息的网络爬虫
本部分介绍爬虫需预安装库和运行步骤。本设计面向携程欧洲城市景点的旅游信息进行爬取，能实现绝大部分景点的爬取，对于小部分页面结构与主流网页不一致的无法面面俱到，但针对大部分网页能满足用户的需求。
## 依赖
* tkinter # GUI界面
* requests,BeautifulSoup4，urllib # 爬虫
* wordcloud,jieba # 生成词云
* PIL # 图像显示
## 运行步骤
step1：<br>
创建picture文件夹存放爬取图片和词云图片，注意.py文件中保存路径应和创建路径保持一致<br>
![不存在](https://github.com/westernworld/hello-world/raw/master/img-folder/路径.png)
step2：<br>
下载simhei.ttf字体，安装到C:\Windows\Fonts，用于词云的汉化（系统可能默认自带）<br>
step3：<br>
运行爬虫.py文件，选择对应国家城市确定，成功爬取结果如图所示<br>
![不存在](https://github.com/westernworld/hello-world/raw/master/img-folder/结果.png)
step4：<br>
如需选择其他景点，重复step3操作<br>
