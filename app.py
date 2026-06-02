import sys
import os
# Thêm dòng này để Streamlit Cloud tự nhận diện toàn bộ các file .py trong thư mục dự án
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
# ... (Giữ nguyên toàn bộ phần code phía dưới của file app.py cũ của bạn)
import pandas as pd
from database import load_data
from chatbot import custom_chatbot

st.set_page_config(page_title="Dashboard Tài Chính", layout="wide")
sales, customers = load_data()

if sales is None or customers is None:
    st.error("❌ Thiếu file dữ liệu mẫu CSV!")
else:
    st.sidebar.title("🧭 MENU ĐIỀU HƯỚNG")
    menu = st.sidebar.radio("Chọn màn hình:", ["📊 Dashboard Kinh Doanh", "💬 Trợ Lý AI Chatbot"])

    if menu == "📊 Dashboard Kinh Doanh":
        st.title("📊 DASHBOARD PHÂN TÍCH TÀI CHÍNH")
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("Tổng Doanh Thu", f"{sales['revenue'].sum():,.0f} đ")
        col2.metric("Lợi Nhuận", f"{sales['profit'].sum():,.0f} đ")
        col3.metric("Tổng Công Nợ", f"{customers['debt'].sum():,.0f} đ")
        st.markdown("---")
        st.subheader("📈 Biểu Đồ Xu Hướng")
        st.line_chart(sales.groupby('date')[['revenue', 'profit']].sum())

    elif menu == "💬 Trợ Lý AI Chatbot":
        st.title("💬 TRỢ LÝ AI TRUY VẤN TỰ ĐỘNG")
        if "chat_history" not in st.session_state: st.session_state.chat_history = []
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]): st.markdown(msg["content"])
        if user_input := st.chat_input("Hỏi tôi về doanh thu, lợi nhuận..."):
            with st.chat_message("user"): st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            reply = custom_chatbot(user_input)
            with st.chat_message("assistant"): st.markdown(reply)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
