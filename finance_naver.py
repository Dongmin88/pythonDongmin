import pandas as pd
import warnings
import matplotlib.pyplot as plt
from IPython.display import display
import streamlit as st



def get_exchange_rate_data(code, currency_name):
    warnings.filterwarnings('ignore')
    plt.rc('font',family='Malgun Gothic')
    df = pd.DataFrame()
    for page_num in range(1,6):
        
        base_url=f"https://finance.naver.com/marketindex/exchangeDailyQuote.naver?marketindexCd=FX_{code}KRW&page={page_num}"
        temp = pd.read_html(base_url,encoding='cp949',header=1)
        df=pd.concat([df,temp[0]],ignore_index=True)
    total_rate_data_view(df,code,currency_name)

def total_rate_data_view(df,code,currency_name):
    #원하는 열만 선택
    df_total = df[['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]

    #데이터표시
    st.subheader(f'{currency_name} : {code}')
    
    st.dataframe(df_total.head(20))
    
    #df_test= df.loc[:,['날짜', '매매기준율', '사실 때', '파실 때', '보내실 때', '받으실 때']]
    #df_test

    df_total['날짜'] = pd.to_datetime(df_total['날짜'], format='%Y.%m.%d') 
    df_total['월'] = df_total['날짜'].dt.month  

    df_total_chart = df_total.copy()
    df_total_chart=df_total_chart.set_index('날짜')

    df_total_chart = df_total_chart[::-1]



 
    ax =df_total_chart['매매기준율'].plot(figsize=(15,6), title='exchange rate')
    fig = ax.get_figure()
    st.pyplot(fig)
    plt.show()
    
    # month_rate_data_view(df_total)
    
    
def month_rate_data_view(df_total):
    df_total['날짜'] = pd.to_datetime(df_total['날짜'], format='%Y.%m.%d') 
    df_total['월'] = df_total['날짜'].dt.month  
    avr_month = df_total.groupby('월').mean()

    #검색한 월에 대해서 자료 다가져 오기
    month_in = int(input('검색 할 월 입력>>'))
    #month_df = df_total[df_total['월']==month_in]
    #month_df = month_df['날짜','매매기준율','사실 때','파실 때','보내실 때','받으실 때']
    month_df = df_total.loc[df_total['월']==month_in,['날짜','매매기준율','사실 때','파실 때','보내실 때','받으실 때']]
    month_df[::-1].reset_index(drop=True)

    month_df_chart = month_df.copy()
    month_df_chart = month_df_chart.reset_index(drop=True)
    month_df_chart =month_df_chart.set_index('날짜')

    month_df_chart['매매기준율'].plot()
    plt.show()
    

def exchane_main():    
    currency_symbols_name = {'미국 달러':'USD','유렵연합 유로':'EUR','일본 엔(100)':"JPY"}
    
    currency_name = st.selectbox("통화 선택",currency_symbols_name.keys())
    # currency_name = ['미국 달러','유럽연합 유로','일본 엔(100)']
    code = currency_symbols_name[currency_name]
    clicked= st.button('환율 데이터 가져오기')
    if clicked:
        get_exchange_rate_data(code, currency_name)
    
if __name__=="__main__":
    exchane_main()
    


#데이터 표시
# print(currency_symbols[code_in])




