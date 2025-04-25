#xpath解析
'''
from lxml import etree
xml = """ 
    <nav class="navbar">
        <ul>
            <li><a href="#home">主页</a></li>
            <li><a href="#projects">项目</a></li>
            <li><a href="#skills">技能</a></li>
            <li><a href="#contact">联系</a></li>
            <div><li><a href="#contact">海贼</a></li></div>
        </ul>
    </nav>
    """
tree = etree.XML(xml)
result = tree.xpath("/nav/ul/*/li/a/text()")  
# /表示层级关系，第一个/是根节点
# text()拿文本，且得到的是其数据的集合   ['主页', '项目', '技能', '联系']
# "/nav/ul/*/li/a/text()",其中的‘*’表示通配符（但是不能匹配恐）
print(result)
'''
''''''
from lxml import etree

with open(r"c:\Users\67604\Desktop\爬虫\Two\mybadu.html", "r", encoding="utf-8") as f:
    html_content = f.read()

tree = etree.HTML(html_content)
#result = tree.xpath("/html/body/div/div/div/a/text()")
#result = tree.xpath("/html/body/div/div/div[1]/a[1]/text()")
#result = tree.xpath("/html/body/div/div/div/a[@href='//news.baidu.com/']/text()")
#print(result)
div_a_list = tree.xpath("/html/body/div/div/div/a")
#一直获得所排列的结点
i = 0
for a in div_a_list:
    i += 1
    result = a.xpath("./text()")#在div中继续寻找，使用./表示当前结点
    #print(result)
    result2 = a.xpath("./@href")#通过@获得属性值
    #print(result2)
print(tree.xpath('/html/body/div/div/div[1]/a[1]/text()'))