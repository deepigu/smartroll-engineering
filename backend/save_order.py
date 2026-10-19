
from database import get_connection


def save_order(order_id, material_code, machine_code, quantity, part_length):

    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO production_orders
                (order_id, material_code, machine_code, quantity, part_length)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order_id, material_code, machine_code, quantity, part_length)
            )

    print("Production order saved successfully!")


save_order(
    order_id="ORD1002",
    material_code="ss304",
    machine_code="RF200",
    quantity=2000,
    part_length=3.0
)
