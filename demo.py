import streamlit as st
import pandas as pd
import numpy as np
def check_is_need_to_pass(num):
    int_num = int(num)
    if (int_num % 7 == 0) or (str(int_num)[-1] == '7'):
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
def round_to_multiple(total, ori_end_val):
    return total * round(ori_end_val/total)
def init_df(total, start_val=0,end_val=9999, start_direction='Left'):
    ret_df = dict()
    start_direction = start_direction.lower()
    usr_list = create_user_list(total)
    end_val = round_to_multiple(total,end_val)
    if start_direction == 'left':
        for num in range(start_val, end_val+1):
            idx = num % len(usr_list) if num % len(usr_list) else len(usr_list)
            ret_df.setdefault(f'U{idx}', []).append(check_is_need_to_pass(num))
    else:
        for num in range(start_val, end_val+1):
            idx = (len(usr_list) + 1) - (num % len(usr_list) if num % len(usr_list) else len(usr_list))
            ret_df.setdefault(f'U{idx}', []).append(check_is_need_to_pass(num))
        ret_df = dict(sorted(ret_df.items(), key=lambda item:int(item[0].replace('U',''))))
    return pd.DataFrame(ret_df)
def highlight_col(row):
    return 'background-color: yellow'
st.set_page_config(layout="wide")
total = st.slider('當前人數:',1,15)
if total:
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
    choose = st.radio('落在第幾個:',range(1,total+1))
    max_val = int(st.number_input('上限',value=500,max_value=9999))
    min_val = int(st.number_input('下限',value=1, min_value=0))
    col1, col2 = st.columns(2)
    with col1: # 從左到右
        df_left = init_df(total,min_val,max_val,'left').style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
        st.dataframe(df_left)
    with col2:
        df_right = init_df(total,min_val,max_val,'right').style.applymap(highlight_col, subset=pd.IndexSlice[:, [f'U{choose}']])
        st.dataframe(df_right)
    st.write(choose)
    num = st.number_input('text', format='%d')
    st.text(num)
    if num:
        check = st.button('GOGO')
        if check:
            st.text(check_is_need_to_pass(num))