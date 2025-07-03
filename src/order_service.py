from typing import List, Optional, Dict

class OrderItem:
    def __init__(self, product_name: str, quantity: int, unit_price: int, category: Optional[str] = None):
        self.product_name = product_name
        self.quantity = int(quantity)
        self.unit_price = int(unit_price)
        self.category = category

class Order:
    def __init__(self, items: List[OrderItem], original_amount: Optional[int] = None, discount: Optional[int] = None):
        self.items = items
        self.original_amount = (
            original_amount if original_amount is not None
            else sum(item.quantity * item.unit_price for item in items)
        )
        self.discount = discount if discount is not None else 0
        self.total_amount = self.original_amount - self.discount

class OrderService:
    """
    負責處理訂單優惠邏輯：
    - 門檻折扣（threshold discount）
    - cosmetics 買一送一（bogo）
    - 雙十一優惠（double11）
    支援優惠疊加。
    """
    def __init__(self, promotions: Optional[List[Dict]] = None, bogo_cosmetics_active: bool = False, double11_active: bool = False):
        self.promotions = promotions
        self.bogo_cosmetics_active = bogo_cosmetics_active
        self.double11_active = double11_active

    def place_order(self, items: List[Dict]) -> Order:
        has_category = any('category' in item for item in items)
        order_items = [OrderItem(
            item.get('productName'),
            item.get('quantity'),
            item.get('unitPrice'),
            item.get('category') if has_category else None
        ) for item in items]

        if self.double11_active:
            total_amount = self._apply_double11_discount(order_items)
            return Order(order_items, original_amount=total_amount, discount=0)

        original_amount = sum(item.quantity * item.unit_price for item in order_items)
        discount = self._calculate_threshold_discount(original_amount)
        display_items = self._apply_bogo_cosmetics(order_items) if self.bogo_cosmetics_active else order_items
        return Order(display_items, original_amount, discount)

    def _calculate_threshold_discount(self, original_amount: int) -> int:
        """計算門檻折扣金額"""
        discount = 0
        if self.promotions:
            for promo in self.promotions:
                threshold = int(promo.get('threshold', 0))
                promo_discount = int(promo.get('discount', 0))
                if original_amount >= threshold:
                    discount += promo_discount
        return discount

    def _apply_bogo_cosmetics(self, items: List[OrderItem]) -> List[OrderItem]:
        """對 cosmetics 商品加贈 1 件（僅顯示數量，金額不變）"""
        result = []
        for item in items:
            if item.category == 'cosmetics':
                result.append(OrderItem(item.product_name, item.quantity + 1, item.unit_price, item.category))
            else:
                result.append(item)
        return result

    def _apply_double11_discount(self, items: List[OrderItem]) -> int:
        """同一商品每滿 10 件享 8 折，其餘原價"""
        total = 0
        for item in items:
            n = item.quantity
            price = item.unit_price
            groups_of_10 = n // 10
            rest = n % 10
            total += groups_of_10 * 10 * price * 0.8 + rest * price
        return int(total) 