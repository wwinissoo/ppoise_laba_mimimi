from datetime import date, timedelta

import pytest

from culinary.exceptions import InsufficientIngredientError, OrderStateError, SupplierError, WarehouseCapacityError
from culinary.ingredients import Vegetable
from culinary.warehouse import (
    Delivery,
    ExpirationTracker,
    Inventory,
    InventoryManager,
    ProductBatch,
    Purchase,
    Stock,
    StockItem,
    Supplier,
    SupplierDelivery,
    Warehouse,
)


@pytest.fixture
def supplier(tomato):
    return Supplier("Ферма", "+7 900 777-77-77", [tomato], 0)


@pytest.fixture
def cucumber():
    return Vegetable("Огурец", 5000, 100, 15, 7, 4)


class TestStockItem:
    def test_movements(self, tomato):
        item = StockItem(tomato, 1, minimum_kg=3, location_code="B-2")
        assert item.ingredient is tomato and item.location_code == "B-2" and item.minimum_kg == 3
        assert item.needs_restock() and item.calculate_shortage() == 2
        item.receive(4)
        item.withdraw(1)
        assert item.quantity_kg == 4 and not item.needs_restock() and item.calculate_shortage() == 0
        item.relocate("C-1")
        assert item.location_code == "C-1"

    def test_validation(self, tomato):
        item = StockItem(tomato, 1)
        with pytest.raises(InsufficientIngredientError):
            item.withdraw(5)
        with pytest.raises(ValueError):
            item.withdraw(0)
        with pytest.raises(ValueError):
            item.receive(-1)
        for args in [("томат", 1), (tomato, -1), (tomato, 1, -1)]:
            with pytest.raises((TypeError, ValueError)):
                StockItem(*args)


class TestWarehouse:
    def test_capacity_and_encapsulation(self, tomato, cucumber):
        warehouse = Warehouse(" Склад ", " Цех ", [StockItem(tomato, 1)], 2)
        assert warehouse.name == "Склад" and warehouse.location == "Цех" and warehouse.capacity_kg == 2
        assert warehouse.calculate_free_capacity() == 1 and warehouse.has_free_capacity(1)
        with pytest.raises(AttributeError):
            warehouse.stock_items.append(StockItem(tomato, 100))
        with pytest.raises(WarehouseCapacityError):
            warehouse.add_stock_item(StockItem(cucumber, 5))
        with pytest.raises(WarehouseCapacityError):
            Warehouse("Склад", "", [StockItem(tomato, 5)], 2)
        with pytest.raises(WarehouseCapacityError):
            Warehouse("Склад", "", capacity_kg=-1)
        with pytest.raises(ValueError):
            warehouse.has_free_capacity(-1)

    def test_registry(self, tomato):
        warehouse = Warehouse("Склад", "")
        warehouse.add_stock_item(StockItem(tomato, 0))
        with pytest.raises(ValueError):
            warehouse.add_stock_item(StockItem(tomato, 1))
        with pytest.raises(TypeError):
            warehouse.add_stock_item("томат")
        assert warehouse.get_stock_item(" ПОМИДОР ") is not None and warehouse.get_available_quantity("лук") == 0
        assert warehouse.remove_stock_item("Помидор") and not warehouse.remove_stock_item("Помидор")

    def test_cannot_remove_non_empty(self, tomato):
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1)])
        with pytest.raises(ValueError):
            warehouse.remove_stock_item(tomato)

    def test_deduct(self, tomato):
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1)], 10)
        warehouse.deduct_ingredient(tomato, 0.25)
        assert tomato.weight == 750
        with pytest.raises(InsufficientIngredientError):
            warehouse.deduct_ingredient(tomato, 5)
        with pytest.raises(ValueError):
            warehouse.deduct_ingredient(tomato, 0)
        lookalike = Vegetable("Помидор", 1000, 200, 18, 7, 4)
        with pytest.raises(InsufficientIngredientError):
            warehouse.deduct_ingredient(lookalike, 0.1)

    def test_deduct_checks_batch_weight(self, tomato):
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 5)], 10)
        with pytest.raises(InsufficientIngredientError):
            warehouse.deduct_ingredient(tomato, 2)

    def test_write_off_expired(self, tomato, cucumber):
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1), StockItem(cucumber, 5)], 10)
        for _ in range(tomato.expiration_days):
            tomato.pass_day()
        assert warehouse.find_expired()[0].ingredient is tomato
        assert warehouse.write_off_expired() == pytest.approx(1)
        assert tomato.weight == 0 and warehouse.write_off_expired() == 0


