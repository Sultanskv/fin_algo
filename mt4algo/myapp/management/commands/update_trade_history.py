import asyncio
from datetime import timedelta, datetime
from django.utils import timezone
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
import httpx
from myapp.models import TradeHistory, ClientDetail  # Apne project structure ke hisaab se adjust karein

# REST API base URL – apne account region ke hisaab se update karein.
REST_BASE_URL = "https://mt-client-api-v1.london-a.agiliumtrade.ai"

async def fetch_deals_by_position(account_id, position_id, token):
    """
    MetaApi REST endpoint se closed deals fetch karta hai for a given position.
    (Endpoint: /users/current/accounts/{accountId}/history-deals/position/{positionId})
    """
    url = f"{REST_BASE_URL}/users/current/accounts/{account_id}/history-deals/position/{position_id}"
    headers = {
        "Accept": "application/json",
        "auth-token": token
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

def parse_datetime(dt_str):
    """
    ISO datetime string (jo 'Z' se end ho sakta hai) ko Python datetime object mein convert karta hai.
    """
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

async def update_trade_for_client(client):
    """
    Har client ke liye:
      - ClientDetail se account id aur token lekar,
      - Pichle 4 dino ke un TradeHistory records ko fetch karta hai jinke exit_time blank hain,
      - Har record ke liye, position id (jo hum assume karte hain ki trade.ticket_id ke barabar hai)
        se closed deals fetch karta hai using fetch_deals_by_position.
      - List mein se "entryType" == "DEAL_ENTRY_OUT" record ko chunta hai aur uske "time", "price"
        aur "profit" fields se exit_time, exit_price aur p_l update karta hai.
    """
    account_id = client.MataApi_ACCOUNT_ID
    token = client.MataApi_TOKEN
    cutoff = timezone.now() - timedelta(days=4)
    trades = await sync_to_async(list)(
        TradeHistory.objects.filter(
            client=client,
            ticket_id__isnull=False,
            exit_time__isnull=True,
            signal_time__gte=cutoff
        )
    )
    if not trades:
        print(f"No trades to update for client {client.user_id}")
    for trade in trades:
        print(f"Fetching deals for position (ticket) {trade.ticket_id} for client {client.user_id}")
        data = []
        try:
            data = await fetch_deals_by_position(account_id, trade.ticket_id, token)
        except Exception as e:
            print(f"Error fetching deals by position for ticket {trade.ticket_id}: {e}")
            continue

        if data:
            selected_record = None
            for record in data:
                # Chunte hain exit deal record
                if record.get("entryType") == "DEAL_ENTRY_OUT":
                    selected_record = record
                    break

            if not selected_record:
                print(f"No exit record (DEAL_ENTRY_OUT) found for position {trade.ticket_id}. Full data: {data}")
                continue

            # Update record fields
            trade.exit_time = parse_datetime(selected_record.get("time"))
            exit_price = selected_record.get("price") or selected_record.get("currentPrice")
            if exit_price is None:
                print(f"Exit price not found for ticket {trade.ticket_id} in record: {selected_record}")
                continue
            trade.exit_price = exit_price
            profit = selected_record.get("profit")
            if profit is None:
                print(f"Profit not found for ticket {trade.ticket_id} in record: {selected_record}")
                profit = 0.0
            trade.p_l = profit
            await sync_to_async(trade.save)()
            print(f"Updated trade {trade.ticket_id} for client {client.user_id}: exit_price={exit_price}, p_l={profit}")
        else:
            print(f"No deal data found for ticket {trade.ticket_id} for client {client.user_id}")


async def main():
    # Sabhi aise clients jinke MetaApi credentials available hain.
    clients = await sync_to_async(list)(
        ClientDetail.objects.filter(
            MataApi_ACCOUNT_ID__isnull=False,
            MataApi_TOKEN__isnull=False
        )
    )
    if not clients:
        print("No clients with valid MetaApi credentials found.")
        return
    await asyncio.gather(*(update_trade_for_client(client) for client in clients))

class Command(BaseCommand):
    help = ("Update TradeHistory records with closed trade details (exit_time, exit_price, profit) "
            "fetched via MetaApi REST API using deals by position endpoint for trades in the last 4 days.")

    def handle(self, *args, **options):
        asyncio.run(main())


