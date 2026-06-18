#This class for pydantic model to validate the data for the product. It has three attributes: id, name, and price. The id is an integer, the name is a string, and the price is a float.

from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float