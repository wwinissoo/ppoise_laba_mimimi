from datetime import datetime

import pytest

from culinary.exceptions import InvalidOrderException, OrderStateError, PaymentError
from culinary.orders import CustomerOrder, Delivery, Menu, MenuItem, Order, OrderItem, Payment, Receipt
from culinary.people import Customer
from culinary.warehouse import Purchase, Supplier


@pytest.fixture
def order(dish, customer):
    return Order("1", customer, [OrderItem(dish, 2, 150)])


class TestOrderItem:
    def test_totals(self, dish):
        item = OrderItem(dish, 2, 150, " без лука ")
        assert item.dish is dish and item.note == "без лука" and item.calculate_total() == 300
        item.increase_quantity(1)
        item.update_unit_price(100)
        assert item.quantity == 3 and item.unit_price == 100 and item.calculate_total() == 300
        item.update_quantity(1)
        assert item.quantity == 1

    def test_notes(self, dish):
        item = OrderItem(dish, 1, 100)
        item.add_note("острое")
        item.add_note("с собой")
        item.add_note("")
        assert item.note == "острое; с собой"

    def test_validation(self, dish):
        with pytest.raises(ValueError):
            OrderItem(dish, 1.5, 150)
        with pytest.raises(ValueError):
            OrderItem(dish, 1, -1)
        with pytest.raises(TypeError):
            OrderItem("салат", 1, 150)


class TestOrder:
    def test_items_are_read_only(self, order, dish):
        with pytest.raises(AttributeError):
            order.items.append(OrderItem(dish, 1, 150))
        assert order.order_number == "1" and isinstance(order.created_at, datetime)
        assert order.calculate_total() == 300 and order.count_portions() == 2

    def test_editing(self, order, dish):
        extra = OrderItem(dish, 1, 150)
        order.add_item(extra)
        assert order.remove_item(extra) and not order.remove_item(extra)
        with pytest.raises(InvalidOrderException):
            order.remove_item(order.items[0])
        order.replace_items([extra])
        assert order.items == (extra,)
        with pytest.raises(TypeError):
            order.add_item("салат")

    def test_status_transitions(self, order, dish):
        order.change_status(Order.COOKING)
        order.change_status(Order.COOKING)
        with pytest.raises(OrderStateError):
            order.add_item(OrderItem(dish, 1, 150))
        with pytest.raises(OrderStateError):
            order.change_status(Order.HANDED_OVER)
        with pytest.raises(OrderStateError):
            order.change_status("потерян")
        order.change_status(Order.READY)
        assert order.status == Order.READY

    def test_validation(self, dish, customer):
        item = OrderItem(dish, 1, 150)
        with pytest.raises(OrderStateError):
            Order(" ", customer, [item])
        with pytest.raises(OrderStateError):
            Order("2", customer, [item], Order.READY)
        with pytest.raises(TypeError):
            Order("3", "Анна", [item])
        with pytest.raises(TypeError):
            Order("4", customer, [item], created_at="вчера")
        with pytest.raises(TypeError):
            Order("5", customer, ["салат"])
        with pytest.raises(InvalidOrderException):
            Order("6", customer, [])


class TestPayment:
    def test_cash_with_change(self, order):
        payment = Payment(order, 500, "наличные")
        assert payment.order is order and payment.method == "наличные" and payment.purpose == Payment.FOR_ORDER
        assert payment.process() == 200 and payment.is_paid() and payment.charged_amount == 300
        with pytest.raises(PaymentError):
            payment.process()
        assert payment.refund() == 300 and payment.is_refunded()
        with pytest.raises(PaymentError):
            payment.refund()

    def test_declined(self, order):
        card = Payment(order, 400, "карта")
        with pytest.raises(PaymentError):
            card.process()
        assert card.status == Payment.DECLINED
        short = Payment(order, 100, "наличные")
        with pytest.raises(PaymentError):
            short.process()

    def test_expected_amount_override(self, order):
        payment = Payment(order, 100, "онлайн", purpose=Payment.FOR_DELIVERY, expected_amount=100)
        assert payment.expected_amount == 100 and payment.process() == 0 and payment.amount == 100

    @pytest.mark.parametrize(
        "amount, method, status, purpose, expected",
        [
            (-1, "карта", "ожидает", "заказ", None),
            (1, "бартер", "ожидает", "заказ", None),
            (1, "карта", "ожидает", "чаевые", None),
            (1, "карта", "оплачено", "заказ", None),
            (1, "карта", "ожидает", "заказ", -5),
        ],
    )
    def test_validation(self, order, amount, method, status, purpose, expected):
        with pytest.raises(PaymentError):
            Payment(order, amount, method, status, purpose, expected)

    def test_requires_payable_object(self):
        with pytest.raises(TypeError):
            Payment("заказ", 1, "карта")

    def test_pays_purchase(self, tomato):
        purchase = Purchase(Supplier("Ферма", "+7 900", [tomato]), tomato, 2, 100)
        payment = Payment(purchase, 200, "карта", purpose=Payment.FOR_PURCHASE)
        assert payment.process() == 0


