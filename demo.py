import streamlit as st
def check_is_need_to_pass(num):
    int_num = int(num)
    if (int_num % 7 == 0) or (str(int_num)[-1] == '7'):
        return "PASS!"
    else:
        return str(num)


num = st.number_input('text', format='%d')
st.text(num)
if num:
    check = st.button('GOGO')
    if check:
        st.text(check_is_need_to_pass(num))