from bs4 import BeautifulSoup

html = """
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""
# 读取HTML文件
soup = BeautifulSoup(html,"html.parser")
# 提取出title的页面元素
print(soup.title)
# 提取出title的值
print(soup.title.string)

# 提取出第一个p的元素对象
print(soup.p)
# 提取出第一个P的id属性的值
print(soup.p['id'])
# 提取出第一个P的标签的值
print(soup.p.string)
# 提取出所有的P的元素对象
print(soup.find_all('p'))

# 将所有a标签中的href属性值和对应的标签值依次打印
print(soup.find_all('a'))

for s in soup.find_all('a'):
    print("href = {}, 对应的标签值为：{}".format(s['href'],s.string))