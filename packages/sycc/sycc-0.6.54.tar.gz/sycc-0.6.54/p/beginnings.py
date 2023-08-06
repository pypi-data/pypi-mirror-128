__Author__='神秘的·'
__Project__='虹源三式'
#__version__='定制版'
link='https://pypi.org/project/sycc/#description/'
from time import sleep as dd
from sys import path
from .tqdm._tqdm import trange
from random import uniform as float__wait_time
path.append('..')
from k.Mac import bs64
from os import popen
from os.path import exists,isfile


import sys as s, time as t
import threading
version=[]
#def A():#作者&运算符相关
#global ver_str
def sycc_ver():
    global ver_str
    ver_str=list(popen('pip show sycc').read().splitlines(False))
    def ver_outside():
        global ver_str
        ver_str=ver_str[1].split(':')[1].split('.')
    (threading.Thread(target=ver_outside)).start()
def wf():
    print('\r请稍等,全力加载中')  
    (threading.Thread(target=sycc_ver)).start()
    for i in trange(0,100):
        #s.stdout.write("██")
        dd_random=float__wait_time(0.08,0.13)
        dd(0.012)
        dd(dd_random)

    try:
        version.append(ver_str[0])
        version.append(ver_str[1])
        version.append(ver_str[2])
    except NameError:
        print('请耐心等待…')
        dd(2.5)
        try:
            del version[2]
            del version[1]
            del version[0]
        except Exception:
            try:
                del version[1]
                del version[0]
            except Exception:
                try:
                    del version[0]
                except:
                    global ver2
                    ver2='定制版'
        version.append(ver_str[0])
        version.append(ver_str[1])
        version.append(ver_str[2])
        
    if  len(version)>=3:
        print('\ndone!')
        dd(0.02)
    else:
        print('请等待几秒,子线程未运行完成',flush=True)
        dd(2)
        if len(version)>=3:
            print('\ndone!')
            dd(0.02)
        else:
            print('就再等几秒…')
            dd(3)
def A():
    try:
        __version__=version[0]+'.'+version[1]+'.'+version[2]
    except Exception:
        __version__=ver2
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

    