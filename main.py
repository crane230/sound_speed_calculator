import streamlit as st
import pandas as pd
from streamlit import session_state
from decimal import Decimal
from physicalDataProcessing import significant_digit_caculator as cac


#精度处理思路：除了最终答案，其余的数据尽量使用Decimal保持精度

#使用f_table建立频率表格，使用l_table建立l表格
if 'f_table' not in session_state:
    st.session_state.f_table=pd.DataFrame(
        {
            '次数':['f(KHz)'],
            '1':[''],
            '2': [''],
            '3': [''],
            '4': [''],
            '5': [''],
            '平均值': ['']
        }
    )
if 'l_table' not in session_state:
    st.session_state.l_table=pd.DataFrame(
        {
            'l1':[''],
            'l2': [''],
            'l3': [''],
            'l4': [''],
            'l5': [''],
            'l6': [''],
            'l7': [''],
            'l8': [''],
            'l9': [''],
            'l10': [''],
            'l11': [''],
            'l12': ['']
        }
    )
    st.session_state.iscalculated=False


st.title('1.原始数据记录')
st.header('声速测定数据记录')
st.write('平均值可填可不填')

if st.session_state.iscalculated is False:
    edited_f_table=st.data_editor(
        st.session_state.f_table,
        key='f_table_editor'
    )
    st.session_state.f_table_editor_name=edited_f_table
    edited_l_table=st.data_editor(
        st.session_state.l_table,
        key='l_table_editor'
    )
    st.session_state.l_table_editor_name = edited_l_table
else:
    st.dataframe(st.session_state.f_table)
    st.dataframe(st.session_state.l_table)
st.divider()
Button=st.button('数据输入完毕，开始计算')

