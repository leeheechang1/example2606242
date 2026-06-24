import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from kiwoom_rest_api import KiwoomAPI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

APP_KEY = os.getenv("KIWOOM_APP_KEY")
APP_SECRET = os.getenv("KIWOOM_APP_SECRET")


class KiwoomTrader:
    def __init__(self, is_mock=False):
        self.api = KiwoomAPI(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            is_mock=is_mock,
        )

    def login(self):
        result = self.api.login()
        if self.api._client.access_token:
            print("[로그인 성공]")
        else:
            print(f"[로그인 실패] {result}")
            sys.exit(1)

    def logout(self):
        self.api.logout()
        print("[로그아웃]")

    def get_daily_chart(self, code="005930"):
        today = datetime.now().strftime("%Y%m%d")
        result = self.api.chart.stock_daily_chart(
            stk_cd=code, base_dt=today, upd_stkpc_tp="1"
        )
        return result.get("stk_dt_pole_chart_qry", [])

    def calc_ma(self, closes, window):
        ma = []
        for i in range(len(closes)):
            if i < window - 1:
                ma.append(None)
            else:
                ma.append(sum(closes[i - window + 1:i + 1]) / window)
        return ma

    def check_signal(self, closes):
        if len(closes) < 20:
            return "대기"

        ma5 = self.calc_ma(closes, 5)
        ma20 = self.calc_ma(closes, 20)

        today_ma5, today_ma20 = ma5[-1], ma20[-1]
        yesterday_ma5, yesterday_ma20 = ma5[-2], ma20[-2]

        if None in (today_ma5, today_ma20, yesterday_ma5, yesterday_ma20):
            return "대기"

        if yesterday_ma5 <= yesterday_ma20 and today_ma5 > today_ma20:
            return "매수"
        elif yesterday_ma5 >= yesterday_ma20 and today_ma5 < today_ma20:
            return "매도"
        return "대기"

    def buy(self, code, qty):
        result = self.api.order.buy_order(
            dmst_stex_tp="01",
            stk_cd=code,
            ord_qty=qty,
            trde_tp="01",
            ord_uv=0,
        )
        print(f"[매수 주문] {code} {qty}주 → {result}")
        return result

    def sell(self, code, qty):
        result = self.api.order.sell_order(
            dmst_stex_tp="01",
            stk_cd=code,
            ord_qty=qty,
            trde_tp="01",
            ord_uv=0,
        )
        print(f"[매도 주문] {code} {qty}주 → {result}")
        return result

    def run(self, code="005930", qty=1):
        print(f"=== 키움 자동매매 시작 ({code}) ===")
        print(f"모드: {'모의투자' if self.api._is_mock else '실전투자'}")
        print()

        self.login()

        print("[주가 데이터 조회 중...]")
        rows = self.get_daily_chart(code)
        if not rows:
            print("데이터 조회 실패")
            self.logout()
            return

        rows.reverse()
        closes = [int(row["cur_prc"]) for row in rows]

        print(f"조회 기간: {rows[0]['dt']} ~ {rows[-1]['dt']} ({len(rows)}일)")
        print(f"최근 종가: {closes[-1]:,}원")

        ma5 = self.calc_ma(closes, 5)
        ma20 = self.calc_ma(closes, 20)
        if ma5[-1]:
            print(f"MA5:  {ma5[-1]:,.0f}원")
        if ma20[-1]:
            print(f"MA20: {ma20[-1]:,.0f}원")

        signal = self.check_signal(closes)
        print(f"\n[신호] {signal}")

        if signal == "매수":
            self.buy(code, qty)
        elif signal == "매도":
            self.sell(code, qty)
        else:
            print("매매 신호 없음. 대기합니다.")

        self.logout()
        print("\n=== 완료 ===")


if __name__ == "__main__":
    trader = KiwoomTrader(is_mock=False)
    trader.run(code="005930", qty=1)
