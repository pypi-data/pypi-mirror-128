"""
写一个常用的包，用来解决平时的各种问题
"""
#!/usr/bin/env python
# coding: utf-8
import numpy as np
from statsmodels.stats.power import NormalIndPower


def ipr(old_num,new_num):
        return ('提升绝对值{0},相对值{1}%'.format(round((new_num-old_num),2),round((new_num-old_num)/old_num*100,2)))
    
def ABSample():
    print("请输入实验主要指标当前值 ___ %（比如点击率，留存率）")
    u=input()
    u=float(u)/100
    print("请输入最小可以观测的提升比例___% （相对值）")
    r=input()
    r=float(r)/100
    zpower = NormalIndPower()
    effect_size =u*r/np.sqrt(u*(1-u))
    return(zpower.solve_power(
       effect_size=effect_size,
       nobs1=None,
       alpha=0.05,
       power=0.8,
       ratio=1.0,
       alternative='two-sided'
            ))              
    