if Button is True:
    try:
        st.markdown(r"# 2.用逐差法处理相位法数据，测得波长 $\lambda$ 和 $f_0$")
        #对l的差值需要进行精度处理，简单四则运算，不用调用get_num，有效数字位数是5
        print(type(st.session_state.l_table_editor_name['l7']))
        l7_l1 = Decimal(st.session_state.l_table_editor_name['l7'].iloc[0])-Decimal(st.session_state.l_table_editor_name['l1'].iloc[0])
        l8_l2 = Decimal(st.session_state.l_table_editor_name['l8'].iloc[0])-Decimal(st.session_state.l_table_editor_name['l2'].iloc[0])
        l9_l3 = Decimal(st.session_state.l_table_editor_name['l9'].iloc[0]) - Decimal(st.session_state.l_table_editor_name['l3'].iloc[0])
        l10_l4 = Decimal(st.session_state.l_table_editor_name['l10'].iloc[0]) - Decimal(st.session_state.l_table_editor_name['l4'].iloc[0])
        l11_l5 = Decimal(st.session_state.l_table_editor_name['l11'].iloc[0]) - Decimal(st.session_state.l_table_editor_name['l5'].iloc[0])
        l12_l6 = Decimal(st.session_state.l_table_editor_name['l12'].iloc[0]) - Decimal(st.session_state.l_table_editor_name['l6'].iloc[0])
        #此时A系列出现有效数字位数冗余
        A1=l7_l1/Decimal('3')
        A2=l8_l2/Decimal('3')
        A3=l9_l3/Decimal('3')
        A4=l10_l4/Decimal('3')
        A5=l11_l5/Decimal('3')
        A6=l12_l6/Decimal('3')
        A_list=[A1,A2,A3,A4,A5,A6]

        A_ave=Decimal('0')
        for item in A_list:
            A_ave+=item
        #获取一个具有较冗余精度的Decimal对象A_ave
        A_ave=A_ave/6

        S_A=Decimal('0')
        for item in A_list:
            S_A+=pow(A_ave-item,2)
        S_A=(S_A/5).sqrt()

        A_lower=A_ave-S_A
        A_upper=A_ave+S_A



        #在显示结果之前对目标数据进行格式化处理，获得数据的格式化版本。数据的格式化版本与原始数据相互独立。
        #其中li_li系列有效数字位数正确，可以直接字符串化然后嵌入文本
        #但是A系列需要进行进一步的有效数字处理
        A1_format=cac.return_num(A1,4)
        A2_format=cac.return_num(A2,4)
        A3_format=cac.return_num(A3,4)
        A4_format=cac.return_num(A4,4)
        A5_format=cac.return_num(A5,4)
        A6_format=cac.return_num(A6,4)
        st.latex(r"\Delta l_{7-1} = | l_7 - l_1 | = 3 \lambda = %s \qquad\qquad \lambda = %s" %(l7_l1,Decimal(A1_format[0]+'e'+str(A1_format[1]))))
        st.latex(r"\Delta l_{8-2} = | l_8 - l_2 | = 3 \lambda = %s \qquad\qquad \lambda = %s" %(l8_l2,Decimal(A2_format[0]+'e'+str(A2_format[1]))))
        st.latex(r"\Delta l_{9-3} = | l_9 - l_3 | = 3 \lambda = %s \qquad\qquad \lambda = %s" %(l9_l3,Decimal(A3_format[0]+'e'+str(A3_format[1]))))
        st.latex(r"\Delta l_{10-4} = | l_{10} - l_4 | = 3 \lambda = %s \qquad\qquad \lambda = %s" %(l10_l4,Decimal(A4_format[0]+'e'+str(A4_format[1]))))
        st.latex(r"\Delta l_{11-5} = | l_{11} - l_5 | = 3 \lambda = %s \qquad\qquad \lambda = %s" %(l11_l5,Decimal(A5_format[0]+'e'+str(A5_format[1]))))
        st.latex(r"\Delta l_{12-6} = | l_{12} - l_6 | = 3 \lambda = %s \qquad\qquad \lambda = %s" %(l12_l6,Decimal(A6_format[0]+'e'+str(A6_format[1]))))

        st.divider()

        A_lower_format=cac.return_num(A_lower,4)
        A_upper_format=cac.return_num(A_upper,4)
        st.latex(r"\overline \lambda = \frac{1}{6} \sum_{i=1}^{6} \lambda _{i} = %.2f \qquad\qquad S_{\lambda} = \sqrt{\frac{\sum ( \lambda _{i} - \overline \lambda )^2}{6-1}} = %.2f "%(A_ave,S_A))
        st.latex(r"\lambda = \overline \lambda \pm S_{\lambda} = %s 或 %s"%(Decimal(A_lower_format[0]+'e'+str(A_lower_format[1])),Decimal(A_upper_format[0]+'e'+str(A_upper_format[1]))))

        st.divider()

        #f系列有效数字位数均正确，无需get_num处理
        f1=Decimal(st.session_state.f_table_editor_name['1'].iloc[0])
        f2=Decimal(st.session_state.f_table_editor_name['2'].iloc[0])
        f3=Decimal(st.session_state.f_table_editor_name['3'].iloc[0])
        f4=Decimal(st.session_state.f_table_editor_name['4'].iloc[0])
        f5=Decimal(st.session_state.f_table_editor_name['5'].iloc[0])
        f_lst=[f1,f2,f3,f4,f5]

        f_ave=Decimal('0')
        for item in f_lst:
            f_ave+=item
        #获得具有冗余有效数字位数的f_ave
        f_ave:Decimal=Decimal(f_ave/5)

        S_f:Decimal=Decimal('0')
        for item in f_lst:
            S_f+=pow(f_ave-item,Decimal('2'))
        #获得具有冗余有效数字位数的S_f
        S_f:Decimal=pow(S_f/4,Decimal('0.5'))

        f_lower=f_ave-S_f
        f_upper=f_ave+S_f

        f_ave_format=cac.return_num(f_ave,5)
        S_f_format=cac.return_num(S_f,5)
        f_lower_format=cac.return_num(f_lower,5)
        f_upper_format=cac.return_num(f_upper,5)
        st.latex(r"\overline f_{0} = \frac{1}{5} \sum_{i=1}^{5} f_{0i} = %s \qquad\qquad S_{f_{0}} = \sqrt{\frac{\sum (f_{i0} - \overline f_{0})^2}{5-1}} = %s"%(Decimal(f_ave_format[0]+'e'+str(f_ave_format[1])),Decimal(S_f_format[0]+'e'+str(S_f_format[1]))))
        st.latex(r"f_{0} = \overline f_{0} \pm S_{f_{0}} = %s 或 %s"%(Decimal(f_lower_format[0]+'e'+str(f_lower_format[1])),Decimal(f_upper_format[0]+'e'+str(f_upper_format[1]))))

        st.header('测量声波波速结果：')

        #获得冗余的各数据
        v_ave=A_ave*f_ave
        E_v=pow(pow(S_A/A_ave,2)+pow(S_f/f_ave,2),Decimal('0.5'))
        S_v=E_v*v_ave
        v_lower=v_ave-S_v
        v_upper=v_ave+S_v

        #进行上述5个数据的格式化处理,其中S_v不需要进行格式化处理，因为它不用输出
        v_ave_format=cac.return_num(v_ave,4)
        E_v_format=cac.return_num(E_v,4)
        v_lower_format=cac.return_num(v_lower,4)
        v_upper_format=cac.return_num(v_upper,4)
        st.latex(r"\overline v = \overline \lambda \cdot \overline f_{0} = %s"%Decimal(v_ave_format[0]+'e'+str(v_ave_format[1])))
        st.latex(r"E_{v} = \frac{S_{v}}{\overline v} = \sqrt{(\frac{S_{\lambda}}{\overline \lambda})^2 + (\frac{S_{f_{0}}}{\overline f_0})^2} = %s"%Decimal(E_v_format[0]+'e'+str(E_v_format[1])))
        st.latex(r"v = \overline v \pm S_{v} = %s 或 %s"%(Decimal(v_lower_format[0]+'e'+str(v_lower_format[1])),Decimal(v_upper_format[0]+'e'+str(v_upper_format[1]))))


        st.divider()
        st.write("恭喜你发现了彩蛋！看到这行文字，说明你已经正确输入了程序运行的所有必要参数并完成了一次成功的计算！本程序由CraneMurmur开发，感谢您的支持，如有建议，请通过3930214985@qq.com反馈。")  # 如果为True，显示彩蛋
    except :
        st.markdown("<h2 style='color: red;'>请正确输入！！！</h2>",unsafe_allow_html=True)

