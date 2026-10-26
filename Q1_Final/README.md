# Q1 – Hashing: Pharmacy Inventory System

A command-line inventory system for a pharmacy. Products are stored in a
hash table that resolves collisions with **open addressing and linear probing**,
marks deleted slots as tombstones and resizes automatically when the load
factor would exceed 0.7. The same records are also kept in a one-dimensional
array so that search performance can be compared.

## Files

| File | Purpose |
|---|---|
| `hash_table.py` | Generic `HashTable` class: insert, get, delete (tombstones), resize, display, count_probes |
| `medicine.py` | `Medicine` entity class with validation |
| `linear_search.py` | Linear search used for the 1D array |
| `inventory_system.py` | Menu program: insert, search (hash vs array timing), delete, edit, view table, list products |
| `performance_test.py` | Experiment: hash table vs 1D array search time for 100 – 50,000 records (median of 5 runs, probe counts) |
| `test_hash_table.py` | Automated checks: no duplicate key after a tombstone; every record found after resizing |

## How to run

```
python inventory_system.py     # the inventory system
python performance_test.py     # the performance experiment (about one minute)
python test_hash_table.py      # automated checks of the HashTable class
```
