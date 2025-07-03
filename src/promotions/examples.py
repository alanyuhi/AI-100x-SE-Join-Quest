from typing import List
from src.domain.models import Order, OrderItem
from src.promotions.base import PromotionStrategy, PromotionRule


class FirstTimeCustomerRule(PromotionRule):
    """首次購買客戶規則"""
    
    def __init__(self, discount_percentage: float = 0.1):
        self.discount_percentage = discount_percentage
    
    def evaluate(self, order: Order) -> bool:
        # 這裡可以檢查客戶是否為首次購買
        # 目前簡化為總是適用
        return True
    
    def get_discount_amount(self, order: Order) -> int:
        return int(order.original_amount * self.discount_percentage)


class FirstTimeCustomerStrategy(PromotionStrategy):
    """首次購買客戶策略"""
    
    def __init__(self, discount_percentage: float = 0.1):
        self.rule = FirstTimeCustomerRule(discount_percentage)
    
    def is_applicable(self, order: Order) -> bool:
        return self.rule.evaluate(order)
    
    def apply(self, order: Order) -> Order:
        discount_amount = self.rule.get_discount_amount(order)
        order.apply_discount(discount_amount)
        return order


class CategoryDiscountRule(PromotionRule):
    """特定類別商品折扣規則"""
    
    def __init__(self, category: str, discount_percentage: float):
        self.category = category
        self.discount_percentage = discount_percentage
    
    def evaluate(self, order: Order) -> bool:
        return any(item.category == self.category for item in order.items)
    
    def get_discount_amount(self, order: Order) -> int:
        category_total = sum(
            item.subtotal for item in order.items 
            if item.category == self.category
        )
        return int(category_total * self.discount_percentage)


class CategoryDiscountStrategy(PromotionStrategy):
    """特定類別商品折扣策略"""
    
    def __init__(self, category: str, discount_percentage: float):
        self.rule = CategoryDiscountRule(category, discount_percentage)
    
    def is_applicable(self, order: Order) -> bool:
        return self.rule.evaluate(order)
    
    def apply(self, order: Order) -> Order:
        discount_amount = self.rule.get_discount_amount(order)
        order.apply_discount(discount_amount)
        return order


class BundleDiscountRule(PromotionRule):
    """組合商品折扣規則"""
    
    def __init__(self, required_items: List[str], discount_amount: int):
        self.required_items = set(required_items)
        self.discount_amount = discount_amount
    
    def evaluate(self, order: Order) -> bool:
        order_items = {item.product_name for item in order.items}
        return self.required_items.issubset(order_items)
    
    def get_discount_amount(self, order: Order) -> int:
        return self.discount_amount if self.evaluate(order) else 0


class BundleDiscountStrategy(PromotionStrategy):
    """組合商品折扣策略"""
    
    def __init__(self, required_items: List[str], discount_amount: int):
        self.rule = BundleDiscountRule(required_items, discount_amount)
    
    def is_applicable(self, order: Order) -> bool:
        return self.rule.evaluate(order)
    
    def apply(self, order: Order) -> Order:
        discount_amount = self.rule.get_discount_amount(order)
        order.apply_discount(discount_amount)
        return order 