#bestK

import pyupbit
import numpy as np


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", count=7)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    fee = 0.0032
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'] - fee,
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))


#자동매매코드
import time
import pyupbit
import datetime

access = "XSLSnoA0exVbeHoVBXwmWNrRekw1xKZzU0qQ1pbP"          # 본인 값으로 변경
secret = "24dfzujs8xe8I5uoiwupxJNJhXewAQSKKm4kRrvH"          # 본인 값으로 변경

def get_target_price(ticker, k):
	#ticker : 목표로 하는 코인(정해야됨)
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") #시작시간 : 09시
        end_time = start_time + datetime.timedelta(days=1) #마감시간 : 다음날 09시

        if start_time < now < end_time - datetime.timedelta(seconds=10):
	# 09:00:00 < 현재 < 08:59:50를 만족하면 아래 구문 작동
            target_price = get_target_price("KRW-BTC", 0.5) #변동성돌파전략 설정 ################
	#매수목표가
            current_price = get_current_price("KRW-BTC")
	#현재가격
            if target_price < current_price:
	#목표가격보다 현재가격이 높으면, 
                krw = get_balance("KRW")
	#이때 내 원화 잔고(krw)를 조회하고 
                if krw > 5000:
	#거래최소금액인 5000원이 넘으면
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
	#구매를 한다. 이때 수수료 0.05%를 고려해 *0.9995를 곱한다.
        else:
	#만약 현재 시간이 08:59:50~09:00:00이면
            btc = get_balance("BTC")
	#현재 가진 코인을 전량 매도한다.
            if btc > 0.00008:
	#설명영상이 제작됐을 당시 0.00008btc가 최소거래금액인 5000원정도였는데,
	#내가 가진 코인의 합산금액이 최소거래금액 이상이면
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
	#계속 전량 매도한다.
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)

# ################가 있는 줄의 타겟프라이스와 k값을 입맛에 맞게 고치면 새로운 코드가 됨.