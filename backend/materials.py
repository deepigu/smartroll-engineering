
materials = {
    "cs_type_b": {
        "name": "Cold Rolled Carbon Steel",
        "grade": "ASTM A1008 CS Type B",
        "density": 7850,
        "price_per_kg": 1.20,

        "yield_strength_min_mpa": None,
        "yield_strength_max_mpa": None,
        "tensile_strength_mpa": None,
        "strength_data_type": "not_guaranteed",
        "typical_yield_range_mpa": [140, 275],
        "strength_source": (
            "ASTM A1008 typical nonmandatory "
            "mechanical property table"
        )
    },

    "galvanized_cs": {
        "name": "Galvanized Carbon Steel",
        "grade": "ASTM A653 CS Type B",
        "density": 7850,
        "price_per_kg": 1.50,

        "yield_strength_min_mpa": None,
        "yield_strength_max_mpa": None,
        "tensile_strength_mpa": None,
        "strength_data_type": "not_guaranteed",
        "typical_yield_range_mpa": [205, 380],
        "strength_source": (
            "Tata Steel ASTM A653 CS Type B "
            "typical mechanical properties"
        )
    },

    "ss304": {
        "name": "Stainless Steel",
        "grade": "AISI 304",
        "density": 8000,
        "price_per_kg": 4.50,

        "yield_strength_min_mpa": 205,
        "yield_strength_max_mpa": None,
        "tensile_strength_mpa": 515,
        "strength_data_type": "published_minimum",
        "material_condition": "Annealed",
        "strength_source": (
            "AZoM Stainless Steel Grade 304 "
            "mechanical properties"
        )
    },

    "al5052": {
        "name": "Aluminum",
        "grade": "5052-H32",
        "density": 2680,
        "price_per_kg": 3.80,

        "yield_strength_min_mpa": None,
        "yield_strength_max_mpa": None,
        "tensile_strength_mpa": 230,
        "typical_yield_strength_mpa": 195,
        "strength_data_type": "typical",
        "material_condition": "H32 temper",
        "strength_source": (
            "ASM International Properties of "
            "Wrought Aluminum and Aluminum Alloys"
        )
    }
}


def get_material(material_code):
    return materials.get(material_code)
