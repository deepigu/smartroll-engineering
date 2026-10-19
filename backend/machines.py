
machines = {
    "RF100": {
        "name": "SmartRoll Demo RF100",
        "min_thickness": 0.5,
        "max_thickness": 2.0,
        "max_strip_width": 500
    },
    "RF200": {
        "name": "SmartRoll Demo RF200",
        "min_thickness": 1.0,
        "max_thickness": 4.0,
        "max_strip_width": 800
    }
}


def get_machine(machine_code):
    return machines.get(machine_code)
