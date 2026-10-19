
import math


def calculate_c_channel_flat_width(
    web_mm,
    flange_mm,
    thickness_mm,
    inside_radius_mm,
    k_factor=0.4
):
    if min(web_mm, flange_mm, thickness_mm) <= 0:
        raise ValueError("Dimensions must be positive")

    if inside_radius_mm < 0:
        raise ValueError("Inside radius cannot be negative")

    if not 0 < k_factor < 1:
        raise ValueError("K-factor must be between 0 and 1")

    # Two 90-degree bends
    bend_angle_rad = math.radians(90)

    # Bend allowance for one bend
    bend_allowance = bend_angle_rad * (
        inside_radius_mm + k_factor * thickness_mm
    )

    # Outside setback for a 90-degree bend
    outside_setback = inside_radius_mm + thickness_mm

    # Bend deduction for one bend
    bend_deduction = 2 * outside_setback - bend_allowance

    # Assumes web and flange dimensions are outside
    # virtual-sharp dimensions of a simple C-channel
    flat_width = (
        web_mm + 2 * flange_mm - 2 * bend_deduction
    )

    if flat_width <= 0:
        raise ValueError("Calculated flat width is invalid")

    return {
        "flat_width_mm": round(flat_width, 2),
        "bend_allowance_mm": round(bend_allowance, 2),
        "bend_deduction_mm": round(bend_deduction, 2)
    }
