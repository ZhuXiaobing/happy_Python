# 直接引入moduleStudy模块
import python基础与备注.moduleStudy as moduleStudy

print(moduleStudy.a)
print(moduleStudy.b)

# 引入moduleStudy模块的子模块
from python基础与备注.moduleStudy import importee

p = importee.Person("zhuxiaobing", 28)
print(p)
# 不建议直接访问
print(p._name)
importee.sayHello(p)
