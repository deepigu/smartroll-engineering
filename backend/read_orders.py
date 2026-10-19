
from database import get_connection


def read_orders():

    with get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT order_id, material_code, machine_code, quantity, part_length FROM production_orders"
            )

            orders = cursor.fetchall()

            for order in orders:
                print("------------------------")
                print("Order ID:", order[0])
                print("Material:", order[1])
                print("Machine:", order[2])
                print("Quantity:", order[3])
                print("Part Length:", order[4])


read_orders()
