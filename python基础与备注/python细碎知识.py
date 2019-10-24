"""
此模块记录python细碎知识
"""
# note1: python中变量为弱类型，编译前无法获取变量类型，所以不支持自增，自减操作。
a = 1
a += 1
# a ++

# note2: python不支持三目运算符(xx ? yy : zz)，可以如下方式替代
b = a if a > 1 else a - 1

# 为什么说Python没有真正的多线程。因为python臭名昭著的GIL(全局解释器锁)的存在。