class TestSupplier:
    def test_assortment_and_rating(self, supplier, tomato, cucumber):
        assert supplier.name == "Ферма" and supplier.phone == "+7 900 777-77-77" and supplier.rating == 0
        supplier.add_product(tomato)
        supplier.add_product(cucumber)
        assert supplier.products == (tomato, cucumber) and supplier.supplies("огурец")
        supplier.rate(5)
        assert supplier.is_reliable()
        with pytest.raises(SupplierError):
            supplier.rate(6)
        with pytest.raises(TypeError):
            supplier.add_product("лук")

    def test_validation(self):
        with pytest.raises(SupplierError):
            Supplier("", "+7 900")
        with pytest.raises(SupplierError):
            Supplier("Ферма", "+7 900", rating=7)


class TestPurchase:
    def test_lifecycle(self, supplier, tomato):
        purchase = Purchase(supplier, tomato, 2, 180)
        assert purchase.supplier is supplier and purchase.ingredient is tomato and purchase.unit_price == 180
        assert purchase.calculate_total() == 360 and purchase.quantity_kg == 2
        with pytest.raises(OrderStateError):
            purchase.mark_received()
        purchase.mark_paid()
        with pytest.raises(OrderStateError):
            purchase.mark_paid()
        purchase.mark_received()
        assert purchase.received and purchase.status == Purchase.RECEIVED
        with pytest.raises(OrderStateError):
            purchase.cancel()

    def test_cancel(self, supplier, tomato):
        purchase = Purchase(supplier, tomato, 2, 180)
        purchase.cancel()
        assert purchase.status == Purchase.CANCELLED

    def test_validation(self, supplier, tomato, cucumber):
        with pytest.raises(SupplierError):
            Purchase(supplier, cucumber, 5, 90)
        with pytest.raises(TypeError):
            Purchase("ферма", tomato, 1, 1)
        with pytest.raises(TypeError):
            Purchase(supplier, "томат", 1, 1)
        with pytest.raises(ValueError):
            Purchase(supplier, tomato, 0, 1)


class TestProductBatch:
    def test_usage(self, supplier, tomato):
        batch = ProductBatch(tomato, "B1", date.today() - timedelta(days=10), 5, supplier)
        assert batch.ingredient is tomato and batch.supplier is supplier and batch.quantity_kg == 5
        assert batch.is_expired() and not batch.is_expired(batch.received_date)
        batch.use(2)
        assert batch.remaining_quantity() == 3
        with pytest.raises(InsufficientIngredientError):
            batch.use(4)
        with pytest.raises(ValueError):
            batch.use(0)
        assert batch.assign_batch_code("FARM") == batch.assign_batch_code("FARM") == batch.batch_code == "FARM-B1"

    @pytest.mark.parametrize("field", ["ingredient", "supplier", "date", "quantity"])
    def test_validation(self, supplier, tomato, field):
        args = {"ingredient": tomato, "supplier": supplier, "date": date.today(), "quantity": 1}
        args[field] = 0 if field == "quantity" else "неверно"
        with pytest.raises((TypeError, ValueError)):
            ProductBatch(args["ingredient"], "B1", args["date"], args["quantity"], args["supplier"])


