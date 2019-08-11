def generate_discount_type(row):
    if row<3:
        value = "15% off"
        return value
    elif row<6:
        value = "15€ off"
        return value
    else:
        value = "Free Shipping"
        return value