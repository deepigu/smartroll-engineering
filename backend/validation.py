
def get_positive_float(message):
    while True:
        try:
            value = float(input(message))

            if value > 0:
                return value

            print("Please enter a number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_positive_integer(message):
    while True:
        try:
            value = int(input(message))

            if value > 0:
                return value

            print("Please enter a whole number greater than zero.")

        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_waste_percentage(message):
    while True:
        try:
            value = float(input(message))

            if 0 <= value < 100:
                return value

            print("Waste must be between 0 and less than 100%.")

        except ValueError:
            print("Invalid percentage. Please try again.")
