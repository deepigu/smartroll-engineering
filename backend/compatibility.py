
def check_compatibility(machine, width, thickness):
    issues = []

    if width <= 0 or thickness <= 0:
        raise ValueError("Width and thickness must be positive")

    if width > machine["max_strip_width"]:
        issues.append("Strip width exceeds machine limit")

    if thickness < machine["min_thickness"]:
        issues.append("Material is too thin for this machine")

    if thickness > machine["max_thickness"]:
        issues.append("Material is too thick for this machine")

    if issues:
        return {
            "status": "OUTSIDE_LIMITS",
            "issues": issues
        }

    return {
        "status": "NEEDS_VERIFICATION",
        "issues": [],
        "message": (
            "Width and thickness pass the demo limits. "
            "Material grade, tooling, strength, profile geometry "
            "and other machine constraints are not yet verified."
        )
    }
