from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.domain.models import Order, OrderItem


class PromotionStrategy(ABC):
    """促銷策略抽象基類"""
    
    @abstractmethod
    def apply(self, order: Order) -> Order:
        """應用促銷策略到訂單"""
        pass
    
    @abstractmethod
    def is_applicable(self, order: Order) -> bool:
        """檢查促銷是否適用於此訂單"""
        pass


class PromotionRule(ABC):
    """促銷規則抽象基類"""
    
    @abstractmethod
    def evaluate(self, order: Order) -> bool:
        """評估規則是否滿足"""
        pass
    
    @abstractmethod
    def get_discount_amount(self, order: Order) -> int:
        """計算折扣金額"""
        pass 