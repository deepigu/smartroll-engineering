
from optimizer import optimize_coils

result = optimize_coils(
    required_weight=20846.84,
    price_per_kg=1.20
)

print("SMARTROLL - COIL OPTIMIZATION")
print("-----------------------------")

for option in result["options"]:
    print("\nCoil:", option["coil_name"])
    print("Coils Needed:", option["coils_needed"])
    print("Purchased Weight:", option["purchased_weight"], "kg")
    print("Remaining Weight:", option["remaining_weight"], "kg")
    print("Purchase Cost: $", option["total_cost"])

print("\nBEST OPTION")
print(result["best_option"]["coil_name"])
