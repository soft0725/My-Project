import streamlit as st
from PIL import Image
from model import main

st.write("""
    ## 간단한 거북목 측정 프로그램
    아래 버튼을 눌러 이미지를 업로드 해주세요.
    """)

# 파일 업로드
uploaded_image = st.file_uploader("", type=["jpg", "png", "jpeg"])

# 업로드한 이미지 저장 및 표시
if uploaded_image is not None:
    # 이미지를 서버에 저장
    with open("images/uploaded_image.jpg", "wb") as f:
        temp_image = f.write(uploaded_image.read())

    # 이미지 다시 열기
    image = Image.open("images/uploaded_image.jpg")

    # 이미지 표시
    st.image(image, caption='업로드한 이미지', use_column_width=True)

    # 결과 표시
    result = main()
    if result:
        result_image = Image.open("images/Result.jpg")
        st.image(result_image, caption='결과 이미지', use_column_width=True)
        if result > 1.0:
            st.write("결과 : 거북목 아님")
        else:
            formatted_result = f"결과 : 거북목입니다. (__수치:{result:.3f}__   1에서 멀어질 수록 심한 거북목)"
            st.write(formatted_result)
    else:
        st.write("다른 사진을 사용해주세요.")
