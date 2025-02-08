import time
from myapp.utils import fetch_positions_and_update_trades

# Continuously fetch positions every 10 seconds
while True:
    fetch_positions_and_update_trades()
    time.sleep(10)
