from hash_table import HashTable

print("=== Test 1: no duplicate after tombstone ===")
table = HashTable(23)
table.insert(1042, "Paracetamol")
table.insert(1065, "Ibuprofen")
table.delete(1042)
table.insert(1065, "Ibuprofen (updated)")
slots = [i for i in range(table.size) if table.keys[i] == 1065]
print("1065 found in slot(s):", slots, "->", "PASS" if len(slots) == 1 else "FAIL")

print("\n=== Test 2: automatic resize ===")
table = HashTable(23)
for product_id in range(1000, 1040):
    old_size = table.size
    table.insert(product_id, f"Medicine {product_id}")
    if table.size != old_size:
        print(f"Inserted item {table.count}: table resized {old_size} -> {table.size}")
print(f"Final: {table.count} items, size {table.size}, load factor {table.load_factor():.2f}")

missing = [pid for pid in range(1000, 1040) if table.get(pid) is None]
print("All 40 items still found after resizing ->", "PASS" if not missing else f"FAIL {missing}")