# main.py

from ibkr_connection import connect_ibkr
from strategies import check_moving_averages, check_gap_breakdown

def main():
    ib = connect_ibkr()
    symbols = ['SPY', 'QQQ']
    for sym in symbols:
        check_moving_averages(ib, sym)
        check_gap_breakdown(ib, sym)
    ib.disconnect()

if __name__ == "__main__":
    main()
