from typing import List, Dict, Optional
from src.domain.models import Order, OrderItem
from src.promotions.base import PromotionStrategy
from src.promotions.factory import PromotionStrategyFactory


class OrderService:
    """
    訂單服務 - 負責處理訂單創建和促銷應用
    使用策略模式處理不同類型的促銷
    """
    
    def __init__(
        self,
        promotions: Optional[List[Dict[str, int]]] = None,
        bogo_cosmetics_active: bool = False,
        double11_active: bool = False
    ):
        self.strategies = PromotionStrategyFactory.create_strategies(
            promotions=promotions,
            bogo_cosmetics_active=bogo_cosmetics_active,
            double11_active=double11_active
        )
    
    def place_order(self, items: List[Dict]) -> Order:
        """
        下訂單並應用促銷策略
        
        Args:
            items: 訂單項目列表，每個項目包含 productName, quantity, unitPrice, category
            
        Returns:
            Order: 處理後的訂單
        """
        # 創建訂單項目
        order_items = self._create_order_items(items)
        
        # 創建初始訂單
        order = Order(items=order_items)
        
        # 應用促銷策略
        order = self._apply_promotions(order)
        
        return order
    
    def _create_order_items(self, items: List[Dict]) -> List[OrderItem]:
        """從字典列表創建訂單項目"""
        has_category = any('category' in item for item in items)
        
        order_items = []
        for item in items:
            order_item = OrderItem(
                product_name=item.get('productName'),
                quantity=item.get('quantity'),
                unit_price=item.get('unitPrice'),
                category=item.get('category') if has_category else None
            )
            order_items.append(order_item)
        
        return order_items
    
    def _apply_promotions(self, order: Order) -> Order:
        """應用所有適用的促銷策略"""
        # 特殊處理：雙十一策略優先級最高，會重新計算總金額
        double11_strategy = next(
            (s for s in self.strategies if hasattr(s, 'rule') and hasattr(s.rule, 'evaluate') and 'Double11Rule' in str(type(s.rule))),
            None
        )
        
        if double11_strategy and double11_strategy.is_applicable(order):
            return double11_strategy.apply(order)
        
        # 應用其他促銷策略
        for strategy in self.strategies:
            if strategy.is_applicable(order):
                order = strategy.apply(order)
        
        return order
    
    def add_promotion_strategy(self, strategy: PromotionStrategy) -> None:
        """動態添加促銷策略"""
        self.strategies.append(strategy)
    
    def remove_promotion_strategy(self, strategy_type: type) -> None:
        """移除指定類型的促銷策略"""
        self.strategies = [s for s in self.strategies if not isinstance(s, strategy_type)] 