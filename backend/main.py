
from calculator import calculate_material
from materials import materials, get_material
from machines import machines, get_machine
from compatibility import check_compatibility
from optimizer import optimize_coils
from profile import calculate_c_channel_flat_width
from validation import (
    get_positive_float,
    get_positive_integer,
    get_waste_percentage
)

print("======================================")
print("       SMARTROLL ENGINEERING")
print("======================================")

# STEP 1: Select material
print("\nAVAILABLE MATERIAL GRADES")

for code, material in materials.items():
    print(code, "-", material["grade"])

while True:
    material_code = input(
        "\nEnter material code: "
    ).strip().lower()

    selected_material = get_material(material_code)

    if selected_material is not None:
        break

    print("Invalid material code. Try again.")

# STEP 2: Select machine
print("\nAVAILABLE MACHINES")

for code, machine in machines.items():
    print(code, "-", machine["name"])

while True:
    machine_code = input(
        "\nEnter machine code: "
    ).strip().upper()

    selected_machine = get_machine(machine_code)

    if selected_machine is not None:
        break

    print("Invalid machine code. Try again.")

# STEP 3: Enter finished profile dimensions
print("\nENTER C-CHANNEL PROFILE DIMENSIONS")

while True:
    web = get_positive_float("Web dimension (mm): ")
    flange = get_positive_float("Each flange dimension (mm): ")
    thickness = get_positive_float("Thickness (mm): ")

    radius = get_positive_float("Inside bend radius (mm): ")

    try:
        profile_result = calculate_c_channel_flat_width(
            web_mm=web,
            flange_mm=flange,
            thickness_mm=thickness,
            inside_radius_mm=radius
        )

        break

    except ValueError as error:
        print("Profile error:", error)
        print("Please enter the profile dimensions again.")

# STEP 4: Enter production requirements
print("\nENTER PRODUCTION REQUIREMENTS")

length = get_positive_float("Part length (m): ")
quantity = get_positive_integer("Quantity (pieces): ")
waste_percent = get_waste_percentage("Estimated waste (%): ")

# STEP 5: Calculate material requirements
flat_width = profile_result["flat_width_mm"]

result = calculate_material(
    flat_width,
    thickness,
    length,
    quantity,
    selected_material["density"],
    selected_material["price_per_kg"],
    waste_percent
)

# STEP 6: Check machine limits
compatibility = check_compatibility(
    selected_machine,
    flat_width,
    thickness
)

# STEP 7: Optimize coil purchasing

optimization = optimize_coils(
    required_weight=result["gross_weight"],
    price_per_kg=selected_material["price_per_kg"]
)

# STEP 8: Print engineering report
print("\n======================================")
print("       SMARTROLL ENGINEERING REPORT")
print("======================================")

print("Material:", selected_material["name"])
print("Grade:", selected_material["grade"])
print("Machine:", selected_machine["name"])

print("\nPROFILE GEOMETRY")
print("--------------------------------------")
print("Web:", web, "mm")
print("Flange:", flange, "mm")
print("Thickness:", thickness, "mm")
print("Inside Radius:", radius, "mm")
print("Assumed K-Factor: 0.4")
print("Flat Strip Width:", flat_width, "mm")

print("\nMATERIAL ESTIMATE")
print("--------------------------------------")
print("Gross Coil Length:", result["gross_length"], "m")
print("Gross Material Weight:", result["gross_weight"], "kg")
print("Estimated Waste:", result["waste_weight"], "kg")
print("Estimated Cost: $", result["total_cost"])

print("\nMACHINE COMPATIBILITY")
print("--------------------------------------")
print("Status:", compatibility["status"])

for issue in compatibility["issues"]:
    print("WARNING:", issue)

if "message" in compatibility:
    print(compatibility["message"])

print("\nPRELIMINARY ESTIMATE")
print("Engineering validation required.")

print("\n======================================")
print("       COIL OPTIMIZATION REPORT")
print("======================================")

for option in optimization["options"]:
    print("\nCoil:", option["coil_name"])
    print("Coils Needed:", option["coils_needed"])
    print("Purchased Weight:", option["purchased_weight"], "kg")
    print("Remaining Material:", option["remaining_weight"], "kg")
    print("Purchase Cost: $", option["total_cost"])

best = optimization["best_option"]

print("\n--------------------------------------")
print("LOWEST-COST COIL OPTION")
print("--------------------------------------")
print("Coil:", best["coil_name"])
print("Number of Coils:", best["coils_needed"])
print("Total Purchase Cost: $", best["total_cost"])
print("Remaining Material:", best["remaining_weight"], "kg")

print("\nPRELIMINARY ESTIMATE")
print("Engineering and supplier validation required.")
