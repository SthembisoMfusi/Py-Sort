from typing import List, Optional, Dict

class Product:
    """
    Represents a product with a name, price, and category.
    """
    def __init__(self, name: str, price: float, category: str):
        self.name = name
        self.price = price
        self.category = category

def find_most_expensive_product(products: List["Product"]) -> Optional["Product"]:
    """
    Finds the most expensive product in the list of products.

    Args:
        products: A list of Product objects.

    Returns:
        The most expensive Product object, or None if the list is empty.
    """
    pass  # Replace with your implementation

def group_products_by_category(products: List["Product"]) -> Dict[str, List["Product"]]:
    """
    Groups the products by their category.

    Args:
        products: A list of Product objects.

    Returns:
        A dictionary where keys are categories (strings) and values are lists of Product objects
        belonging to that category.
    """
    pass # Replace with your implementation

def calculate_total_price(products: List["Product"]) -> float:
     """
     Calculates the total price of all products in the list.

     Args:
         products: A list of Product objects.

     Returns:
         The total price of all products.
     """
     pass  # Replace with your implementation

def filter_products_by_price(products: List["Product"], max_price: float) -> List["Product"]:
    """
    Filters the products to return only those with a price less than or equal to the given maximum price.

    Args:
        products: A list of Product objects.
        max_price: The maximum price to filter by.

    Returns:
        A new list containing only the products with a price less than or equal to max_price.
    """
    pass # Replace with your implementation

def search_products_by_name(products: List["Product"], search_term: str) -> List["Product"]:
    """
    Searches for products whose name contains the given search term (case-insensitive).

    Args:
        products: A list of Product objects.
        search_term: The term to search for in the product name.

    Returns:
        A list of Product objects whose name contains the search term.
    """
    pass # Replace with your implementation