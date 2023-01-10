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
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    # for col in df.columns:
    #     if is_object_dtype(df[col]):
    #         try:
    #             df[col] = pd.to_datetime(df[col])
    #         except Exception:
    #             pass

    #     if is_datetime64_any_dtype(df[col]):
    #         df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# with st.sidebar:
#     st.radio("當前人數:", range(1,28))
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
def update_df(usr_list, start_val=1,end_val=9999, start_direction='Left'):
    ret_df = dict()
    print(usr_list)
    start_direction = start_direction.lower()
    end_val = round_to_multiple(len(usr_list),start_val,end_val+1)
    if start_direction == 'left':
        for idx, num in enumerate(range(start_val, end_val)):
            usr_idx = (idx) % len(usr_list)
            ret_df.setdefault(usr_list[usr_idx], []).append(check_is_need_to_pass(num))
    else:
        for idx,num in enumerate(range(start_val, end_val)):
            usr_idx = len(usr_list) - (idx % len(usr_list))
            ret_df.setdefault(usr_list[usr_idx-1], []).append(check_is_need_to_pass(num))
    ret_df = dict(sorted(ret_df.items(), key=lambda item:int(item[0].replace('U',''))))
    return pd.DataFrame(ret_df)

def highlight_col(row):
    return 'background-color: yellow'
st.set_page_config(layout="wide")
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
    with st.sidebar:
        MAX_VAL = int(st.number_input('上限',value=500,max_value=9999)) 
        MIN_VAL = int(st.number_input('下限',value=1, min_value=0))
    ori_usr_list=  [f'U{x}' for x in range(1, total+1)]
    # st.multiselect("hello", df_left.columns, default=list(df_left.columns))
    remaining_usr_list = st.multiselect("hello", ori_usr_list, default=ori_usr_list)
    df_left = update_df(remaining_usr_list,MIN_VAL,MAX_VAL).style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
    col1, col2 = st.columns(2)
    with col1: # 從左到右
        df_left = update_df(remaining_usr_list,MIN_VAL,MAX_VAL).style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        st.dataframe(df_left)
    with col2:
        df_right = update_df(remaining_usr_list,MIN_VAL,MAX_VAL,'right').style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
        st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
        st.dataframe(df_right)
    num = st.number_input('text', format='%d')
    st.text(num)
    if num:
        check = st.button('GOGO')
        if check:
            st.text(check_is_need_to_pass(num))