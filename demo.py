import streamlit as st
import pandas as pd
import numpy as np
from math import ceil
MAX_VAL = 9999
MIN_VAL = 0
TAR = 7
TAR_2 = 7
CURRENT_ROW = []
def check_is_need_to_pass(num, tar_num=TAR, tar_num_2=TAR_2):
    int_num = int(num)
    if (int_num % tar_num == 0) or (str(num).find(str(tar_num)) != -1) or (int_num % tar_num_2 == 0) or (str(num).find(str(tar_num_2)) != -1):
        return f"{num}_PASS!"
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
# def init_df(total, start_val=0,end_val=9999, start_direction='Left'):
#     ret_df = dict()
#     start_direction = start_direction.lower()
#     usr_list = create_user_list(total)
#     end_val = round_to_multiple(total,start_val,end_val+1)
#     if start_direction == 'left':
#         for idx, num in enumerate(range(start_val, end_val)):
#             usr_idx = (idx+1) % len(usr_list) if (idx+1) % len(usr_list) else len(usr_list)
#             ret_df.setdefault(f'U{usr_idx}', []).append(check_is_need_to_pass(num))
#     else:
#         for idx,num in enumerate(range(start_val, end_val)):
#             usr_idx = (len(usr_list) + 1) - ((idx+1) % len(usr_list) if (idx+1)% len(usr_list) else len(usr_list))
#             ret_df.setdefault(f'U{usr_idx}', []).append(check_is_need_to_pass(num))
#     ret_df = dict(sorted(ret_df.items(), key=lambda item:int(item[0].replace('U',''))))
#     return pd.DataFrame(ret_df)
def update_df(usr_list,drop_usr,current_row,tar_num=7,tar_num_2=7, start_val=1,end_val=9999, start_direction='Left'):
    ret_df = dict()
    start_direction = start_direction.lower()
    # st.write(current_row)
    if st.session_state.current_side != start_direction:
        # st.write(st.session_state.max, st.session_state.min)
        # for key in usr_list:
        #     st.write(current_row.iloc[0][key], key)
        #     ret_df.setdefault(key,[]).append(current_row.iloc[0][key])
        if start_direction == 'left':
            # for key in usr_list:
            # # st.write(current_row.iloc[0][key], key)
            #     ret_df.setdefault(key,[]).append(current_row.iloc[0][key])
            for idx, num in enumerate(range(st.session_state.min, st.session_state.max)):
                usr_idx = (idx) % len(usr_list)
                ret_df.setdefault(usr_list[usr_idx], []).append(check_is_need_to_pass(num, tar_num, tar_num_2))
        else:
            for idx,num in enumerate(range(st.session_state.min, st.session_state.max)):
                usr_idx = len(usr_list) - (idx % len(usr_list))
                ret_df.setdefault(usr_list[usr_idx-1], []).append(check_is_need_to_pass(num, tar_num,tar_num_2))
    elif st.session_state.is_need_to_reset == False:
        st.session_state.status = 1
        
        end_val = round_to_multiple(len(usr_list),start_val,end_val+1)
        if start_direction == 'left':
            for idx, num in enumerate(range(start_val, end_val)):
                usr_idx = (idx) % len(usr_list)
                ret_df.setdefault(usr_list[usr_idx], []).append(check_is_need_to_pass(num, tar_num,tar_num_2))
        else:
            for idx,num in enumerate(range(start_val, end_val)):
                usr_idx = len(usr_list) - (idx % len(usr_list))
                ret_df.setdefault(usr_list[usr_idx-1], []).append(check_is_need_to_pass(num, tar_num,tar_num_2))
        st.session_state.max = end_val
        st.session_state.min = start_val
    
    else:
        st.session_state.status = 2
        if st.session_state.is_need_to_reset:
            st.session_state.count = 0
            st.session_state.is_need_to_reset = False
        
        new_start_val = current_row.values.tolist()[0][-1] if direction == 'left' else current_row.values.tolist()[0][0]
        if '_PASS!' in new_start_val:
            new_start_val = new_start_val.replace('_PASS!','')
        new_start_val = int(new_start_val) + 1
        if len(drop_usr) > 0:
            first_df = current_row.drop([drop_usr],axis = 1)
        else:
            first_df = current_row
        end_val = round_to_multiple(len(usr_list),new_start_val,end_val+1)
        for key in usr_list:
            ret_df.setdefault(key,[]).append(first_df.iloc[0][key])
        if start_direction == 'left':
           
            for idx, num in enumerate(range(new_start_val, end_val)):
                usr_idx = (idx) % len(usr_list)
                ret_df.setdefault(usr_list[usr_idx], []).append(check_is_need_to_pass(num, tar_num,tar_num_2))
        else:
            for idx,num in enumerate(range(new_start_val, end_val)):
                usr_idx = len(usr_list) - (idx % len(usr_list))
                ret_df.setdefault(usr_list[usr_idx-1], []).append(check_is_need_to_pass(num, tar_num,tar_num_2))
        st.session_state.max = end_val
        st.session_state.min = new_start_val
    ret_df = dict(sorted(ret_df.items(), key=lambda item:int(item[0].replace('U',''))))
    # st.write(ret_df)
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
if 'pre_list' not in st.session_state:
    st.session_state.pre_list = []
if 'current_row' not in st.session_state:
    st.session_state.current_row = []
if 'is_need_to_reset' not in st.session_state:
    st.session_state.is_need_to_reset = False
if 'status' not in st.session_state:
    st.session_state.status = 1
if 'is_need_to_update_row' not in st.session_state:
    st.session_state.is_need_to_update_row = False
if 'drop_usr' not in st.session_state:
    st.session_state.drop_usr = ''
if 'current_usrs' not in st.session_state:
    st.session_state.current_usrs = 0
