
class Material:

    def __init__(self, name, grade, density, price_per_kg):
        self.name = name
        self.grade = grade
        self.density = density
        self.price_per_kg = price_per_kg

    def display_info(self):
        print("Material:", self.name)
        print("Grade:", self.grade)
        print("Density:", self.density, "kg/m³")
        print("Price per kg: $", self.price_per_kg)
