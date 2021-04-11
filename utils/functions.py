import random
from products.models import Product

def checkExistenceOfCode(code):
    return Product.objects.filter(code=code).exists()

def generate_product_code():
    code = ''
    for x in range(16):
        code+=str(random.randint(0,9))
    if checkExistenceOfCode(code):
        return generate_product_code()
    return code



