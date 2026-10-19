
from production_order import ProductionOrder

order1 = ProductionOrder(
    "ORD1001",
    "cs_type_b",
    "RF100",
    5000,
    2
)

print("SMARTROLL PRODUCTION ORDER")
print("--------------------------")

order1.display_order()
