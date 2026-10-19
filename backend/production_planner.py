
import math


def plan_production(
    quantity,
    part_length_m,
    strip_width_mm,
    thickness_mm,
    density,
    price_per_kg,
    production_speed_m_min,
    setup_time_min=30,
    waste_percentage=5
):
    values = [
        quantity,
        part_length_m,
        strip_width_mm,
        thickness_mm,
        density,
        price_per_kg,
        production_speed_m_min,
        setup_time_min,
        waste_percentage
    ]

    if not all(math.isfinite(value) for value in values):
        raise ValueError("All inputs must be finite numbers.")

    if quantity <= 0 or int(quantity) != quantity:
        raise ValueError("Quantity must be a positive whole number.")

    if any(value <= 0 for value in [
        part_length_m,
        strip_width_mm,
        thickness_mm,
        density,
        production_speed_m_min
    ]):
        raise ValueError(
            "Dimensions, density, and speed must be positive."
        )

    if price_per_kg < 0 or setup_time_min < 0:
        raise ValueError(
            "Price and setup time cannot be negative."
        )

    if not 0 <= waste_percentage < 100:
        raise ValueError(
            "Waste percentage must be between 0 and 100."
        )

    total_length_m = quantity * part_length_m

    # Convert millimetres to metres
    width_m = strip_width_mm / 1000
    thickness_m = thickness_mm / 1000

    volume_m3 = (
        total_length_m * width_m * thickness_m
    )

    net_weight_kg = volume_m3 * density

    # Waste is treated as a percentage of input material
    gross_weight_kg = (
        net_weight_kg / (1 - waste_percentage / 100)
    )

    estimated_waste_kg = gross_weight_kg - net_weight_kg

    material_cost = gross_weight_kg * price_per_kg

    run_time_min = (
        total_length_m / production_speed_m_min
    )

    total_time_min = run_time_min + setup_time_min

    return {
        "quantity": int(quantity),
        "total_length_m": round(total_length_m, 2),
        "net_weight_kg": round(net_weight_kg, 2),
        "gross_weight_kg": round(gross_weight_kg, 2),
        "estimated_waste_kg": round(estimated_waste_kg, 2),
        "material_cost": round(material_cost, 2),
        "run_time_min": round(run_time_min, 2),
        "setup_time_min": round(setup_time_min, 2),
        "total_time_min": round(total_time_min, 2),
        "total_time_hours": round(total_time_min / 60, 2),
        "estimated_shifts_8h": math.ceil(
            total_time_min / 480
        ),
        "assumptions": [
            "Production speed is constant.",
            "Part geometry is approximated using flat strip.",
            "Waste percentage represents input material loss.",
            "Downtime and changeovers beyond setup are excluded.",
            "Results are preliminary planning estimates."
        ]
    }


if __name__ == "__main__":
    result = plan_production(
        quantity=1500,
        part_length_m=2.5,
        strip_width_mm=400,
        thickness_mm=1.5,
        density=7850,
        price_per_kg=1.50,
        production_speed_m_min=20
    )

    print("SMARTROLL PRODUCTION PLAN")
    print("-------------------------")

    for key, value in result.items():
        print(f"{key}: {value}")
