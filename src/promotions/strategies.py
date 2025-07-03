from typing import List, Dict, Any
from src.domain.models import Order, OrderItem
from src.promotions.base import PromotionStrategy, PromotionRule


class ThresholdDiscountRule(PromotionRule):
    """門檻折扣規則"""
    
    def __init__(self, threshold: int, discount: int):
        self.threshold = int(threshold)
        self.discount = int(discount)
    
    def evaluate(self, order: Order) -> bool:
        return order.original_amount >= self.threshold
    
    def get_discount_amount(self, order: Order) -> int:
        return self.discount if self.evaluate(order) else 0


class ThresholdDiscountStrategy(PromotionStrategy):
    """門檻折扣策略"""
    
    def __init__(self, rules: List[Dict[str, int]]):
        self.rules = [ThresholdDiscountRule(rule['threshold'], rule['discount']) 
                     for rule in rules]
    
    def is_applicable(self, order: Order) -> bool:
        return any(rule.evaluate(order) for rule in self.rules)
    
    def apply(self, order: Order) -> Order:
        total_discount = sum(rule.get_discount_amount(order) for rule in self.rules)
        order.apply_discount(total_discount)
        return order


class BogoCosmeticsRule(PromotionRule):
    """買一送一化妝品規則"""
    
    def evaluate(self, order: Order) -> bool:
        return any(item.category == 'cosmetics' for item in order.items)
    
    def get_discount_amount(self, order: Order) -> int:
        return 0  # BOGO 不影響金額，只影響數量


class BogoCosmeticsStrategy(PromotionStrategy):
    """買一送一化妝品策略"""
    
    def __init__(self):
        self.rule = BogoCosmeticsRule()
    
    def is_applicable(self, order: Order) -> bool:
        return self.rule.evaluate(order)
    
    def apply(self, order: Order) -> Order:
        # 創建新的訂單項目列表，化妝品數量+1
        new_items = []
        for item in order.items:
            if item.category == 'cosmetics':
                new_item = OrderItem(
                    product_name=item.product_name,
                    quantity=item.quantity + 1,
                    unit_price=item.unit_price,
                    category=item.category
                )
                new_items.append(new_item)
            else:
                new_items.append(item)
        
        # 創建新訂單，保持原金額不變
        new_order = Order(
            items=new_items,
            original_amount=order.original_amount,
            discount=order.discount
        )
        return new_order


class Double11Rule(PromotionRule):
    """雙十一規則"""
    
    def evaluate(self, order: Order) -> bool:
        return any(item.quantity >= 10 for item in order.items)
    
    def get_discount_amount(self, order: Order) -> int:
        total_original = sum(item.subtotal for item in order.items)
        total_discounted = 0
        
        for item in order.items:
            groups_of_10 = item.quantity // 10
            rest = item.quantity % 10
            discounted_price = groups_of_10 * 10 * item.unit_price * 0.8
            original_price = rest * item.unit_price
            total_discounted += discounted_price + original_price
        
        return int(total_original - total_discounted)


class Double11Strategy(PromotionStrategy):
    """雙十一策略"""
    
    def __init__(self):
        self.rule = Double11Rule()
    
    def is_applicable(self, order: Order) -> bool:
        return self.rule.evaluate(order)
    
    def apply(self, order: Order) -> Order:
        # 雙十一特殊處理：重新計算總金額
        total_amount = 0
        for item in order.items:
            groups_of_10 = item.quantity // 10
            rest = item.quantity % 10
            discounted_price = groups_of_10 * 10 * item.unit_price * 0.8
            original_price = rest * item.unit_price
            total_amount += discounted_price + original_price
        
        # 創建新訂單，使用計算後的金額
        new_order = Order(
            items=order.items,
            original_amount=int(total_amount),
            discount=0
        )
        return new_order 