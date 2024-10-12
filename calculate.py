import csv
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

    d = datetime.datetime.strptime(order.createdAt, "%Y-%m-%dT%H:%M:%S.%fZ")

    order_year = d.strftime("%Y")
    order_month = d.strftime("%m")
    order_day = d.strftime("%d")

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

csv_response = input("\nWould you like to save this data to a CSV file? Y/N: ")

if csv_response.lower() == "y":
    with open("doordash_spending.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Year", "Month", "Day", "Total"])

        for year, months in yearly_spend.items():
            for month, days in months.items():
                for day, total in days.items():
                    month_name = datetime.datetime.strptime(month, "%m").strftime("%B")
                    writer.writerow([year, month_name, day, total / 100])

    print("Data saved to doordash_spending.csv")

print("\nDone!")