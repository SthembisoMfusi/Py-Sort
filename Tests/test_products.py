import unittest
from products import Product, find_most_expensive_product, group_products_by_category, calculate_total_price, filter_products_by_price, search_products_by_name
from typing import List, Dict

class TestAssessment(unittest.TestCase):

    def setUp(self):
        
        self.product1 = Product("Laptop", 1200.00, "Electronics")
        self.product2 = Product("Mouse", 25.00, "Electronics")
        self.product3 = Product("T-Shirt", 20.00, "Clothing")
        self.product4 = Product("Jeans", 60.00, "Clothing")
        self.product5 = Product("Coffee Maker", 80.00, "Appliances")
        self.products = [self.product1, self.product2, self.product3, self.product4, self.product5]

    def test_find_most_expensive_product_basic(self):
        self.assertEqual(find_most_expensive_product(self.products), self.product1)

    def test_find_most_expensive_product_empty(self):
        self.assertIsNone(find_most_expensive_product([]))

    def test_group_products_by_category_basic(self):
        expected: Dict[str, List["Product"]] = {
            "Electronics": [self.product1, self.product2],
            "Clothing": [self.product3, self.product4],
            "Appliances": [self.product5]
        }
        self.assertEqual(group_products_by_category(self.products), expected)

    def test_group_products_by_category_empty(self):
        self.assertEqual(group_products_by_category([]), {})

    def test_calculate_total_price_basic(self):
        self.assertEqual(calculate_total_price(self.products), 1385.00)
import products

class TestAssessment(unittest.TestCase):

    def test_part1(self):
  

        self.assertTrue(hasattr(products, 'compare_phonebook_search'), "compare_phonebook_search function missing")
       

        self.assertTrue(hasattr(products, 'identify_faster_method'), "identify_faster_method function missing")
        

        self.assertTrue(hasattr(products, 'explain_logarithmic_time'), "explain_logarithmic_time function missing")


    def test_part2(self):

        self.assertTrue(hasattr(products, 'compare_largest_number_algorithms'), "compare_largest_number_algorithms function missing")
        

        self.assertTrue(hasattr(products, 'analyze_dictionary_lookup'), "analyze_dictionary_lookup function missing")
        

    def test_part3(self):

         self.assertTrue(hasattr(products, 'choose_search_algorithm'), "choose_search_algorithm function missing")
 

    def test_calculate_total_price_empty(self):
        self.assertEqual(calculate_total_price([]), 0.0)

    def test_filter_products_by_price_basic(self):
        expected = [self.product2, self.product3, self.product4, self.product5]
        self.assertEqual(filter_products_by_price(self.products, 80.00), expected)

    def test_filter_products_by_price_empty(self):
        self.assertEqual(filter_products_by_price([], 50.00), [])

    def test_filter_products_by_price_no_match(self):
        self.assertEqual(filter_products_by_price(self.products, 10.00), [])

    def test_search_products_by_name_basic(self):
        expected = [self.product1]
        self.assertEqual(search_products_by_name(self.products, "Lap"), expected)

    def test_search_products_by_name_empty(self):
        self.assertEqual(search_products_by_name([], "mouse"), [])

    def test_search_products_by_name_no_match(self):
        self.assertEqual(search_products_by_name(self.products, "keyboard"), [])

    def test_search_products_by_name_case_insensitive(self):
          expected = [self.product2]
          self.assertEqual(search_products_by_name(self.products, "Mouse"), expected)

    def test_search_products_by_name_partial_match(self):
          expected = [self.product3]
          self.assertEqual(search_products_by_name(self.products, "Shirt"), expected)

if __name__ == '__main__':
    unittest.main()