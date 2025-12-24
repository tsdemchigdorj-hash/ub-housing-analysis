import streamlit as st
import pandas as pd
import plotly.express as px  # Интерактив графикын сан

# 1. Вэбийн тохиргоо
st.set_page_config(page_title="UB Housing Analysis", layout="wide")
st.title("🏙️ Улаанбаатар хотын орон сууцны зах зээлийн дэлгэрэнгүй шинжилгээ")

@st.cache_data
def load_data():
    # Excel файлыг унших
    data = pd.read_excel('ub_housing.csv')
    data['Сар'] = pd.to_datetime(data['Сар'])
    return data

try:
    df = load_data()
    
    # --- 1-Р ХЭСЭГ: ЕРӨНХИЙ ТРЕНД (ТОМ ХАРАГДАЦ) ---
    st.subheader("📊 1. Орон сууцны үнийн ерөнхий хандлага")
    overall_mean = df.groupby('Сар')['Утга'].mean().reset_index()
    
    fig1 = px.line(overall_mean, x='Сар', y='Утга', 
                  title="Улаанбаатар хотын дундаж үнэ (сая ₮)",
                  markers=True, line_shape="linear")
    fig1.update_layout(xaxis_title="Хугацаа", yaxis_title="Үнэ (сая ₮)")
    st.plotly_chart(fig1, use_container_width=True) # Дэлгэц дүүрэн гарна

    st.divider() # Хөндлөн зураас

    # --- 2-Р ХЭСЭГ: ДҮҮРГҮҮДИЙН ХАРЬЦУУЛАЛТ ---
    st.subheader("🏘️ 2. Дүүргүүдийн үнийн харьцуулалт болон өсөлт")
    col1, col2 = st.columns(2) # Дэлгэцийг босоо хоёр хуваах

    with col1:
        # Дүүрэг бүрийн шугаман график
        pivot_df = df.pivot_table(index='Сар', columns='Дүүрэг', values='Утга', aggfunc='mean').reset_index()
        fig2 = px.line(df, x='Сар', y='Утга', color='Дүүрэг', title="Дүүрэг бүрээр")
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        # Өсөлтийн хувь (Баганан график)
        pivot_calc = df.pivot_table(index='Сар', columns='Дүүрэг', values='Утга', aggfunc='mean')
        growth = ((pivot_calc.iloc[-1] - pivot_calc.iloc[0]) / pivot_calc.iloc[0] * 100).reset_index()
        growth.columns = ['Дүүрэг', 'Өсөлт (%)']
        fig3 = px.bar(growth.sort_values('Өсөлт (%)'), x='Өсөлт (%)', y='Дүүрэг', 
                     orientation='h', color='Өсөлт (%)', title="Нийт өсөлтийн хувь")
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # --- 3-Р ХЭСЭГ: УЛИРЛЫН НӨЛӨӨ ---
    st.subheader("📅 3. Саруудын дундаж үнэ (Улирлын нөлөө)")
    df['Сар_Дугаар'] = df['Сар'].dt.month
    seasonal = df.groupby('Сар_Дугаар')['Утга'].mean().reset_index()
    
    fig4 = px.bar(seasonal, x='Сар_Дугаар', y='Утга', 
                 title="Сар бүрийн үнийн дундаж үзүүлэлт",
                 labels={'Сар_Дугаар': 'Сар', 'Утга': 'Дундаж үнэ (сая ₮)'},
                 color='Утга')
    fig4.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1)) # Сарыг 1, 2, 3.. гэж харуулна
    st.plotly_chart(fig4, use_container_width=True)

except Exception as e:
    st.error(f"Алдаа гарлаа: {e}")
