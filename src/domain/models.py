from typing import List, Optional
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class OrderItem:
    """訂單項目實體"""
    product_name: str
    quantity: int
    unit_price: int
    category: Optional[str] = None
    
    def __post_init__(self):
        self.quantity = int(self.quantity)
        self.unit_price = int(self.unit_price)
    
    @property
    def subtotal(self) -> int:
        """計算項目小計"""
        return self.quantity * self.unit_price


@dataclass
class Order:
    """訂單實體"""
    items: List[OrderItem]
    original_amount: Optional[int] = None
    discount: int = 0
    total_amount: int = field(init=False)
    
    def __post_init__(self):
        if self.original_amount is None:
            self.original_amount = sum(item.subtotal for item in self.items)
        self.total_amount = self.original_amount - self.discount
    
    def add_item(self, item: OrderItem) -> None:
        """添加訂單項目"""
        self.items.append(item)
        self.original_amount = sum(item.subtotal for item in self.items)
        self.total_amount = self.original_amount - self.discount
    
    def apply_discount(self, discount_amount: int) -> None:
        """應用折扣"""
        self.discount += discount_amount
        self.total_amount = self.original_amount - self.discount 