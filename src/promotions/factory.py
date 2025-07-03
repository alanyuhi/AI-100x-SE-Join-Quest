from typing import List, Dict, Optional
from src.promotions.base import PromotionStrategy
from src.promotions.strategies import (
    ThresholdDiscountStrategy,
    BogoCosmeticsStrategy,
    Double11Strategy
)


class PromotionStrategyFactory:
    """促銷策略工廠"""
    
    @staticmethod
    def create_threshold_discount(promotions: List[Dict[str, int]]) -> ThresholdDiscountStrategy:
        """創建門檻折扣策略"""
        return ThresholdDiscountStrategy(promotions)
    
    @staticmethod
    def create_bogo_cosmetics() -> BogoCosmeticsStrategy:
        """創建買一送一化妝品策略"""
        return BogoCosmeticsStrategy()
    
    @staticmethod
    def create_double11() -> Double11Strategy:
        """創建雙十一策略"""
        return Double11Strategy()
    
    @staticmethod
    def create_strategies(
        promotions: Optional[List[Dict[str, int]]] = None,
        bogo_cosmetics_active: bool = False,
        double11_active: bool = False
    ) -> List[PromotionStrategy]:
        """創建多個促銷策略"""
        strategies = []
        
        if promotions:
            strategies.append(PromotionStrategyFactory.create_threshold_discount(promotions))
        
        if bogo_cosmetics_active:
            strategies.append(PromotionStrategyFactory.create_bogo_cosmetics())
        
        if double11_active:
            strategies.append(PromotionStrategyFactory.create_double11())
        
        return strategies 