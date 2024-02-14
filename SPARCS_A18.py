import streamlit as st
import pandas as pd

def korean_date_parser(date):
    """한국어로 된 날짜를 파싱하여 ISO 형식(yyyy-mm-dd)으로 반환합니다."""
    months = ['01월', '02월', '03월', '04월', '05월', '06월', '07월', '08월', '09월', '10월', '11월', '12월']
    year_str, month_str = date.split()
    year = int(year_str.replace('년', ''))
    month = months.index(month_str) + 1
    return f"{year:04d}-{month:02d}-01"  # First day of the month

def load_data(file_path):
    """CSV 파일을 로드하고 데이터프레임을 반환합니다."""
    try:
        df = pd.read_csv(file_path, parse_dates=['날짜'], date_parser=korean_date_parser)
        return df
    except pd.errors.ParserError:
        st.error("데이터를 파싱하는 중에 오류가 발생했습니다. CSV 파일의 형식을 확인하십시오.")
        return None

def main():
    # Streamlit 앱 제목
    st.title('Train Passenger Visualization')

    # 데이터 파일의 절대 경로
    file_path = "rail_data.csv"

    # 파일 로드 및 데이터프레임 생성
    df = load_data(file_path)

    if df is not None:
        # 데이터프레임 보기
        # st.write(df)

        # 날짜를 인덱스로 설정
        df.set_index('날짜', inplace=True)

        # 월 선택
        selected_month = st.selectbox('월 선택', df.index.strftime('%Y-%m').unique())

        # 월별 노선 이용객 현황 시각화
        st.subheader(f'{selected_month} 이용객 현황')
        df_selected_month = df[df.index.strftime('%Y-%m') == selected_month]
        st.bar_chart(df_selected_month.groupby('노선')['여객수송실적'].sum())

if __name__ == "__main__":
    main()

st.markdown("대전은 가장 이용량이 많은 경부선(대전역), 호남선(서대전역)이 모두 지나는 교통의 중심지로, ")
st.markdown("유동인구가 많은 것으로 파악된다.")


# 이미지 표시
st.image("rail_line_image.png", caption='Example Image 1', use_column_width=True)