class TestSupplierDelivery:
    def test_empty_delivery(self, supplier):
        delivery = SupplierDelivery(supplier, delivery_date=date(2026, 1, 1))
        assert (
            delivery.supplier is supplier
            and delivery.delivery_date == date(2026, 1, 1)
            and Delivery is SupplierDelivery
        )
        with pytest.raises(SupplierError):
            delivery.dispatch()
        with pytest.raises(SupplierError):
            delivery.mark_received()

    def test_lifecycle(self, supplier, tomato):
        batch = ProductBatch(tomato, "B1", date.today(), 5, supplier)
        delivery = SupplierDelivery(supplier)
        delivery.add_batch(batch)
        with pytest.raises(SupplierError):
            delivery.add_batch(batch)
        delivery.dispatch()
        delivery.mark_received()
        assert (
            delivery.status == "получена"
            and delivery.calculate_delivered_weight() == 5
            and delivery.batches == (batch,)
        )
        with pytest.raises(SupplierError):
            delivery.cancel()
        with pytest.raises(SupplierError):
            delivery.add_batch(ProductBatch(tomato, "B2", date.today(), 1, supplier))

    def test_validation(self, supplier, tomato):
        other = Supplier("Другой", "+7 900 888-88-88", [tomato])
        batch = ProductBatch(tomato, "B1", date.today(), 5, supplier)
        with pytest.raises(SupplierError):
            SupplierDelivery(other).add_batch(batch)
        with pytest.raises(TypeError):
            SupplierDelivery(supplier).add_batch("партия")
        with pytest.raises(TypeError):
            SupplierDelivery("ферма")
        with pytest.raises(SupplierError):
            SupplierDelivery(supplier, status="получена")
        with pytest.raises(TypeError):
            SupplierDelivery(supplier, delivery_date="завтра")
        cancelled = SupplierDelivery(supplier, [batch])
        cancelled.cancel()
        assert cancelled.status == "отменена"


class TestInventory:
    def test_counting(self, tomato):
        item = StockItem(tomato, 1)
        warehouse = Warehouse("Склад", "", [item], 10)
        inventory = Inventory(warehouse, "Иван", inventory_date=date(2026, 1, 1))
        assert inventory.warehouse is warehouse and inventory.counted_by == "Иван"
        assert inventory.inventory_date == date(2026, 1, 1) and inventory.find_uncounted() == [item]
        assert not inventory.is_balanced()
        inventory.record_count(item, 0.9)
        assert inventory.find_discrepancies()[item] == pytest.approx(-0.1) and inventory.counted_items == {item: 0.9}
        assert Inventory(warehouse, "Пётр", {item: 1}).is_balanced()

    def test_validation(self, tomato):
        item = StockItem(tomato, 1)
        inventory = Inventory(Warehouse("Склад", "", [item]), "Иван")
        with pytest.raises(ValueError):
            inventory.record_count(StockItem(tomato, 1), 1)
        with pytest.raises(ValueError):
            inventory.record_count(item, -1)
        with pytest.raises(TypeError):
            inventory.record_count("томат", 1)
        with pytest.raises(TypeError):
            Inventory("склад", "Иван")


class TestInventoryManager:
    def test_reports(self, tomato):
        warehouse = Warehouse("Склад", "", [StockItem(tomato, 1, minimum_kg=3)], 10)
        manager = InventoryManager(warehouse)
        assert manager.warehouse is warehouse and manager.calculate_stock_value() == 200
        assert manager.find_reorder_candidates()[0].ingredient is tomato
        assert manager.calculate_reorder_quantities() == {"Помидор": 2}
        assert manager.create_inventory_report() == {"Помидор": 1}
        with pytest.raises(TypeError):
            InventoryManager("склад")


class TestExpirationTracker:
    def test_tracking(self, tomato, cucumber):
        tracker = ExpirationTracker([tomato, tomato])
        tracker.register(cucumber)
        assert tracker.ingredients == (tomato, cucumber) and tracker.expiring_within(1) == []
        for _ in range(6):
            tracker.advance_day()
        assert tracker.expiring_within(1) == [tomato, cucumber]
        tracker.advance_day()
        assert tracker.expired_items() == [tomato, cucumber] and tracker.fresh_items() == []
        with pytest.raises(TypeError):
            tracker.register("томат")


class TestStock:
    def test_index(self, tomato, cucumber):
        stock = Stock()
        stock.add_item(StockItem(tomato, 1, minimum_kg=2))
        stock.add_item(StockItem(cucumber, 5))
        assert stock.get_item(" помидор ").quantity_kg == 1 and len(stock.items) == 2
        assert stock.total_quantity() == 6 and [item.ingredient for item in stock.below_minimum()] == [tomato]
        with pytest.raises(ValueError):
            stock.add_item(StockItem(tomato, 2))
        with pytest.raises(TypeError):
            stock.add_item("томат")
