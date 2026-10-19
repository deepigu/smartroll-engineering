
def calculate_material(
    width, thickness, length, quantity,
    density, price_per_kg, waste_percent
):
    # Convert millimeters to meters
    width_m = width / 1000
    thickness_m = thickness / 1000

    # Calculate finished material length
    total_length = length * quantity

    # Calculate material volume
    volume = width_m * thickness_m * total_length

    # Calculate finished material weight
    weight = volume * density

    # Calculate material loss allowance
    waste_fraction = waste_percent / 100

    # Calculate gross material requirements
    gross_weight = weight / (1 - waste_fraction)
    gross_length = total_length / (1 - waste_fraction)

    # Calculate waste material weight
    waste_weight = gross_weight - weight

    # Calculate estimated material cost
    total_cost = gross_weight * price_per_kg

    return {
        "total_length": round(total_length, 2),
        "gross_length": round(gross_length, 2),
        "net_weight": round(weight, 2),
        "gross_weight": round(gross_weight, 2),
        "waste_weight": round(waste_weight, 2),
        "total_cost": round(total_cost, 2)
    }
