import streamlit as st
import pandas as pd
import numpy as np
from math import ceil
MAX_VAL = 9999
MIN_VAL = 0
TAR = 7
def check_is_need_to_pass(num, tar_num=TAR):
    int_num = int(num)
    if (int_num % tar_num == 0) or (str(int_num)[-1] == str(tar_num)):
        return "PASS!"
    else:
        return str(num)

def button_clicked():
    print('5566')

def create_user_list(total):
    return [f'U{x}' for x in range(1,total+1)]
def round_to_multiple(total,start_val, ori_end_val):
    length = len(range(start_val, ori_end_val))
    new_length = int(total * ceil(length/total))
    return (start_val + new_length)
def init_df(total, start_val=0,end_val=9999, start_direction='Left'):
    ret_df = dict()
    start_direction = start_direction.lower()
    usr_list = create_user_list(total)
    end_val = round_to_multiple(total,start_val,end_val+1)
    if start_direction == 'left':
        for idx, num in enumerate(range(start_val, end_val)):
            usr_idx = (idx+1) % len(usr_list) if (idx+1) % len(usr_list) else len(usr_list)
            ret_df.setdefault(f'U{usr_idx}', []).append(check_is_need_to_pass(num))
    else:
        for idx,num in enumerate(range(start_val, end_val)):
            usr_idx = (len(usr_list) + 1) - ((idx+1) % len(usr_list) if (idx+1)% len(usr_list) else len(usr_list))
            ret_df.setdefault(f'U{usr_idx}', []).append(check_is_need_to_pass(num))
    ret_df = dict(sorted(ret_df.items(), key=lambda item:int(item[0].replace('U',''))))
    return pd.DataFrame(ret_df)
def update_df(usr_list,tar_num=7, start_val=1,end_val=9999, start_direction='Left'):
    ret_df = dict()
    start_direction = start_direction.lower()
    end_val = round_to_multiple(len(usr_list),start_val,end_val+1)
    if start_direction == 'left':
        for idx, num in enumerate(range(start_val, end_val)):
            usr_idx = (idx) % len(usr_list)
            ret_df.setdefault(usr_list[usr_idx], []).append(check_is_need_to_pass(num, tar_num))
    else:
        for idx,num in enumerate(range(start_val, end_val)):
            usr_idx = len(usr_list) - (idx % len(usr_list))
            ret_df.setdefault(usr_list[usr_idx-1], []).append(check_is_need_to_pass(num, tar_num))
    ret_df = dict(sorted(ret_df.items(), key=lambda item:int(item[0].replace('U',''))))
    return pd.DataFrame(ret_df)

def highlight_col(row):
    return 'background-color: yellow'
# st.set_page_config(layout="wide")
hide_dataframe_row_index = """
            <style>
            .row_heading.level0 {display:none}
            .blank {display:none}
            </style>
            """

total = st.slider('當前人數:',1,15)
if total:
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose = st.radio('落在第幾個:',range(1,total+1))
    sub_1,sub_2,sub_3 = st.columns(3)
    if 'count' not in st.session_state:
        st.session_state.count = 0
    with sub_1:
        MAX_VAL = int(st.number_input('上限',value=500,max_value=9999))
    with sub_2: 
        MIN_VAL = int(st.number_input('下限',value=1, min_value=0))
    with sub_3:
        TAR_NUM = int(st.slider('逢N過',value=7, min_value=2,max_value=9))
    ori_usr_list=  [f'U{x}' for x in range(1, total+1)]
    # st.multiselect("hello", df_left.columns, default=list(df_left.columns))
    remaining_usr_list = st.multiselect("生存名單", ori_usr_list, default=ori_usr_list)
    direction = st.radio('從哪個方向開始',['left', 'right'])
    sub_4,sub_5 = st.columns(2)
    with sub_4:
        checked = st.button('+1')
        if checked:
            st.session_state.count += 1
    with sub_5:
        reset = st.button('Reset')
        if reset:
            st.session_state.count = 0
    tmp_df = update_df(remaining_usr_list,TAR_NUM,MIN_VAL,MAX_VAL, direction)
    start_idx = 0 if st.session_state.count - 1 < 0 else st.session_state.count - 1
    end_idx = tmp_df.shape[0] if st.session_state.count + 1 > tmp_df.shape[0] else st.session_state.count + 1
    ori_df = pd.DataFrame(tmp_df.iloc[[start_idx,st.session_state.count,end_idx]]).reset_index(drop=True).style.applymap(highlight_col, subset=pd.IndexSlice[1, [f'U{choose}']])
    # df = ori_df.iloc[[st.session_state.count]]
    st.dataframe(ori_df)

    # col1, col2 = st.columns(2)
    # with col1: # 從左到右
    #     df_left = update_df(remaining_usr_list,TAR_NUM,MIN_VAL,MAX_VAL).style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
    #     st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    #     st.dataframe(df_left)
    # with col2:
    #     df_right = update_df(remaining_usr_list,TAR_NUM,MIN_VAL,MAX_VAL,'right').style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
    #     st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    #     st.dataframe(df_right)