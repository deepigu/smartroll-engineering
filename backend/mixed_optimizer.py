
import math


def optimize_mixed_coils(required_weight, price_per_kg):

    if required_weight <= 0:
        raise ValueError("Required weight must be positive.")

    if price_per_kg < 0:
        raise ValueError("Price cannot be negative.")

    small_size = 3000
    medium_size = 5000
    large_size = 8000

    best_option = None

    max_small = math.ceil(required_weight / small_size)
    max_medium = math.ceil(required_weight / medium_size)
    max_large = math.ceil(required_weight / large_size)

    for small in range(max_small + 1):
        for medium in range(max_medium + 1):

            weight_so_far = (
                small * small_size
                + medium * medium_size
            )

            remaining_needed = max(
                0,
                required_weight - weight_so_far
            )

            large = math.ceil(
                remaining_needed / large_size
            )

            purchased_weight = (
                weight_so_far + large * large_size
            )

            remaining_weight = (
                purchased_weight - required_weight
            )

            total_cost = (
                purchased_weight * price_per_kg
            )

            option = {
                "small_coils": small,
                "medium_coils": medium,
                "large_coils": large,
                "purchased_weight": purchased_weight,
                "remaining_weight": round(
                    remaining_weight, 2
                ),
                "total_cost": round(total_cost, 2)
            }

            if best_option is None:
                best_option = option

            elif total_cost < best_option["total_cost"]:
                best_option = option

    return best_option
