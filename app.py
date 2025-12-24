import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Хуудасны тохиргоо
st.set_page_config(page_title="UB Housing Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Excel файлыг унших
    data = pd.read_excel('ub_housing.csv')
    data['Сар'] = pd.to_datetime(data['Сар'])
    return data

try:
    df = load_data()
    
    st.title("🏙️ Улаанбаатар хотын орон сууцны зах зээлийн тайлан")
    
    # Тооцооллууд
    latest_date = df['Сар'].max()
    # ЭНД ЗАССАН ШҮҮ: 'Сар' монгол үсгээр
    latest_data = df[df['Сар'] == latest_date]
    avg_price = latest_data['Утга'].mean()
    
    # Дээд талын Metrics
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Дундаж үнэ (Сүүлийн сар)", f"{avg_price:.1f} сая ₮")
    with m2:
        top_district = latest_data.loc[latest_data['Утга'].idxmax(), 'Дүүрэг']
        st.metric("Хамгийн үнэтэй дүүрэг", top_district)
    with m3:
        # Ерөнхий дундаж өсөлт
        monthly_avg = df.groupby('Сар')['Утга'].mean()
        total_growth = ((monthly_avg.iloc[-1] / monthly_avg.iloc[0]) - 1) * 100
        st.metric("Нийт өсөлт (хугацааны турш)", f"{total_growth:.1f}%", delta=f"{total_growth:.1f}%")

    st.divider()

    # Табууд
    tab1, tab2 = st.tabs(["📈 Ерөнхий тренд", "📊 Дүүргийн харьцуулалт"])

    with tab1:
        st.subheader("Орон сууцны үнийн динамик өөрчлөлт")
        overall_trend = df.groupby('Сар')['Утга'].mean().reset_index()
        fig1 = px.area(overall_trend, x='Сар', y='Утга', 
                       title="УБ хотын дундаж үнийн тренд",
                       color_discrete_sequence=['#1f77b4'])
        fig1.update_layout(hovermode="x unified")
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.subheader("Дүүрэг бүрийн үнэ")
            fig2 = px.line(df, x='Сар', y='Утга', color='Дүүрэг', markers=True)
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            st.subheader("Өсөлтийн хувь")
            pivot_calc = df.pivot_table(index='Сар', columns='Дүүрэг', values='Утга', aggfunc='mean')
            growth = ((pivot_calc.iloc[-1] / pivot_calc.iloc[0]) - 1) * 100
            growth = growth.reset_index().rename(columns={0: 'Өсөлт (%)'})
            fig3 = px.bar(growth.sort_values('Өсөлт (%)'), x='Өсөлт (%)', y='Дүүрэг', 
                         color='Өсөлт (%)', orientation='h', color_continuous_scale='Viridis')
            st.plotly_chart(fig3, use_container_width=True)

except Exception as e:
    st.error(f"Алдаа гарлаа: {e}")
