"""
os：对操作系统进行操作的模块。
"""
import os
import pprint

pprint.pprint(os)
# os.environ：获取系统环境变量
pprint.pprint(os.environ)
pprint.pprint(os.environ['path'])
# os.system：执行操作系统命令
pprint.pprint(os.system("dir"))
