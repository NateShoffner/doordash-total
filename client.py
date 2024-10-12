import requests

from orders import GetConsumerOrdersWithDetail, Model, build_payload


class Client:

    def __init__(self, cookies: dict):
        self.headers = {
            "content-type": "application/json",
            "origin": "https://www.doordash.com",
            "referer": "https://www.doordash.com/",
            "accept-language": "en-US,en;q=0.9",
            "accept-encoding": "gzip, deflate",
            "referer": "https://www.doordash.com/orders",
        }
        self.cookies = cookies

    def get_orders(self) -> list[GetConsumerOrdersWithDetail]:
        url = "https://www.doordash.com/graphql/getConsumerOrdersWithDetails?operation=getConsumerOrdersWithDetails"

        all_orders = []

        offset = 0
        limit = 10
        while True:
            payload = build_payload(offset, limit)
            print(f"Requesting orders {offset} to {offset + limit}")
            response = requests.request(
                "POST", url, headers=self.headers, cookies=self.cookies, data=payload
            )

            orders = Model.parse_raw(response.text)
            if not orders.data.getConsumerOrdersWithDetails:
                print("No more orders")
                break

            all_orders.extend(orders.data.getConsumerOrdersWithDetails)
            offset += limit

        return all_orders
