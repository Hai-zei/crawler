import re
'''
# findall()方法:匹配字符串所有的符合正则表达式的子串，并以列表的形式返回
lit = re.findall("\d+","我的电话号码是：10068")
print(lit)
print("======================================")
# finditer()方法:匹配字符串所有的符合正则表达式的子串，并以迭代器的形式返回
it = re.finditer("\d+","我的电话号码是：10068")
#从迭代器当中获取每一个匹配的对象使用grouP()方法
for i in it:
    print(i.group())
    # search()方法:匹配字符串第一个符合正则表达式的子串，返回的是mathc对象,需要使用。group()方法
    s = re.search(r"(\d+)", "我的电话号码是：10068")
    print(s.group())  # 10068
#match()方法:匹配字符串开头符合正则表达式的子串，返回的是mathc对象,需要使用。group()方法
s = re.match(r"(\d+)", "10068我的电话号码是：10068")
print(s.group())  # 10068
'''
# #预加载正则表达式
# obj = re.compile(r"\d+")

# ret  = obj.finditer("我的电话号码是：10068")
# for i in ret:
#     print(i.group())  # 10068

# ret  = obj.findall("gdfghdgsgfsfgs04555545")
# print(ret)
s = """
<div class='item'><span id='100'>中国联通</span></div>
<div class='ite'><span id='10'>还在</span></div>
<div class='it'><span id='0'>团弄</span></div>
<div class='i'><span id='1044'>海</span></div>
"""
#(?P<分组名称>正则) 可以单独从正则匹配当中进一步提取内容
obj = re.compile(r"<div class='.*?'><span id='\d+'>(?P<op>.*?)</span></div>",re.S)  #re.S表示匹配换行符

result = obj.finditer(s)
for it in result:
    print(it.group("op"))
