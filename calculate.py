from client import Client

def load_cookies(filename: str) -> dict:
    with open(filename, "r") as f:
        cookies_raw = f.read()

        cookies = {}
        for line in cookies_raw.split(";"):
            key, value = line.split("=")
            cookies[key] = value

        return cookies

print("Loading cookies")
cookies = load_cookies("cookie.txt")
print("Cookies loaded\n")

client = Client(cookies)
orders = client.get_orders()

total = 0
annual = 0

yearly_spend = {}

for order in orders:

    if order.cancelledAt:
        continue

    total += order.grandTotal.unitAmount

    order_year = order.createdAt.split("-")[0]

    if order_year not in yearly_spend:
        yearly_spend[order_year] = 0
    else:
        yearly_spend[order_year] += order.grandTotal.unitAmount

print("\nSpending by year:")

for year, spend in yearly_spend.items():
    print(f"{year}: ${spend / 100}")

print(f"\nTotal: ${total / 100}")
