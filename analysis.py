import requests
from datetime import datetime, timedelta

# FRED API Key
api_key = '7d8f1ca8dcba9f0f73d7afd3e2235963'

# API 엔드포인트 및 시계열 코드 정의
fred_endpoint = 'https://api.stlouisfed.org/fred/'
interest_rate_series_code = 'DFF'  # Federal Funds Rate
exchange_rate_series_code = 'DEXKOUS'  # USD to KRW Exchange Rate

# API 요청을 보내는 함수 정의
def get_fred_data(series_code):
    url = f'{fred_endpoint}series/observations?series_id={series_code}&api_key={api_key}&file_type=json'
    response = requests.get(url)
    data = response.json()
    return data

# 최신 데이터와 과거 데이터 비교하는 함수 정의
def compare_data(series_code):
    # 최신 데이터 가져오기
    latest_data = get_fred_data(series_code)['observations'][0]['value']
    # 과거 데이터 가져오기 (1주일 전 데이터)
    past_data = get_fred_data(series_code)['observations'][7]['value']
    return latest_data, past_data

# 금리 비교
latest_interest_rate, past_interest_rate = compare_data(interest_rate_series_code)
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'\nCurrent Time: {current_time}')
print(f'----------------------------------------')
print(f'Latest Federal Funds Rate: {latest_interest_rate}')
print(f'Federal Funds Rate One Week Ago: {past_interest_rate}')
print(f'Federal Funds Rate Change: {float(latest_interest_rate) - float(past_interest_rate)}')

# 환율 비교
latest_exchange_rate, past_exchange_rate = compare_data(exchange_rate_series_code)
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(f'\nCurrent Time: {current_time}')
print(f'----------------------------------------')
print(f'Latest Exchange Rate: {latest_exchange_rate}')
print(f'Exchange Rate One Week Ago: {past_exchange_rate}')
print(f'Exchange Rate Change: {float(latest_exchange_rate) - float(past_exchange_rate)}')