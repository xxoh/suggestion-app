import streamlit as st
import pandas as pd

# 초기 데이터프레임 생성
if 'suggestions' not in st.session_state:
    st.session_state.suggestions = pd.DataFrame(columns=['id', 'student', 'suggestion', 'response'])

# 건의 제출
def submit_suggestion(student, suggestion):
    new_id = len(st.session_state.suggestions) + 1
    st.session_state.suggestions = st.session_state.suggestions.append({'id': new_id, 'student': student, 'suggestion': suggestion, 'response': ''}, ignore_index=True)

# 건의 삭제
def delete_suggestion(suggestion_id):
    st.session_state.suggestions = st.session_state.suggestions[st.session_state.suggestions['id'] != suggestion_id]

# UI 구성
st.title("학교 건의 앱")

user_type = st.radio("사용자 유형 선택", ('학생', '관리자'))

if user_type == '학생':
    # 학생 UI
    st.subheader("건의 제출")
    with st.form(key='suggestion_form'):
        student_name = st.text_input("학생 이름")
        suggestion_text = st.text_area("건의 내용")
        submit_button = st.form_submit_button(label='건의 제출', on_click=submit_suggestion, args=(student_name, suggestion_text))

elif user_type == '관리자':
    # 관리자 UI
    st.subheader("건의 목록")
    for index, row in st.session_state.suggestions.iterrows():
        st.write(f"**[{row['id']}] {row['student']}**: {row['suggestion']}")
        if row['response']:
            st.write(f"**답변**: {row['response']}")
        
        response_text = st.text_area(f"답변 입력 ({row['id']})", value=row['response'], key=f'response_{row["id"]}')
        if st.button("답변 달기", key=f'reply_{row["id"]}'):
            st.session_state.suggestions.at[index, 'response'] = response_text
        
        if st.button("건의 삭제", key=f'delete_{row["id"]}'):
            delete_suggestion(row['id'])
            st.experimental_rerun()

# 건의 목록 (학생용)
if user_type == '학생':
    st.subheader("내 건의 목록")
    for index, row in st.session_state.suggestions.iterrows():
        if row['student'] == student_name:
            st.write(f"**[{row['id']}] {row['suggestion']}**")
            if row['response']:
                st.write(f"**답변**: {row['response']}")
