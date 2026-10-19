
class Machine:

    def __init__(self, name, min_thickness, max_thickness, max_width):
        self.name = name
        self.min_thickness = min_thickness
        self.max_thickness = max_thickness
        self.max_width = max_width

    def display_info(self):
        print("Machine:", self.name)
        print("Minimum Thickness:", self.min_thickness, "mm")
        print("Maximum Thickness:", self.max_thickness, "mm")
        print("Maximum Width:", self.max_width, "mm")
