import pytest
from src.services.order_service import OrderService
from src.domain.models import Order, OrderItem
from src.promotions.strategies import (
    ThresholdDiscountStrategy,
    BogoCosmeticsStrategy,
    Double11Strategy
)
from src.promotions.examples import (
    FirstTimeCustomerStrategy,
    CategoryDiscountStrategy,
    BundleDiscountStrategy
)
from src.config.promotion_config import PromotionConfigManager, PromotionType


class TestRefactoredOrderService:
    """重構後訂單服務的測試"""
    
    def test_basic_order_creation(self):
        """測試基本訂單創建"""
        service = OrderService()
        items = [
            {"productName": "T-shirt", "quantity": 2, "unitPrice": 500}
        ]
        
        order = service.place_order(items)
        
        assert order.original_amount == 1000
        assert order.discount == 0
        assert order.total_amount == 1000
        assert len(order.items) == 1
        assert order.items[0].product_name == "T-shirt"
    
    def test_threshold_discount_strategy(self):
        """測試門檻折扣策略"""
        promotions = [{"threshold": 1000, "discount": 100}]
        service = OrderService(promotions=promotions)
        
        items = [
            {"productName": "T-shirt", "quantity": 2, "unitPrice": 500}
        ]
        
        order = service.place_order(items)
        
        assert order.original_amount == 1000
        assert order.discount == 100
        assert order.total_amount == 900
    
    def test_bogo_cosmetics_strategy(self):
        """測試買一送一化妝品策略"""
        service = OrderService(bogo_cosmetics_active=True)
        
        items = [
            {"productName": "口紅", "quantity": 1, "unitPrice": 300, "category": "cosmetics"}
        ]
        
        order = service.place_order(items)
        
        assert order.original_amount == 300
        assert order.discount == 0
        assert order.total_amount == 300
        assert len(order.items) == 1
        assert order.items[0].quantity == 2  # 買一送一
    
    def test_double11_strategy(self):
        """測試雙十一策略"""
        service = OrderService(double11_active=True)
        
        items = [
            {"productName": "襪子", "quantity": 12, "unitPrice": 100}
        ]
        
        order = service.place_order(items)
        
        # 10雙8折 + 2雙原價 = 800 + 200 = 1000
        assert order.original_amount == 1000
        assert order.discount == 0
        assert order.total_amount == 1000
    
    def test_multiple_strategies(self):
        """測試多種策略組合"""
        promotions = [{"threshold": 1000, "discount": 100}]
        service = OrderService(
            promotions=promotions,
            bogo_cosmetics_active=True
        )
        
        items = [
            {"productName": "T-shirt", "quantity": 2, "unitPrice": 500},
            {"productName": "口紅", "quantity": 1, "unitPrice": 300, "category": "cosmetics"}
        ]
        
        order = service.place_order(items)
        
        assert order.original_amount == 1300
        assert order.discount == 100
        assert order.total_amount == 1200
        # 檢查化妝品數量是否增加
        cosmetics_item = next(item for item in order.items if item.category == "cosmetics")
        assert cosmetics_item.quantity == 2
    
    def test_dynamic_strategy_addition(self):
        """測試動態添加策略"""
        service = OrderService()
        first_time_strategy = FirstTimeCustomerStrategy(discount_percentage=0.1)
        service.add_promotion_strategy(first_time_strategy)
        
        items = [
            {"productName": "T-shirt", "quantity": 1, "unitPrice": 1000}
        ]
        
        order = service.place_order(items)
        
        assert order.original_amount == 1000
        assert order.discount == 100  # 10% 折扣
        assert order.total_amount == 900
    
    def test_strategy_removal(self):
        """測試移除策略"""
        promotions = [{"threshold": 1000, "discount": 100}]
        service = OrderService(promotions=promotions)
        
        # 移除門檻折扣策略
        service.remove_promotion_strategy(ThresholdDiscountStrategy)
        
        items = [
            {"productName": "T-shirt", "quantity": 2, "unitPrice": 500}
        ]
        
        order = service.place_order(items)
        
        assert order.original_amount == 1000
        assert order.discount == 0  # 沒有折扣
        assert order.total_amount == 1000


