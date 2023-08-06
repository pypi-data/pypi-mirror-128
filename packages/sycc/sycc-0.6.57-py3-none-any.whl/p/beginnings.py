__Author__='神秘的·'
__Project__='虹源三式'
#__version__='定制版'
link='https://pypi.org/project/sycc/#description/'
from time import sleep as dd
from sys import path
path.append('..')
path.append('.')
from .tqdm._tqdm import trange
from random import uniform as float__wait_time
from k.Mac import bs64
from os import popen
from os.path import exists,isfile
import sys as s, time as t
import threading
version=[]
def sycc_ver():
    global ver_str
    try:        
        ver_str=list(popen('pip show sycc').read().splitlines(False))
    except Exception or IndexError as e_test:
        
        if len(list(e_test))>1:
           
           #ver_Flase=False
           __version__='定制版'
    def ver_outside():
        global ver_str
        try:
            ver_str=ver_str[1].split(':')[1].split('.')
        except Exception or IndexError:
            __version__='定制版'
    (threading.Thread(target=ver_outside)).start()
def wf():
    print('\r请稍等,全力加载中')  
    (threading.Thread(target=sycc_ver)).start()
    for i in trange(0,100):
        dd_random=float__wait_time(0.06,0.12)
        dd(0.012)
        dd(dd_random)

    try:
        version.append(ver_str[0])
        dd(0.01)
        version.append(ver_str[1])
        dd(0.01)
        version.append(ver_str[2])
        dd(0.01)
    except Exception:
        print('请耐心等待…')
        if len(version)<=3:
            #ver_Flase = False
            __version__='定制版'
            dd(2)
        else:
            try:
                if len(version)==3:
                    del version[2]
                    del version[1]
                    del version[0]
                elif len(version)==2:
                    del version[1]
                    del version[0]    
                elif len(version)==1:
                    del version[0]            
                version.append(ver_str[0])
                dd(0.01)
                version.append(ver_str[1])
                dd(0.01)
                version.append(ver_str[2])
                dd(0.01)
            except Exception:
                __version__='定制版' 
    if  len(version)>=3:
        print('\ndone!')
        dd(0.02)
    else:
        for dd_tips in ['请  ','耐心 ','等待 ','几秒 ',',  ','子线程','未运行','完成 ']:#空格凑位
            print(dd_tips,end='\r',flush=True)
            dd(0.5)
        if dd_tips=='完成 ':
            print('    ',end='\r')
            dd(0.01)
        if len(version)==3:
            print('\ndone!')
            dd(0.02)
def A():
    try:
        __version__=version[0]+'.'+version[1]+'.'+version[2]
    except Exception:
        __version__='定制版'
    print('\n\033[1;5;44m作者:' ,__Author__,'\033[0m')  
    print('\033[1;5;44m版本:',__version__,'\033[0m')
    print('\033[1;5;44mname:',__Project__,'\033[0m')
    print('\033[1;5;44mDescribe_README:',link,'\033[0m')
    dd(0.3)
    #print('\033[1;44m支持\033[0m','输入运算符(选项除外),\033[0m(使用英文字符)')
    dd(0.02)
pai2='π' #下面要用到，提前放上来 
def dw():#单位
    print('请自行换算单位并保持单位一致')
from math import pi as pai1
def aboutpi():
    print('''
    请选择π的值
    1.输入1,π为3.14
    2.输入2,π为''',pai1,
    '''
    3.输入3,保留π(π不换成数字)
    4.输入4,π自定义大小(大于3 ,小于3.2)
    其他选项:
    5.输入5,切换模式
    6.输入不是1~5中的数,直接退出''')
#wf();A()#test

    