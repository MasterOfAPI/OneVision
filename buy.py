# Module Import
import pyupbit
import numpy as np
import pandas as pd
import time
import datetime

# API KEY (동적 할당된 IP는 접근 불가)
access = "6m8iaAEu9DgzNwQ08XJnXV2d06Ix90x0Ly0w1lEG"
secret = "5L7sGieX4K396bfuXEafe2IDXpMHxBdMVForJWiZ"
upbit = pyupbit.Upbit(access, secret)

# KRW 잔고 확인 (수수료 포함)
balance = upbit.get_balance("KRW")
fee = balance * 0.0005
real_balance = balance - fee
print("보유 KRW : ")
print(upbit.get_balance("KRW"))
print("\n수수료(0.05%) 적용 KRW : ")
print(real_balance)

# 업비트에서 거래되는 모든 암호화폐 목록
print("\n암호화폐 목록 : ")
markets = pyupbit.get_tickers(fiat="KRW")
# 존버 암호화폐는 대상 제외
markets.remove("KRW-GLM")
print(markets)

pd.options.display.float_format = '{:.2f}'.format

while True:
    # OHLC(open 시가, high 고가, low 저가, close 종가, volume 거래량)
    def get_multiple_ohlcvs(markets, count=2):
        ohlcvs = {}
        for market in markets:
            # interval="day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month"
            data = pyupbit.get_ohlcv(market, count=count, interval="day")
            ohlcvs[market] = data
        return ohlcvs

    markets = pyupbit.get_tickers(fiat="KRW")
    ohlcvs_multiple = get_multiple_ohlcvs(markets, count=2)

    # 'upper' 지표 계산
    for market, df in ohlcvs_multiple.items():
        df['upper'] = ((df['close'] - df['close'].shift(1)) / df['close'].shift(1)) * 100

    # 새로운 데이터프레임 만들기 (소요시간 약 1분)
    df = pd.concat(ohlcvs_multiple.values(), keys=ohlcvs_multiple.keys())

    # open: 해당 시간대의 시가
    # high: 해당 시간대의 고가
    # low: 해당 시간대의 저가
    # close: 해당 시간대의 종가
    # volume: 해당 시간대의 거래량
    # value: 해당 시간대의 거래 대금
    # range: 해당 시간대의 가격 변동폭
    # target: 해당 시간대의 목표 가격
    # ror: 해당 시간대의 수익율
    # hpr: 해당 시간대의 누적 수익률p
    # dd: 해당 시간대의 최대 손실률

    # 'upper' 값이 가장 큰 항목 추출
    max_upper_row = df.loc[df['upper'].idxmax()]
    print("\n금일 급상승 암호화폐:")
    print(max_upper_row)

    # 금일 급상승 암호화폐 Ticker 확인
    boss_crypto_name = max_upper_row.name[0]
    print(boss_crypto_name)


# 매수 알고리즘

# 비트코인 upper 확인
    for _ in range(200):
        # interval="day/minute1/minute3/minute5/minute10/minute15/minute30/minute60/minute240/week/month"
        df_bit = pyupbit.get_ohlcv("KRW-BTC", count=2, interval="minute1")
        df_bit['upper'] = ((df_bit['close'] - df_bit['close'].shift(1)) / df_bit['close'].shift(1)) * 100
        current_upper = df_bit['upper'].iloc[-1]  # 현재 가장 최근의 'upper' 값
        print("\n---------------------------------")
        print("KRW-BTC 'upper'값 :", current_upper)

        # 매수/매도 호가 확인
        boss_crypto_orderbook = pyupbit.get_orderbook(ticker=boss_crypto_name)

        asks = boss_crypto_orderbook['orderbook_units']
        bids = boss_crypto_orderbook['orderbook_units']

        # "market": 암호화폐의 거래 페어 (예: "KRW-BTC")
        # "timestamp": 호가 정보를 가져온 시간 (UNIX 타임스탬프)
        # "total_ask_size": 매도 호가 총 잔량
        # "total_bid_size": 매수 호가 총 잔량
        # "orderbook_units": 호가 정보를 담은 리스트
        # "ask_price": 매도 호가 가격
        # "bid_price": 매수 호가 가격
        # "ask_size": 매도 호가 잔량
        # "bid_size": 매수 호가 잔량

        # 매도 호가와 매수 호가를 데이터프레임으로 변환
        df_asks = pd.DataFrame(asks, columns=["ask_price", "ask_size"])
        df_bids = pd.DataFrame(bids, columns=["bid_price", "bid_size"])

        median_bid_price = df_bids["bid_price"].median()
        median_bid_size = df_bids["bid_size"].median()
        max_bid_price = df_bids["bid_price"].max()
        max_bid_size = df_bids["bid_size"].max()

        print("매수 대상 :", boss_crypto_name)
        print("매수 가격 중간 값 :", median_bid_price)
        print("매수 잔량 중간 값 :", median_bid_size)
        print("매수 가격 최대 값 :", max_bid_price)
        print("매수 잔량 최대 값 :", max_bid_size)

        # 거래 대금 세팅 (※주의항목※)
        set_balance = real_balance * 0.1
        print("준비된 보유 자금   :", set_balance)

        # 매수 API 호출 (※주의항목※)
        if current_upper > 0.06 and median_bid_size * 10 < max_bid_size:
            print("\n매수 조건 충족: 매수를 진행합니다.")
            my_bid_price = max_bid_price
            my_bid_size = (set_balance / my_bid_price) - 1 # 오류 방지를 위한 -1
            print(upbit.buy_limit_order(boss_crypto_name, max_bid_price, my_bid_size))
            break  # 매수 조건 충족 시 반복문 종료
        elif set_balance < max_bid_price:
            print("\n매도 조건 미충족: 보유 자금이 부족합니다.")
            break
        else:
            print("\n매수 조건 미충족: 조건 값을 재조회합니다.")
            # 아무 것도 하지 않음