import datetime
from client import Client
from tabulate import tabulate

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

yearly_spend = {} # {year: {month: {day: {total}}}}

for order in orders:
    if order.cancelledAt:
        continue

    total += order.grandTotal.unitAmount

    order_year, order_month, order_day = order.createdAt.split("-")

    if order_year not in yearly_spend:
        yearly_spend[order_year] = {}
    if order_month not in yearly_spend[order_year]:
        yearly_spend[order_year][order_month] = {}
    if order_day not in yearly_spend[order_year][order_month]:
        yearly_spend[order_year][order_month][order_day] = 0

    yearly_spend[order_year][order_month][order_day] += order.grandTotal.unitAmount

print("\nSpending by year:")

for year, months in yearly_spend.items():

    table = [["Month", "Total"]]

    print(f"\n{year}:")
    year_total = 0
    for month, days in months.items():
        month_name = datetime.datetime.strptime(month, "%m").strftime("%B")
        monthly_sum = sum(days.values())
        year_total += monthly_sum

        table.append([month_name, f"${monthly_sum / 100}"])

    print(tabulate(table, headers="firstrow", tablefmt="grid"))

    print(f"\n----------\nTotal: ${year_total / 100}")

print(f"\nTotal: ${total / 100}")
