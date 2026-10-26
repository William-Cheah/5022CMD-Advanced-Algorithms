"""
medicine.py:
Medicine entity class: stores one pharmacy product and validates its data.
"""

from decimal import Decimal

class Medicine:
    """One product sold by the pharmacy"""

    def __init__(self, product_id, name, category, price, stock_qty,requires_prescription):
        # validation: refuse bad data
        if product_id <= 0:
            raise ValueError("Product ID must be a positive number")
        if stock_qty < 0:
            raise ValueError("Stock quantity cannot be negative")

        # attributes
        self.product_id = product_id
        self.name = name
        self.category = category
        # in case become Decimal (5.9 is float), will become 5.9000...3552,so change to str first
        self.price = Decimal(str(price)).quantize(Decimal("0.01"))
        self.stock_qty = stock_qty
        self.requires_prescription = requires_prescription

    def is_low_stock(self):
        return self.stock_qty <= 20

    def __str__(self):  # Python auto calls it to determine how it is displayed
        rx = "Prescription" if self.requires_prescription else "Over-the-counter"
        return (f"ID: {self.product_id} | {self.name} | {self.category} | "
                f"RM{self.price} | Stock: {self.stock_qty} | {rx}")