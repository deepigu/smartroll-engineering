
import math


COIL_OPTIONS = [
    {"name": "Small Coil", "weight": 3000},
    {"name": "Medium Coil", "weight": 5000},
    {"name": "Large Coil", "weight": 8000}
]


def optimize_coils(required_weight, price_per_kg):
    if not math.isfinite(required_weight) or required_weight <= 0:
        raise ValueError(
            "Required weight must be a positive finite number."
        )

    if not math.isfinite(price_per_kg) or price_per_kg < 0:
        raise ValueError(
            "Price per kg must be a non-negative finite number."
        )

    results = []

    # Compare single coil sizes
    for coil in COIL_OPTIONS:
        coil_weight = coil["weight"]

        coils_needed = math.ceil(
            required_weight / coil_weight
        )

        purchased_weight = coils_needed * coil_weight
        remaining_weight = purchased_weight - required_weight
        total_cost = purchased_weight * price_per_kg

        utilization = (
            required_weight / purchased_weight
        ) * 100

        results.append({
            "coil_name": coil["name"],
            "coil_weight_kg": coil_weight,
            "coils_needed": coils_needed,
            "purchased_weight": purchased_weight,
            "remaining_weight": round(remaining_weight, 2),
            "utilization_percentage": round(utilization, 2),
            "total_cost": round(total_cost, 2)
        })

    best_option = min(
        results,
        key=lambda option: (
            option["total_cost"],
            option["coils_needed"]
        )
    )

    # Compare combinations of different coil sizes
    # For these demo coil weights, all sizes are multiples
    # of 1000 kg. Search for the smallest feasible total.
    unit_kg = math.gcd(
        *(coil["weight"] for coil in COIL_OPTIONS)
    )

    target_units = math.ceil(
        required_weight / unit_kg
    )

    max_coil_units = max(
        coil["weight"] // unit_kg
        for coil in COIL_OPTIONS
    )

    # A feasible solution always exists within this range
    max_units = target_units + max_coil_units - 1

    # dp[weight] stores the best combination at that weight
    # using the fewest coils
    dp = [None] * (max_units + 1)
    dp[0] = [0] * len(COIL_OPTIONS)

    for weight_units in range(1, max_units + 1):
        for index, coil in enumerate(COIL_OPTIONS):
            coil_units = coil["weight"] // unit_kg

            if weight_units < coil_units:
                continue

            previous = dp[weight_units - coil_units]

            if previous is None:
                continue

            candidate = previous.copy()
            candidate[index] += 1

            if (
                dp[weight_units] is None
                or sum(candidate) < sum(dp[weight_units])
            ):
                dp[weight_units] = candidate

    best_mix = None

    for weight_units in range(target_units, max_units + 1):
        counts = dp[weight_units]

        if counts is None:
            continue

        purchased_weight = weight_units * unit_kg
        coils_needed = sum(counts)

        candidate_key = (
            purchased_weight * price_per_kg,
            purchased_weight,
            coils_needed
        )

        if (
            best_mix is None
            or candidate_key < best_mix["_sort_key"]
        ):
            best_mix = {
                "_sort_key": candidate_key,
                "coil_combination": [
                    {
                        "coil_name": coil["name"],
                        "coil_weight_kg": coil["weight"],
                        "quantity": counts[index]
                    }
                    for index, coil in enumerate(COIL_OPTIONS)
                    if counts[index] > 0
                ],
                "total_coils": coils_needed,
                "purchased_weight": purchased_weight,
                "remaining_weight": round(
                    purchased_weight - required_weight, 2
                ),
                "utilization_percentage": round(
                    required_weight / purchased_weight * 100,
                    2
                ),
                "total_cost": round(
                    purchased_weight * price_per_kg, 2
                )
            }

    if best_mix is not None:
        best_mix.pop("_sort_key")

    return {
        "required_weight": round(required_weight, 2),
        "price_per_kg": price_per_kg,
        "options": results,
        "best_option": best_option,
        "best_mixed_option": best_mix,
        "assumptions": [
            "Coil sizes are demonstration inventory options.",
            "All coil sizes use the same price per kilogram.",
            "Remaining material is reusable inventory, "
            "not necessarily manufacturing scrap.",
            "Coil width, grade, tooling, changeover costs, "
            "and supplier constraints are not modeled."
        ]
    }


if __name__ == "__main__":
    result = optimize_coils(
        required_weight=11000,
        price_per_kg=1.50
    )

    print("SMARTROLL COIL OPTIMIZATION")
    print("---------------------------")

    print("\nSingle-size options:")
    for option in result["options"]:
        print(option)

    print("\nBest single-size option:")
    print(result["best_option"])

    print("\nBest mixed-coil option:")
    print(result["best_mixed_option"])
