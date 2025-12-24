import streamlit as st
import pandas as pd
import plotly.express as px # Илүү тод, томруулж болдог графикын сан

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="UB Housing Analysis", layout="wide")
st.title("🏙️ Улаанбаатар хотын орон сууцны зах зээлийн дэлгэрэнгүй тайлан")

@st.cache_data
def load_data():
    # Excel файлыг унших
    data = pd.read_excel('ub_housing.csv')
    data['Сар'] = pd.to_datetime(data['Сар'])
    return data

try:
    df = load_data()
    
    # --- 1. Үнийн ерөнхий хандлага (ТОМ ГРАФИК) ---
    st.header("1. Орон сууцны үнийн ерөнхий хандлага")
    overall_mean = df.groupby('Сар')['Утга'].mean().reset_index()
    fig1 = px.line(overall_mean, x='Сар', y='Утга', 
                  title="Улаанбаатар хотын дундаж үнэ (сая ₮)",
                  line_shape="spline", render_mode="svg")
    fig1.update_layout(height=500) # Өндөрийг нь нэмсэн
    st.plotly_chart(fig1, use_container_width=True)

    # --- 2. Дүүргүүдийн харьцуулалт (ТАБ-аар тусгаарлах) ---
    st.header("2. Дүүргүүдийн нарийвчилсан шинжилгээ")
    
    col1, col2 = st.columns(2) # Дэлгэцийг хоёр хувааж харуулах
    
    with col1:
        st.subheader("Дүүрэг бүрийн үнийн хайч")
        pivot_df = df.pivot_table(index='Сар', columns='Дүүрэг', values='Утга', aggfunc='mean')
        st.line_chart(pivot_df) # Энэ график дээр дүүрэг бүрийг унтрааж асааж болно

    with col2:
        st.subheader("Нийт өсөлтийн хувь (%)")
        first_vals = pivot_df.iloc[0]
        last_vals = pivot_df.iloc[-1]
        growth = ((last_vals - first_vals) / first_vals * 100).reset_index()
        growth.columns = ['Дүүрэг', 'Өсөлт (%)']
        fig2 = px.bar(growth.sort_values('Өсөлт (%)'), x='Өсөлт (%)', y='Дүүрэг', 
                     orientation='h', color='Өсөлт (%)')
        st.plotly_chart(fig2, use_container_width=True)

    # --- 3. Улирлын нөлөө (ТУСДАА ХЭСЭГ) ---
    st.header("3. Саруудын дундаж үнэ (Улирлын нөлөө)")
    df['Сар_Нэр'] = df['Сар'].dt.month
    seasonal = df.groupby('Сар_Нэр')['Утга'].mean().reset_index()
    fig3 = px.bar(seasonal, x='Сар_Нэр', y='Утга', color='Утга',
                 labels={'Сар_Нэр': 'Сар', 'Утга': 'Дундаж үнэ'},
                 title="Сар бүрийн үнийн дундаж үзүүлэлт")
    st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Алдаа гарлаа: {e}")
