
import unittest

from production_order import ProductionOrder
from material_model import Material
from machine_model import Machine


class TestSmartRoll(unittest.TestCase):

    def test_total_length(self):
        order = ProductionOrder(
            "ORD1001",
            "cs_type_b",
            "RF100",
            5000,
            2
        )

        self.assertEqual(order.total_length(), 10000)

    def test_material_name(self):
        steel = Material(
            "Carbon Steel",
            "ASTM A1008 CS Type B",
            7850,
            1.20
        )

        self.assertEqual(steel.name, "Carbon Steel")

    def test_machine_max_width(self):
        machine = Machine(
            "SmartRoll Demo RF100",
            0.5,
            2.0,
            500
        )

        self.assertEqual(machine.max_width, 500)


if __name__ == "__main__":
    unittest.main()
