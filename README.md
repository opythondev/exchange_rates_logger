### Simple currency exchange logger
Gets data currency rates from REST API

Calculates 3 step exchange profitability

Ex.:
1. USD -> GBP
2. GBP -> EUR
3. EUR -> USD

If calc result > 1 == profit found

Returns calculation result in telegram message

---
1. Clone project
2. Install requirements
3. Create .env
4. Set BOT_API_KEY == telegram bot api key
5. Set CHAT_ID == telegram user_id or group_id
6. Run monitor.py