class TestPromotionConfigManager:
    """促銷配置管理器測試"""
    
    def test_default_configs(self):
        """測試預設配置"""
        manager = PromotionConfigManager()
        
        # 檢查預設配置
        threshold_config = manager.get_config(PromotionType.THRESHOLD_DISCOUNT)
        assert threshold_config.enabled == True
        assert threshold_config.priority == 1
        
        bogo_config = manager.get_config(PromotionType.BOGO_COSMETICS)
        assert bogo_config.enabled == False
    
    def test_enable_disable_promotion(self):
        """測試啟用和停用促銷"""
        manager = PromotionConfigManager()
        
        # 停用門檻折扣
        manager.disable_promotion(PromotionType.THRESHOLD_DISCOUNT)
        config = manager.get_config(PromotionType.THRESHOLD_DISCOUNT)
        assert config.enabled == False
        
        # 啟用買一送一
        manager.enable_promotion(PromotionType.BOGO_COSMETICS)
        config = manager.get_config(PromotionType.BOGO_COSMETICS)
        assert config.enabled == True
    
    def test_get_enabled_configs(self):
        """測試獲取啟用的配置"""
        manager = PromotionConfigManager()
        
        # 啟用雙十一促銷
        manager.enable_promotion(PromotionType.DOUBLE11)
        
        enabled_configs = manager.get_enabled_configs()
        enabled_types = [config.type for config in enabled_configs]
        
        assert PromotionType.THRESHOLD_DISCOUNT in enabled_types
        assert PromotionType.DOUBLE11 in enabled_types
        assert PromotionType.BOGO_COSMETICS not in enabled_types  # 預設停用


class TestNewPromotionStrategies:
    """新促銷策略測試"""
    
    def test_first_time_customer_strategy(self):
        """測試首次購買客戶策略"""
        strategy = FirstTimeCustomerStrategy(discount_percentage=0.15)
        
        items = [OrderItem("T-shirt", 1, 1000)]
        order = Order(items=items)
        
        assert strategy.is_applicable(order)
        
        result_order = strategy.apply(order)
        assert result_order.discount == 150  # 15% 折扣
        assert result_order.total_amount == 850
    
    def test_category_discount_strategy(self):
        """測試類別折扣策略"""
        strategy = CategoryDiscountStrategy("electronics", 0.2)
        
        items = [
            OrderItem("手機", 1, 1000, "electronics"),
            OrderItem("T-shirt", 1, 500, "apparel")
        ]
        order = Order(items=items)
        
        assert strategy.is_applicable(order)
        
        result_order = strategy.apply(order)
        assert result_order.discount == 200  # 電子產品 20% 折扣
        assert result_order.total_amount == 1300
    
    def test_bundle_discount_strategy(self):
        """測試組合折扣策略"""
        strategy = BundleDiscountStrategy(["T-shirt", "褲子"], 200)
        
        items = [
            OrderItem("T-shirt", 1, 500),
            OrderItem("褲子", 1, 800)
        ]
        order = Order(items=items)
        
        assert strategy.is_applicable(order)
        
        result_order = strategy.apply(order)
        assert result_order.discount == 200
        assert result_order.total_amount == 1100
    
    def test_bundle_discount_strategy_not_applicable(self):
        """測試組合折扣策略不適用情況"""
        strategy = BundleDiscountStrategy(["T-shirt", "褲子"], 200)
        
        items = [
            OrderItem("T-shirt", 1, 500),
            OrderItem("帽子", 1, 300)  # 缺少褲子
        ]
        order = Order(items=items)
        
        assert not strategy.is_applicable(order)
        
        result_order = strategy.apply(order)
        assert result_order.discount == 0
        assert result_order.total_amount == 800 