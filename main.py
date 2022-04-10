import json


def main():
    p1 = Orders([1122, 1123])  # input order ids here
    p1.process_orders()


class Orders:
    def __init__(self, id_arr: list):  # id_arr =[]
        self.order_ids = id_arr

    def process_orders(self):
        data = self.extract_json()
        input_ids = self.order_ids
        product_ids_map = self.map_product_ids(input_ids, data)
        final_val = self.iterate_through_mapped_list(product_ids_map, data)
        return set(final_val)

    def iterate_through_mapped_list(self, product_ids_map: list, data: list) -> list:
        for i in product_ids_map:
            order_id = i["orderId"]
            product_ids = i["productIds"]
            qty = i["qty"]
            j = 0
            while j < len(product_ids):
                try:
                    unfulfilled_orders = self.process_orders_next(
                        order_id, product_ids[j], data, qty[j]
                        )
                finally:
                    j += 1
        print(set(unfulfilled_orders))
        return unfulfilled_orders

    def process_orders_next(
            self, order_id: str, prod_ids: list, data: list, qty: int
            ) -> list:
        unfulfilled_orders = []
        product = self.query_to_json("productId", prod_ids, data["products"])
        stock_available = product[0]["quantityOnHand"]
        stock_threshold = product[0]["reorderThreshold"]
        order_qty = qty
        res_val = self.check_order_status(
            order_id, product, order_qty, stock_available, stock_threshold
            )
        if res_val:
            unfulfilled_orders.append(res_val)
        return unfulfilled_orders

    def check_order_status(
            self, order: str or int, product: list, qty: int, a: int, b: int
            ) -> int:
        if a > qty:  # if stock is above ordered qty  fulfil the order
            product[0]["quantityOnHand"] = product[0]["quantityOnHand"] - qty
            print("Stock quantity decreased successfully")
            print(product)
            self.change_order_status(order, "fulfilled")
        else:
            product[0]["quantityOnHand"] = product[0]["quantityOnHand"]
            self.change_order_status(order, "unfulfilled")
            return order
        if a < b:
            self.purchase_order()

    def change_order_status(self, order_id: int, status_message: str) -> None:
        data = self.extract_json()
        order = self.query_to_json("orderId", order_id, data["orders"])
        order[0]["status"] = status_message
        print("Order Status Changed")
        print(order)

    def map_product_ids(self, input_id_arr: list, data_dom: list) -> list:
        mapped_array = []
        orders_all = self.get_all_orders(input_id_arr, data_dom)
        for i in orders_all:
            product_ids_map = {"orderId": i[0]["orderId"]}
            prod_arr = []
            qty_arr = []
            for x in i[0]["items"]:
                prod_arr.append(x["productId"])
                qty_arr.append(x["quantity"])
            product_ids_map["productIds"] = prod_arr
            product_ids_map["qty"] = qty_arr
            mapped_array.append(product_ids_map)
        return mapped_array

    def get_all_orders(self, input_arr: list, data_dom: list) -> list:
        orders_all = []
        for i in input_arr:
            orders = self.query_to_json("orderId", i, data_dom["orders"])
            orders_all.append(orders)
        return orders_all

    @staticmethod
    def query_to_json(k: any, val: any, domain: list) -> list:
        val = list(filter(lambda x: x[k] == val, domain))
        return val

    @staticmethod
    def extract_json():
        f = open("data.json")
        data = json.load(f)
        return data

    @staticmethod
    def purchase_order() -> bool:
        return True


if __name__ == "__main__":
    main()
