
from mixed_optimizer import optimize_mixed_coils

result = optimize_mixed_coils(
    required_weight=100000,
    price_per_kg=1.20
)

print("SMARTROLL - MIXED COIL OPTIMIZATION")
print("-----------------------------------")

print("Small Coils:", result["small_coils"])
print("Medium Coils:", result["medium_coils"])
print("Large Coils:", result["large_coils"])

print("Purchased Weight:", result["purchased_weight"], "kg")
print("Remaining Weight:", result["remaining_weight"], "kg")
print("Total Cost: $", result["total_cost"])
