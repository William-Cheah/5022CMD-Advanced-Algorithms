"""
A menu program
"""

import time
from linear_search import linear_search
from hash_table import HashTable
from medicine import Medicine

#---------- input helpers: keep asking until the input is valid ---------
def ask_int(prompt):
    while True:
        text = input(prompt)
        try:
            return int(text)    # success -> return int, leave function
        except ValueError:
            print("Please enter a WHOLE NUMBER! ") # failed -> ask one more time

def ask_price(prompt):
    while True:
        text = input(prompt)
        try:
            if float(text) < 0:
                print(" Price cannot be negative! ")
            else:
                return text
        except ValueError:
            print(" Please enter a number, e.g. 5.90")

def ask_yes_no(prompt):
    while True:
        text = input(prompt).strip().upper()
        if text == "Y":
            return True
        if text == "N":
            return False
        print(" Please enter Y or N! ")


#------------------------- Edit --------------------------
def to_price(text):
    if float(text)<0:
        raise ValueError("Price cannot be negative! ")
    return text

def to_stock(text):
    value = int(text)
    if value < 0:
        raise ValueError("Stock cannot be negative! ")
    return value

def to_yes_no(text):
    text = text.upper()
    if text == "Y":
        return True
    if text == "N":
        return False
    raise ValueError("Enter Y or N")

def edit_or_keep(prompt, current, convert):
    while True:
        text = input(f"{prompt} [{current}]: ").strip()
        if text == "":
            return current          # press enter = keep current value
        try:
            return convert(text)
        except ValueError:
            print(" Invalid input, please try again!")

def edit_product(table,array):
    product_id = ask_int("Enter Product ID to edit: ")
    old = table.get(product_id)
    if old is None:
        print(f"Product ID {product_id} not found.")
        return

    print("Current: ", old)
    print("Press Enter to keep the current value.")
    name = edit_or_keep("Name", old.name, str)
    category = edit_or_keep("Category", old.category, str)
    price = edit_or_keep("Price", old.price, to_price)
    stock = edit_or_keep("Stock Quantity", old.stock_qty, to_stock)
    rx = edit_or_keep("Requires prescription? (Y/N)", old.requires_prescription, to_yes_no)

    try:
        new_med = Medicine(product_id, name, category, price, stock, rx)
    except ValueError as error:
        print(" Error: ", error)
        return

    print("\nFrom (Old): ", old)
    print("To   (New): ", new_med)

    if ask_yes_no(f"Confirm update for Product {product_id}? (Y/N): "):
        slot, probes = table.insert(product_id, new_med)  # find the same key and overwrite that slot
        index = array.index(old)    # position of old medicine in array
        array[index] = new_med      # replace it
        print(f"Product {product_id} updated slot [{slot}].")
    else:
        print("Update cancelled. No changes made")


#---------------------------- menu (insert, search, delete)------------------------------
def insert_product(table, array):
    product_id = ask_int("Product ID: ")
    if product_id <= 0:
        print("Please enter a valid product ID (must be a positive number)! ")
        return
    # try get to search for the same id, prevent duplicate insertion
    if table.get(product_id) is not None:
        print(f"Product ID already exists.")
        return
    name = input("Enter Product Name: ")
    category = input("Enter Product Category: ")
    price = ask_price("Enter Price (RM): ")
    stock = ask_int("Enter Stock Quantity: ")
    rx = ask_yes_no("Requires prescription? (Y/N): ")

    try:
        med=Medicine(product_id, name, category, price, stock, rx)      # insert as new Medicine to validate value
    except ValueError as error:     # such as (id, stock_qty = negative)
        print ("Error: ", error)
        return

    home = table.hash_function(product_id)
    old_size = table.size
    slot,probes = table.insert(product_id, med)
    array.append(med)
    if table.size != old_size:
        print(f"Load Factor exceeded 0.7: table resized from {old_size} to {table.size} slots")
        home = table.hash_function(product_id)  # new size changed,so home slot need to re-calculate

    print(f"Product inserted successfully into slot [{slot}] (home slot {home}, {probes} slot(s) skipped).")

def search_product(table, array):
    product_id = ask_int("Enter Product ID to search: ")
    med = table.get(product_id)
    if med is not None:
        print("Product Found!")
        print(med)
    else:
        print(f"Product ID {product_id} not found.")

    # time for searching in both hash table and array
    repeats = 1000
    start = time.perf_counter_ns()
    for _ in range(repeats):
        table.get(product_id)
    hash_ns = (time.perf_counter_ns() - start) / repeats

    start = time.perf_counter_ns()
    for _ in range(repeats):
        linear_search(array, product_id)
    array_ns = (time.perf_counter_ns() - start) / repeats

    print(f"Search Time (average of {repeats} searches): ")
    print(f" Hash Table : {hash_ns:>8,.0f} ns")
    print(f" 1D Array : {array_ns:>8,.0f} ns")

def delete_product(table, array):
    product_id = ask_int("Enter Product ID to delete: ")
    med = table.get(product_id)
    if table.delete(product_id):
        array.remove(med)
        print(f"Product {product_id} ({med.name}) deleted (slot is now a tombstone).")
    else:
        print(f"Product {product_id} not found.")

def list_products(table):
    medicines = sorted(table.get_all_values(), key=lambda med:med.product_id)
    if len(medicines) == 0:
        print("No products found in the inventory.")
        return

    print(f"\n{'ID':>6} | {'Name':<20} | {'Category':<14} | {'Price':>8} | {'Stock':>5} | {'Rx':<3} | Alert")
    print("-"*70)
    for med in medicines:
        rx = "Yes" if med.requires_prescription else "No"
        alert = "LOW" if med.is_low_stock() else ""
        print(f"{med.product_id:>6} | {med.name:<20} | {med.category:<14} | "
              f"RM{med.price:>6} | {med.stock_qty:>5} | {rx:<3} | {alert}")
    print(f"Total: {len(medicines)} product(s)")

def get_menu_choice():
    print("\n***** Pharmacy Inventory System *****")
    print("1. Insert Product")
    print("2. Search Product")
    print("3. Delete Product")
    print("4. Edit Product")
    print("5. View Hash Table")
    print("6. List All Products")
    print("0. Exit")
    choice = ask_int("Choice: ")
    return choice


#----------------------------------------------------- main program -----------------------------
def main():
    table = HashTable(8)
    array = []

    #pre-defined records
    for med in [
        Medicine(1042, "Paracetamol 500mg", "Analgesic", "5.90", 120, False),
        Medicine(1065, "Ibuprofen 200mg", "Analgesic", "8.50", 85, False),
        Medicine(1088, "Amoxicillin 500mg", "Antibiotic", "18.00", 40, True),
        Medicine(2001, "Cetirizine 10mg", "Antihistamine", "12.90", 60, False),
        Medicine(2024, "Loratadine 10mg", "Antihistamine", "14.50", 15, False),
    ]:
        table.insert(med.product_id, med)
        array.append(med)

    while True:
        choice = get_menu_choice()
        if choice == 1:
            insert_product(table, array)
        elif choice == 2:
            search_product(table, array)
        elif choice == 3:
            delete_product(table, array)
        elif choice == 4:
            edit_product(table, array)
        elif choice == 5:
            table.display()
        elif choice == 6:
            list_products(table)
        elif choice == 0:
            print("Exiting Inventory System. GoodBye!")
            break
        else:
            print("Invalid choice, please enter 0-6")

if __name__ == "__main__":
    main()

