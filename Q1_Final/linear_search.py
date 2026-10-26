"""
1D array search: compare each item's product_id from the start until it matches Time complexity: O(n).
"""

def linear_search(array, key):
    for med in array:
        if med.product_id == key:
            return med
    return None