"""
sys 模块：提供了一些变量和函数，可以获取到python解析器信息，也可以修改解析器信息。
"""

import sys

# 通过pprint （pretty print）模块的pprint()方法，来对打印的数据做简单的格式化
import pprint
# 通过pprint （pretty print）模块的pprint()方法，来对打印的数据做简单的格式化
import pprint
import sys

pprint.pprint(sys.argv)
# 获取当前程序引入的所有模块的字典
pprint.pprint(sys.modules)

# sys.path：指定的是”模块的搜索路径“
pprint.pprint(sys.path)

# sys.platform：指定当前python的运行平台。
pprint.pprint(sys.platform)

# 退出当前程序，这个语句后面的语句不会执行。
sys.exit()
