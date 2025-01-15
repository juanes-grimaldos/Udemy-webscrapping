import os
import json
import logging

def store_product_info(file_name: str, product_info: dict):
    """
    Stores the product information in a JSON file.

    Args:
        file_name (str): The name of the JSON file.
        product_info (dict): The product information to be stored.

    Returns:
        None
    """
    if os.path.exists(file_name):
        with open(file_name, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        data.append(product_info)

        with open(file_name, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            logging.info(f"Product info appended in {file_name}")
    else:
        data = [product_info]

        with open(file_name, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            logging.info(f"Product info stored in {file_name}")