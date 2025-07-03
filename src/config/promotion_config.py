from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class PromotionType(Enum):
    """促銷類型枚舉"""
    THRESHOLD_DISCOUNT = "threshold_discount"
    BOGO_COSMETICS = "bogo_cosmetics"
    DOUBLE11 = "double11"
    FIRST_TIME_CUSTOMER = "first_time_customer"
    CATEGORY_DISCOUNT = "category_discount"
    BUNDLE_DISCOUNT = "bundle_discount"


@dataclass
class PromotionConfig:
    """促銷配置"""
    type: PromotionType
    enabled: bool = True
    priority: int = 0
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class PromotionConfigManager:
    """促銷配置管理器"""
    
    def __init__(self):
        self.configs: Dict[PromotionType, PromotionConfig] = {}
        self._load_default_configs()
    
    def _load_default_configs(self):
        """載入預設配置"""
        default_configs = [
            PromotionConfig(
                type=PromotionType.THRESHOLD_DISCOUNT,
                enabled=True,
                priority=1,
                parameters={"thresholds": [{"threshold": 1000, "discount": 100}]}
            ),
            PromotionConfig(
                type=PromotionType.BOGO_COSMETICS,
                enabled=False,
                priority=2
            ),
            PromotionConfig(
                type=PromotionType.DOUBLE11,
                enabled=False,
                priority=3
            ),
            PromotionConfig(
                type=PromotionType.FIRST_TIME_CUSTOMER,
                enabled=False,
                priority=4,
                parameters={"discount_percentage": 0.1}
            ),
            PromotionConfig(
                type=PromotionType.CATEGORY_DISCOUNT,
                enabled=False,
                priority=5,
                parameters={"category": "electronics", "discount_percentage": 0.15}
            ),
            PromotionConfig(
                type=PromotionType.BUNDLE_DISCOUNT,
                enabled=False,
                priority=6,
                parameters={"required_items": ["T-shirt", "褲子"], "discount_amount": 200}
            )
        ]
        
        for config in default_configs:
            self.configs[config.type] = config
    
    def get_config(self, promotion_type: PromotionType) -> PromotionConfig:
        """獲取指定促銷類型的配置"""
        return self.configs.get(promotion_type)
    
    def update_config(self, promotion_type: PromotionType, **kwargs) -> None:
        """更新促銷配置"""
        if promotion_type in self.configs:
            config = self.configs[promotion_type]
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
    
    def get_enabled_configs(self) -> List[PromotionConfig]:
        """獲取所有啟用的配置，按優先級排序"""
        enabled_configs = [
            config for config in self.configs.values() 
            if config.enabled
        ]
        return sorted(enabled_configs, key=lambda x: x.priority)
    
    def enable_promotion(self, promotion_type: PromotionType) -> None:
        """啟用促銷"""
        self.update_config(promotion_type, enabled=True)
    
    def disable_promotion(self, promotion_type: PromotionType) -> None:
        """停用促銷"""
        self.update_config(promotion_type, enabled=False) 