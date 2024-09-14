class ProductService:
    def get_product(self, product_id):
        # Logic to get product by ID
        return {"product_id": product_id, "name": "Sample Product"}

    def create_product(self, product_data):
        # Logic to create a new product
        return {"product_id": 1, "name": product_data['name']}
