# main.py

import asyncio
from ib_insync import IB
from strategies import check_moving_averages, check_gap_breakdown, check_gap_and_alert

async def main():
    ib = IB()
    await ib.connectAsync('127.0.0.1', 7497, clientId=1)

    symbols = ['SPY', 'QQQ']
    for sym in symbols:
        await check_moving_averages(ib, sym)
        await check_gap_and_alert(ib, sym)
        await check_gap_breakdown(ib, sym)

    ib.disconnect()  # <-- corregido aquí

if __name__ == "__main__":
    asyncio.run(main())
