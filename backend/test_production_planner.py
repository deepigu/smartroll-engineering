
import math

import pytest

from production_planner import plan_production


# ---------------------------------------
# SAMPLE PRODUCTION INPUTS
# ---------------------------------------

def sample_inputs():
    return {
        "quantity": 1500,
        "part_length_m": 2.5,
        "strip_width_mm": 400,
        "thickness_mm": 1.5,
        "density": 7850,
        "price_per_kg": 1.5,
        "production_speed_m_min": 20,
        "setup_time_min": 30,
        "waste_percentage": 5,
    }


# ---------------------------------------
# TEST 1: BASIC PRODUCTION CALCULATION
# ---------------------------------------

def test_production_calculation():
    result = plan_production(**sample_inputs())

    assert result["quantity"] == 1500
    assert result["total_length_m"] == 3750.0
    assert result["net_weight_kg"] == 17662.5
    assert result["gross_weight_kg"] == 18592.11
    assert result["estimated_waste_kg"] == 929.61
    assert result["material_cost"] == 27888.16


# ---------------------------------------
# TEST 2: PRODUCTION TIME
# ---------------------------------------

def test_production_time():
    result = plan_production(**sample_inputs())

    assert result["run_time_min"] == 187.5
    assert result["setup_time_min"] == 30
    assert result["total_time_min"] == 217.5
    assert result["total_time_hours"] == 3.62
    assert result["estimated_shifts_8h"] == 1


# ---------------------------------------
# TEST 3: ZERO WASTE
# ---------------------------------------

def test_zero_waste():
    inputs = sample_inputs()
    inputs["waste_percentage"] = 0

    result = plan_production(**inputs)

    assert result["gross_weight_kg"] == result["net_weight_kg"]
    assert result["estimated_waste_kg"] == 0


# ---------------------------------------
# TEST 4: INVALID QUANTITY
# ---------------------------------------

@pytest.mark.parametrize("quantity", [0, -1, 1.5])
def test_invalid_quantity(quantity):
    inputs = sample_inputs()
    inputs["quantity"] = quantity

    with pytest.raises(ValueError):
        plan_production(**inputs)


# ---------------------------------------
# TEST 5: INVALID DIMENSIONS
# ---------------------------------------

@pytest.mark.parametrize(
    "field",
    [
        "part_length_m",
        "strip_width_mm",
        "thickness_mm",
        "density",
        "production_speed_m_min",
    ],
)
def test_invalid_dimensions(field):
    inputs = sample_inputs()
    inputs[field] = 0

    with pytest.raises(ValueError):
        plan_production(**inputs)


# ---------------------------------------
# TEST 6: INVALID WASTE PERCENTAGE
# ---------------------------------------

@pytest.mark.parametrize("waste", [-1, 100, 110])
def test_invalid_waste(waste):
    inputs = sample_inputs()
    inputs["waste_percentage"] = waste

    with pytest.raises(ValueError):
        plan_production(**inputs)


# ---------------------------------------
# TEST 7: INVALID NEGATIVE COST
# ---------------------------------------

def test_negative_price():
    inputs = sample_inputs()
    inputs["price_per_kg"] = -5

    with pytest.raises(ValueError):
        plan_production(**inputs)


# ---------------------------------------
# TEST 8: INVALID SETUP TIME
# ---------------------------------------

def test_negative_setup_time():
    inputs = sample_inputs()
    inputs["setup_time_min"] = -10

    with pytest.raises(ValueError):
        plan_production(**inputs)


# ---------------------------------------
# TEST 9: NON-FINITE INPUT
# ---------------------------------------

@pytest.mark.parametrize(
    "invalid_value",
    [math.nan, math.inf, -math.inf],
)
def test_non_finite_values(invalid_value):
    inputs = sample_inputs()
    inputs["density"] = invalid_value

    with pytest.raises(ValueError):
        plan_production(**inputs)


# ---------------------------------------
# TEST 10: EIGHT-HOUR SHIFT BOUNDARY
# ---------------------------------------

def test_shift_calculation():
    inputs = sample_inputs()
    inputs["quantity"] = 4000

    result = plan_production(**inputs)

    assert result["estimated_shifts_8h"] == 2
