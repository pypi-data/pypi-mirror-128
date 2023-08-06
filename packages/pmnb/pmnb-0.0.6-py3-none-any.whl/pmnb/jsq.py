"""
写一个常用的包，用来解决平时的各种问题
"""
#!/usr/bin/env python
# coding: utf-8
import numpy as np
from statsmodels.stats.power import NormalIndPower

#提升多少ipr

def ipr(old_num,new_num):
        print ('{0} 相比{1}:  提升绝对值{2},  相对值{3}%'.format(new_num,old_num,round((new_num-old_num),2),round((new_num-old_num)/old_num*100,2)))

#AB样本量计算ABSample
def ABSample():
    print("请输入实验主要指标当前值 _？？_ %（比如点击率，留存率等，一般都是率或者占比）")
    u=input()
    u=float(u)/100
    print("请输入最小可以观测的提升比例_？_% （就是最少提升多少你觉得才ok，相对值,取绝对值）")
    r=input()
    r=float(r)/100
    zpower = NormalIndPower()
    effect_size =u*r/np.sqrt(u*(1-u))
    res=(zpower.solve_power(
       effect_size=effect_size,
       nobs1=None,
       alpha=0.05,
       power=0.8,
       ratio=1.0,
       alternative='two-sided'
            ))
    print('******* 您的AB实验，实验组需要的用户量为：{0}人 ******'.format(int(res)))
                   
    