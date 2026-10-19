
class ProductionOrder:

    def __init__(
        self,
        order_id,
        material_code,
        machine_code,
        quantity,
        part_length
    ):
        self.order_id = order_id
        self.material_code = material_code
        self.machine_code = machine_code
        self.quantity = quantity
        self.part_length = part_length

    def total_length(self):
        return self.quantity * self.part_length

    def display_order(self):
        print("Order ID:", self.order_id)
        print("Material:", self.material_code)
        print("Machine:", self.machine_code)
        print("Quantity:", self.quantity)
        print("Part Length:", self.part_length, "m")
        print("Total Length:", self.total_length(), "m")
