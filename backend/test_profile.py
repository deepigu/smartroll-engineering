
from profile import calculate_c_channel_flat_width

result = calculate_c_channel_flat_width(
    web_mm=100,
    flange_mm=40,
    thickness_mm=1.5,
    inside_radius_mm=2,
    k_factor=0.4
)

print("SMARTROLL - C CHANNEL ESTIMATE")
print("------------------------------")
print("Flat Width:", result["flat_width_mm"], "mm")
print("Bend Allowance:", result["bend_allowance_mm"], "mm")
print("Bend Deduction:", result["bend_deduction_mm"], "mm")
