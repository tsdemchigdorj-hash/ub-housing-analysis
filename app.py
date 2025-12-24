import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Дата унших (Excel учраас)
@st.cache_data
def load_data():
    # Файл чинь Excel бүтэцтэй тул read_excel ашиглана
    return pd.read_excel('ub_housing.csv')

try:
    df = load_data()
    
    # 2. Тайланд хэрэгтэй тооцооллуудыг энд хийнэ (Pivot гэх мэт)
    pivot_df = df.pivot_table(index='Сар', columns='Дүүрэг', values='Утга', aggfunc='mean')
    
    # --- ТАНЫ БИЧСЭН ГРАФИКЫН КОД ЭХЭЛЖ БАЙНА ---
    plt.style.use('dark_background')
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    fig.suptitle('Улаанбаатар хотын орон сууцны зах зээлийн нэгдсэн тайлан', fontsize=22)

    # НҮД 1: Ерөнхий тренд
    overall_mean = pivot_df.mean(axis=1)
    axes[0, 0].plot(overall_mean.index, overall_mean.values, color='#3498db', linewidth=4)
    axes[0, 0].set_title('1. Орон сууцны үнийн ерөнхий хандлага')

    # НҮД 2: Үнийн хайч
    max_p = pivot_df.max(axis=1)
    min_p = pivot_df.min(axis=1)
    axes[0, 1].plot(pivot_df.index, max_p, color='#2ecc71', alpha=0.7)
    axes[0, 1].plot(pivot_df.index, min_p, color='#e74c3c', alpha=0.7)
    axes[0, 1].fill_between(pivot_df.index, min_p, max_p, color='#f1c40f', alpha=0.1)
    axes[0, 1].set_title('2. Үнийн зааг /Хайч/')

    # НҮД 3: Улирлын шинж чанар
    # (seasonal_trend-ийг энд тооцоолох хэрэгтэй)
    df['Сар_Тоо'] = pd.to_datetime(df['Сар']).dt.month
    seasonal = df.groupby('Сар_Тоо')['Утга'].mean()
    sns.barplot(x=seasonal.index, y=seasonal.values, ax=axes[1, 0], palette='viridis')
    axes[1, 0].set_title('3. Саруудын дундаж үнэ')

    # НҮД 4: Дүүргүүдийн өсөлт
    # (Өсөлтийн тооцооллыг энд хийнэ)
    growth = ((pivot_df.iloc[-1] - pivot_df.iloc[0]) / pivot_df.iloc[0] * 100).reset_index()
    growth.columns = ['Дүүрэг', 'Өсөлт (%)']
    sns.barplot(data=growth.sort_values('Өсөлт (%)', ascending=False), 
                x='Өсөлт (%)', y='Дүүрэг', ax=axes[1, 1], palette='magma')
    axes[1, 1].set_title('4. Дүүрэг бүрийн нийт өсөлтийн хувь')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # --- ХАМГИЙН ЧУХАЛ ХЭСЭГ: ВЭБ ДЭЭР ГАРГАХ ---
    st.pyplot(fig) 

except Exception as e:
    st.error(f"Алдаа гарлаа: {e}")
