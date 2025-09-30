from decimal import *
from math import pi
from typing import List
from typing import Union
# from typing import Tuple
def get_num(obj:Union[str,Decimal])->int:
    """
    输入：obj:字符串、Decimal
    输出：有效数字位数num，int类型
    如果obj内无dot则会报错
    """
    obj=str(obj)
    obj = list(obj)
    obj.remove('.')
    #i指向obj从左到右第一个非0数
    i=0
    while obj[i]=='0':
        i+=1
    obj=obj[i:]
    return len(obj)

def carry_bit(lst,index):
    """
    输入：
    lst1：一个去掉dot与头部0的非幂列表(其中存字符串)
    index：指向非幂列表可能会出现进位的元素
    输出：只有隐输出完成由index开始的进位链的lst
    lst1是lst的副本
    """
    #第二类基本情况
    if index<0:
        lst.insert(0,'1')
        return
    #递归情况
    if int(lst[index])>=10:
        lst[index]=str(int(lst[index])-10)
        if index==0:
            carry_bit(lst, index - 1)
        else:
            lst[index-1]=str(int(lst[index-1])+1)
            carry_bit(lst, index - 1)
    else:
        return

def return_num(number:Union[str,Decimal],num:int)->tuple:
    """
    输入：
    number:字符串或Decimal，表示要处理的数字
    num：要保留的有效数字位数 int类型
    输出：
    一个元组(number,exponent) number是保留了num位有效数字位数的字符串，exponent是10的指数
    """
    number=list(str(number))
    e_sign=False
    if 'E' not in number and 'e' not in number :
        fsi=0
        while number[fsi]=='0' or number[fsi]=='.':
            fsi+=1
        di=0
        while number[di]!='.':
            di+=1
        #求指数
        if di>fsi:
            exponent=di-fsi-1
        else:
            exponent=di-fsi
    else:
        e_sign=True
        if 'E' in number:
            e_index=number.index('E')
            e_lst=number[e_index+1:]
            e_lst=''.join(e_lst)
            exponent=int(e_lst)
        else:
            e_index=number.index('e')
            e_lst = number[e_index + 1:]
            e_lst = ''.join(e_lst)
            exponent = int(e_lst)
    #处理非幂字符串
    #c指针指向有效数字终止处
    number.remove('.')
    if e_sign is True:
        if 'e' in number:
            e_index=number.index('e')
            del number[e_index:]
        else:
            e_index = number.index('E')
            del number[e_index:]    #更新fsi
    fsi = 0
    while number[fsi] == '0' or number[fsi] == '.':
        fsi += 1
    c=fsi+num-1
    number.extend(['0']*(c-fsi+3))
    if int(number[c+1])<=4:
        pass
    elif int(number[c+1])>=6:
        number[c]=str(int(number[c])+1)
        carry_bit(number,c)
    else:
        number1=number[c+2:]
        sign=0
        for item in number1:
            if item=='0':
                pass
            else:
                sign+=1
        if sign==0:
            if int(number[c])%2==0:
                pass
            else:
                number[c]=str(int(number[c])+1)
                carry_bit(number,c)
        else:
            number[c]=str(int(number[c])+1)
            carry_bit(number,c)
    number=number[fsi:c+1]
    number.insert(1,'.')
    number=''.join(number)
    f=(number,exponent)
    return f

# #开始计算体积
# V_lst=[]
# for _ in range(7):
#     st1,st2=map(str,input().split())
#     L,D=Decimal(st1),Decimal(st2)
#     mini=min(get_num(L),get_num(D))
#     pi=Decimal(str(round(float(pi),20)))
#     pi_set=return_num(pi,mini+1)
#     mini=min(get_num(L),get_num(D),len(pi_set[0])-1)
#     V=pow(D,Decimal('2'))*L*Decimal(pi_set[0])*pow(Decimal('10'),Decimal(str(pi_set[1])))/Decimal('4')
#     V_set=return_num(V,mini)
#     V=f'{V_set[0]}e({V_set[1]})'
#     V_lst.append(V)
# V_lst=' '.join(map(str,V_lst))
# print(V_lst)

def standard_deviation(lst:List[Union[str,Decimal]],num:int,average:Decimal)->Decimal:
    #计算lst元素的个数n
    n=len(lst)
    #计算要保留的有效数字位数num
    lst=list(map(Decimal,lst))
    #求平方和
    su=Decimal('0')
    for item in lst:
        su+=pow(item-average,Decimal('2'))
    #求最终结果
    S_item=pow(su/Decimal(f'{n-1}'),Decimal('0.5'))
    f:tuple=return_num(S_item,num)
    return f'{f[0]}e({f[1]})'
#
# v=[4210.000,
# 4213.000,
# 4197.000,
# 4201.000,
# 4200.000,
# 4200.000,
# 4204.000]
# v=list(map(str,v))
# print(standard_deviation(v,4,Decimal(4204)))
#
