import pyupbit

access = "XSLSnoA0exVbeHoVBXwmWNrRekw1xKZzU0qQ1pbP"          # 본인 값으로 변경
secret = "24dfzujs8xe8I5uoiwupxJNJhXewAQSKKm4kRrvH"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회