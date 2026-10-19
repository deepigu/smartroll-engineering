
from materials import materials
from machines import get_machine


def recommend_materials(
    max_price,
    max_density,
    machine_code=None,
    thickness_mm=None,
    strip_width_mm=None,
    min_yield_strength_mpa=None
):
    recommendations = []

    # Validate material requirements
    if max_price <= 0:
        raise ValueError(
            "Maximum price must be greater than zero."
        )

    if max_density <= 0:
        raise ValueError(
            "Maximum density must be greater than zero."
        )

    if (
        min_yield_strength_mpa is not None
        and min_yield_strength_mpa <= 0
    ):
        raise ValueError(
            "Minimum yield strength must be positive."
        )

    # Validate machine requirements
    if machine_code is not None:

        machine = get_machine(machine_code)

        if machine is None:
            raise ValueError(
                f"Machine '{machine_code}' was not found."
            )

        if thickness_mm is None or strip_width_mm is None:
            raise ValueError(
                "Thickness and strip width are required "
                "when selecting a machine."
            )

        if thickness_mm <= 0 or strip_width_mm <= 0:
            raise ValueError(
                "Thickness and strip width must be positive."
            )

        if thickness_mm < machine["min_thickness"]:
            raise ValueError(
                f"{machine['name']} requires a minimum "
                f"thickness of {machine['min_thickness']} mm. "
                f"Requested: {thickness_mm} mm."
            )

        if thickness_mm > machine["max_thickness"]:
            raise ValueError(
                f"{machine['name']} supports a maximum "
                f"thickness of {machine['max_thickness']} mm. "
                f"Requested: {thickness_mm} mm."
            )

        if strip_width_mm > machine["max_strip_width"]:
            raise ValueError(
                f"{machine['name']} supports a maximum "
                f"strip width of {machine['max_strip_width']} mm. "
                f"Requested: {strip_width_mm} mm."
            )

    # Filter materials
    for code, material in materials.items():

        price = material["price_per_kg"]
        density = material["density"]

        if price > max_price or density > max_density:
            continue

        # Only use documented minimum yield strengths
        if min_yield_strength_mpa is not None:

            strength_type = material.get(
                "strength_data_type"
            )

            yield_strength = material.get(
                "yield_strength_min_mpa"
            )

            if strength_type != "published_minimum":
                continue

            if yield_strength is None:
                continue

            if yield_strength < min_yield_strength_mpa:
                continue

        recommendations.append({
            "material_code": code,
            "name": material["name"],
            "grade": material["grade"],
            "density": density,
            "price_per_kg": price,
            "yield_strength_min_mpa": material.get(
                "yield_strength_min_mpa"
            ),
            "tensile_strength_mpa": material.get(
                "tensile_strength_mpa"
            ),
            "strength_data_type": material.get(
                "strength_data_type"
            ),
            "strength_source": material.get(
                "strength_source"
            )
        })

    # Cheapest matching materials first
    recommendations.sort(
        key=lambda item: item["price_per_kg"]
    )

    return recommendations


if __name__ == "__main__":

    try:
        results = recommend_materials(
            max_price=5.0,
            max_density=8500,
            machine_code="RF100",
            thickness_mm=1.5,
            strip_width_mm=400,
            min_yield_strength_mpa=200
        )

        print("SMARTROLL STRENGTH RECOMMENDATIONS")
        print("----------------------------------")

        for material in results:
            print(
                material["name"],
                "- Yield Strength:",
                material["yield_strength_min_mpa"],
                "MPa"
            )

        if not results:
            print("No matching materials found.")

    except ValueError as error:
        print("Validation Error:", error)