if 'current_side' not in st.session_state:
    st.session_state.current_side = ''
if 'current_val' not in st.session_state:
    st.session_state.current_val = 0
if 'current_val_2' not in st.session_state:
    st.session_state.current_val_2 = 0
if 'max' not in st.session_state:
    st.session_state.max = ''
if 'min' not in st.session_state:
    st.session_state.min = ''
total = st.slider('當前人數:',1,15)
if total:
    if st.session_state.current_usrs != total:
        st.session_state.drop_usr = ''
        st.session_state.count = 0

    
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose = st.radio('落在第幾個:',range(1,total+1))
    sub_1,sub_2,sub_3 = st.columns(3)
    if 'count' not in st.session_state:
        st.session_state.count = 0
    with sub_1:
        MAX_VAL = int(st.number_input('上限',key='upper_input',value=1000,max_value=9999))
    with sub_2: 
        MIN_VAL = int(st.number_input('下限',key='lower_input',value=1, min_value=0))
        
    with sub_3:
        TAR_NUM = int(st.slider('逢N過',value=7, min_value=2,max_value=9))
        TAR_2 = int(st.slider('逢N過2', value=7, min_value=2, max_value=9))
    ori_usr_list=  [f'U{x}' for x in range(1, total+1)]
    # st.multiselect("hello", df_left.columns, default=list(df_left.columns))
    remaining_usr_list = st.multiselect("生存名單", ori_usr_list, default=ori_usr_list)
    if ori_usr_list == remaining_usr_list:
        st.session_state.pre_list = ori_usr_list
    elif st.session_state.pre_list != remaining_usr_list:
        drop_usr_list = list(set(st.session_state.pre_list) - set(remaining_usr_list))
        if len(drop_usr_list) > 0:
            st.session_state.drop_usr = drop_usr_list[0]
        else:
            st.session_state.drop_usr = ''
        st.session_state.pre_list = remaining_usr_list
        st.session_state.is_need_to_reset = True
    direction = st.radio('從哪個方向開始',['left', 'right'])
    if len(st.session_state.current_side) <= 0:
        st.session_state.current_side = direction
        
    sub_4,sub_5 = st.columns(2)
    with sub_4:
        checked = st.button('+1')
        if checked:
            st.session_state.count += 1
            # st.session_state.drop_usr = ''
            # if st.session_state.status == 1:
            #     st.session_state.count += 1
            # else:
            #     st.session_state.is_need_to_update_row = True
    with sub_5:
        reset = st.button('Reset')
        if reset:
            st.session_state.count = 0
    # drop_usr_list = list(set(st.session_state.pre_list) - set(remaining_usr_list))
    # if len(drop_usr_list) > 0:
    #     drop_usr = drop_usr_list[0]
    # else:
    #     drop_usr = ''
    if st.session_state.current_usrs != total or st.session_state.is_need_to_reset or st.session_state.current_side != direction \
        or st.session_state.current_val != TAR_NUM or st.session_state.current_val_2 != TAR_2:
        st.session_state.current_df = update_df(remaining_usr_list,st.session_state.drop_usr,st.session_state.current_row,TAR_NUM,TAR_2,MIN_VAL,MAX_VAL, direction)
    start_idx = 0 if st.session_state.count - 1 < 0 else st.session_state.count - 1
    end_idx = st.session_state.count + 1
    ori_df = pd.DataFrame(st.session_state.current_df.iloc[[start_idx,st.session_state.count,end_idx, end_idx + 1, end_idx+2]]).reset_index(drop=True).style.applymap(highlight_col, subset=pd.IndexSlice[1, [f'U{choose}']])
    st.session_state.current_row = pd.DataFrame(st.session_state.current_df.iloc[[st.session_state.count]])
    # if st.session_state.status == 1: 
    #     ori_df = pd.DataFrame(st.session_state.current_df.iloc[[start_idx,st.session_state.count,end_idx]]).reset_index(drop=True).style.applymap(highlight_col, subset=pd.IndexSlice[1, [f'U{choose}']])
    #     st.session_state.current_row = pd.DataFrame(st.session_state.current_df.iloc[[st.session_state.count]])

    # else:
    #     ori_df = pd.DataFrame(tmp_df.iloc[[0,0,1]]).reset_index(drop=True).style.applymap(highlight_col, subset=pd.IndexSlice[1, [f'U{choose}']])
    #     if (st.session_state.is_need_to_update_row == True):
    #         print('????')
    #         st.session_state.current_row = pd.DataFrame(tmp_df.iloc[[1]])
    #         st.session_state.is_need_to_update_row = False
    #     else:
    #         st.session_state.current_row = pd.DataFrame(tmp_df.iloc[[0]])
    # st.write(st.session_state.count)
    # st.write(st.session_state.current_row, st.session_state.status)
    st.session_state.current_usrs = total
    st.session_state.current_side = direction
    st.session_state.current_val = TAR_NUM
    st.session_state.current_val_2 = TAR_2


    # st.write(st.session_state.current_row)
    # st.write(st.session_state.pre_list, remaining_usr_list)
    # if st.session_state.pre_list != remaining_usr_list:
    #     st.session_state.pre_list = remaining_usr_list
    #     st.session_state.is_need_to_reset = True
    st.dataframe(ori_df,use_container_width=True)


    # col1, col2 = st.columns(2)
    # with col1: # 從左到右
    #     df_left = update_df(remaining_usr_list,TAR_NUM,MIN_VAL,MAX_VAL).style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
    #     st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    #     st.dataframe(df_left)
    # with col2:
    #     df_right = update_df(remaining_usr_list,TAR_NUM,MIN_VAL,MAX_VAL,'right').style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
    #     st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    #     st.dataframe(df_right)