class TestReceipt:
    def test_lifecycle(self, order):
        payment = Payment(order, 300, "карта")
        receipt = Receipt(order, payment, "R-1")
        assert receipt.order is order and receipt.payment is payment and receipt.receipt_number == "R-1"
        with pytest.raises(PaymentError):
            receipt.issue()
        payment.process()
        assert receipt.issue() == "R-1" and receipt.issued
        with pytest.raises(PaymentError):
            receipt.issue()
        with pytest.raises(PaymentError):
            receipt.void()
        payment.refund()
        receipt.void()
        assert not receipt.issued
        with pytest.raises(PaymentError):
            receipt.void()
        assert receipt.format_lines() == ["Чек R-1, заказ 1", "Салат × 2: 300.00", "Итого: 300.00 (карта)"]

    def test_issued_on_creation(self, order):
        payment = Payment(order, 300, "карта")
        payment.process()
        assert Receipt(order, payment, "R-2", True).issued

    def test_validation(self, order, dish, customer):
        payment = Payment(order, 300, "карта")
        other = Order("2", customer, [OrderItem(dish, 1, 150)])
        with pytest.raises(TypeError):
            Receipt("заказ", payment, "R")
        with pytest.raises(TypeError):
            Receipt(order, "платёж", "R")
        with pytest.raises(PaymentError):
            Receipt(other, payment, "R")


class TestCustomerOrder:
    def test_delivery_request(self, order, customer):
        link = CustomerOrder(customer, order, "ул. Ленина, 1", True)
        assert link.customer is customer and link.order is order and link.get_customer_name() == "Анна"
        assert link.delivery_required and link.delivery_address == "ул. Ленина, 1"
        link.cancel_delivery()
        assert not link.delivery_required and link.delivery_address == ""
        with pytest.raises(ValueError):
            link.request_delivery(" ")

    def test_validation(self, order, customer):
        stranger = Customer("Борис", "+7 900 555-55-55", "", 30)
        with pytest.raises(TypeError):
            CustomerOrder("Анна", order)
        with pytest.raises(TypeError):
            CustomerOrder(customer, "заказ")
        with pytest.raises(InvalidOrderException):
            CustomerOrder(stranger, order)


class TestDelivery:
    def test_lifecycle(self, order):
        delivery = Delivery(order, " ул. Ленина, 1 ", 100)
        assert delivery.order is order and delivery.address == "ул. Ленина, 1" and delivery.delivery_fee == 100
        assert delivery.calculate_total() == 400
        with pytest.raises(OrderStateError):
            delivery.update_status(Delivery.DELIVERED)
        for status in (Delivery.PREPARING, Delivery.IN_TRANSIT, Delivery.DELIVERED):
            delivery.update_status(status)
        assert delivery.is_completed() and delivery.status == Delivery.DELIVERED and not delivery.is_cancelled()

    def test_validation(self, order):
        with pytest.raises(TypeError):
            Delivery("заказ", "адрес")
        with pytest.raises(OrderStateError):
            Delivery(order, "адрес", 0, Delivery.DELIVERED)
        with pytest.raises(ValueError):
            Delivery(order, " ")
        with pytest.raises(ValueError):
            Delivery(order, "адрес", -1)


def test_orders_package_reexports_menu_classes():
    from culinary.dishes import Menu as DishMenu, MenuItem as DishMenuItem

    assert Menu is DishMenu and MenuItem is DishMenuItem
