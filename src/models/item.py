
import strawberry


@strawberry.type
class Item:
    date: str
    client_id: int
    sku: str
    product_code: int
    product_name: str
    brand: str
    product_category: str
    main_product_category: str
    product_quantity: int
    product_detail_quantity: int
    product_income_amount: float
    added_to_cart_quantity: int
    removed_from_cart_quantity: int
    flag_pipol: int
