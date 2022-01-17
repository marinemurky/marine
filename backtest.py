import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-BTC", count=7)
#OHLCV(당일 open(시가) high(고가) low(저가) close(종가) volume(거래량) 데이터)  
#count=7은 7일치의 OHLCV 데이터를 get해오는 것.

df['range'] = (df['high'] - df['low']) * 0.5
#변동폭 * K(K=상수, 0.5로 설정)만큼 상승이 일어났을 때 매수 진행
#변동폭 = 어제의 고가(high) - 어제의 저가(low)
#이렇게 해서 어제의 매수가격(이 가격으로 매수하는게 아님)인 range 도출

df['target'] = df['open'] + df['range'].shift(1)
#8번줄에서 구한 range값은 전날 매수가격임. 오늘 매수가격을 정하려면 .shift(1)로
#컬럼을 1칸 내려서 오늘로 보정해줌. 여기에서 시가 open을 더해 13번 줄의 매수가격(target)을 확정함

#fee = 0.0032 #수수료, 현재 코드는 빗썸 api 코드라서 업비트 수수료가 아닌 빗썸 수수료로 돼있음
#업비트 수수료 확인되는대로 17번줄에 'fee = 업비트 수수료'를 입력, 20번 줄 주석을 제거해야 함. 
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'], #- fee,
                     1)
#ror = 수익률. np.where라는 구문은 조건문, 참일때 값, 거짓일때 값 이렇게 3가지 인자를 받음.
# 조건이 참이면 참일때 값, 거짓이면 거짓일때 값을 출력함. 
# 여기서 조건문은 high. 19번 줄에서 고가인 high가 타겟값보다 높으면, 매수가 진행된 상황.
# 이게 참이라면 20번줄로 가서 종가 close / 타겟값을 해서 수익률을 구하게 됨.
# 만약 조건문이 거짓(타겟값이 고가보다 높으면 매수 진행이 안된 상황)이면 거래가 일어나지 않았으므로
# 수익률은 그대로 1 유지.( 21번줄의 1) )

df['hpr'] = df['ror'].cumprod()
#누적곱계산(cumprod) 수익률을 곱해서 누적수익률을 구함.

df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
#하락폭계산(drawdown) 누적최댓값과 현재 HPR 차이를 구해서 누적최댓값으로 나눈뒤 100을 곱함.

print("MDD(%): ", df['dd'].max())
#drawdown값 중 제일 최댓값

df.to_excel("dd.xlsx")
#엑셀로 저장