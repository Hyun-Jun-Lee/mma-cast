from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: int


class Store(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._money = 0
        self.name = None
        self._products = {}

    @abstractmethod
    def show_product(self, product_id):
        pass

    @abstractmethod
    def sell_product(self, product_id, money):
        pass


class GrabStore(Store):
    def __init__(self, products):
        self._money = 0
        self.name = "그랩마켓"
        self._products = products

    def set_money(self, money):
        self.money = money

    def set_products(self, products):
        self.products = products

    def get_products(self, product_id):
        return self._products[product_id]

    def show_product(self, product_id):
        return self._products[product_id]

    def _take_money(self, money):
        self._money += money

    def _take_out_product(self, product_id, money):
        try:
            product = self._products.pop(product_id)
            self._take_money(money=money)
            return product
        except Exception as e:
            raise e

    def sell_product(self, product_id, money):
        try:
            self._take_out_product(product_id=product_id, money=money)
        except:
            raise Exception("It's not enough money")


class User:
    def __init__(self, money, store: Store):
        self._money = money
        self.store = store
        self.belongs = []

    def get_money(self):
        return self._money

    def get_belongs(self):
        return self.belongs

    def get_store(self):
        return self.store

    def see_product(self, product_id):
        products = self.store.get_products(product_id=product_id)
        return products

    def _pay(self, price):
        self._money -= price

    def _check_money_enough(self, price):
        return self._money >= price

    def _add_belong(self, product):
        self.belongs.append(product)

    def purchase_product(self, product_id):
        product = self.see_product(product_id)
        price = product.price
        if self._check_money_enough(price=price):
            self._pay(price=price)
            print(product_id)
            my_product = self.store.sell_product(product_id=product_id, money=price)
            print(my_product)
            self._add_belong(product=my_product)
            return self.belongs
        else:
            raise Exception("It's not enough money")


if __name__ == "__main__":
    store = GrabStore(
        products={
            1: Product(name="키보드", price=3000),
            2: Product(name="냉장고", price=5000),
        }
    )
    user = User(money=10000, store=store)
    user.purchase_product(product_id=2)
    print(f"user의 잔돈 : {user.get_money()}")
    print(f"user가 구매한 상품 : {user.get_belongs()}")
