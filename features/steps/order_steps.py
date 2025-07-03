from behave import given, when, then
from src.services.order_service import OrderService

@given('no promotions are applied')
def step_impl(context):
    context.promotion_config = None
    context.bogo_cosmetics_active = False

@given('the threshold discount promotion is configured')
def step_impl(context):
    context.promotion_config = [dict(row.items()) for row in context.table]
    if not hasattr(context, 'bogo_cosmetics_active'):
        context.bogo_cosmetics_active = False

@given('the buy one get one promotion for cosmetics is active')
def step_impl(context):
    context.bogo_cosmetics_active = True
    if not hasattr(context, 'promotion_config'):
        context.promotion_config = None

@given('the double 11 promotion is active')
def step_impl(context):
    context.double11_active = True

@when('a customer places an order with')
def step_impl(context):
    context.items = [dict(row.items()) for row in context.table]
    promotion_config = getattr(context, 'promotion_config', None)
    bogo_cosmetics_active = getattr(context, 'bogo_cosmetics_active', False)
    double11_active = getattr(context, 'double11_active', False)
    context.order_service = OrderService(
        promotions=promotion_config,
        bogo_cosmetics_active=bogo_cosmetics_active,
        double11_active=double11_active
    )
    context.order = context.order_service.place_order(context.items)

@then('the order summary should be')
def step_impl(context):
    expected = dict(context.table[0].items())
    for k in expected:
        try:
            expected[k] = int(expected[k])
        except Exception:
            pass
    actual = {}
    for k in expected:
        if k == 'totalAmount' and hasattr(context.order, 'total_amount'):
            actual[k] = context.order.total_amount
        if k == 'originalAmount' and hasattr(context.order, 'original_amount'):
            actual[k] = context.order.original_amount
        if k == 'discount' and hasattr(context.order, 'discount'):
            actual[k] = context.order.discount
    assert actual == expected, f"Expected {expected}, got {actual}"

@then('the customer should receive')
def step_impl(context):
    expected = [dict(row.items()) for row in context.table]
    actual = [
        {'productName': item.product_name, 'quantity': str(item.quantity)}
        for item in context.order.items
    ]
    for e, a in zip(expected, actual):
        assert e['productName'] == a['productName']
        assert str(e['quantity']) == str(a['quantity'])