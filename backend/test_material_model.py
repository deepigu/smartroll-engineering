
from material_model import Material

steel = Material(
    "Carbon Steel",
    "ASTM A1008 CS Type B",
    7850,
    1.20
)

aluminum = Material(
    "Aluminum",
    "5052-H32",
    2680,
    3.80
)

print("FIRST MATERIAL")
steel.display_info()

print("\nSECOND MATERIAL")
aluminum.display_info()
