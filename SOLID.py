from abc import ABC, abstractmethod
from typing import List


class Order:
    def __init__(self, items=None):
        if items is None:
            self.items = [
                {"name": "Book", "price": 100.5},
                {"name": "Pen", "price": 49.9},
                {"name": "Notebook", "price": 19.9},
                {"name": "Pencil", "price": 15.9},
                {"name": "Eraser", "price": 9.99},
            ]
        else:
            self.items = items
        self.cart = []
        self.name = []

    def show_shop(self):
        for item in self.items:
            print(item['name'], item['price'])  

    def user(self):
        while True:
            user_enter = input('Enter product(9-place an order; 0-exit): ')
            
            if user_enter == '9':
                if self.cart != []:
                    print('~ Excellent choice! ~')
                    User_pay_mail().user_methods(self.cart)        
                    break 
                print('Your cart is empty')   
                self.user()    

            if user_enter == '0':
                print('Exit')
                break  

            found = False

            for item in self.items:
                if user_enter.lower() == item['name'].lower():
                    self.cart.append(item["price"])
                    self.name.append(item["name"])
                    print(f"Your cart: {', '.join(self.name)} ; Total: {sum(self.cart)}")
                    found = True

            if not found:
                print('Error')


class User_pay_mail:       

    def __init__(self):
        self.payments = {
        '1': CreditCardPayment,
        '2': PayPalPayment,
        }
        self.notifiers = {
            '1': EmailNotifier,
            '2': SMSNotifier,
        }      

    def user_methods(self, cart):
        while True:
            user_pay = input('1-card, 2-paypal: ')
            user_mail = input('1-email, 2-sms: ')

            payment_cls = self.payments.get(user_pay)
            if not payment_cls:
                print("Invalid payment method")
                return
            payment = payment_cls()

            notifier_cls = self.notifiers.get(user_pay)
            if not notifier_cls:
                print("Invalid notifier method")
                return
            notifier = notifier_cls()
               
            service = OrderService(payment, notifier)
            service.process_order(self, sum(cart))
            break
                              

    # TODO: Order не должен заниматься логикой оплаты или уведомлений


class PaymentMethod(ABC):
    def __init__(self):
        self.user_cash = 150
        
    @abstractmethod
    def pay(self, amount: float) -> bool:

        """
        TODO:
        Виртуальный метод оплаты.
        Все способы оплаты должны корректно подставляться вместо базового класса
        """
        pass


class CreditCardPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        if self.user_cash < amount:
            print("You don't have enough money")
            return False
        else:
            print(f'Paid {amount} by card')
            return True
    # TODO: реализовать оплату картой
        pass


class PayPalPayment(PaymentMethod):
    def pay(self, amount: float) -> bool:
        if self.user_cash < amount:
            print("You don't have enough money")
            return False
        else:
            print(f'Paid {amount} by paypal')
            return True
    # TODO: реализовать оплату через PayPal
        pass


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        """
        TODO:
        Интерфейс только для уведомлений
        """
        pass


class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f'Email sent: {message}')
    # TODO: реализовать email-уведомление
        pass


class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f'SMS sent : {message}')
    # TODO: реализовать SMS-уведомление
        pass


class OrderService:
    def __init__(
        self,
        payment_method: PaymentMethod,
        notifier: Notifier
    ):
        """
        TODO:
        Зависимости должны быть от абстракций, а не от конкретных классов
        """
        self.payment_method = payment_method
        self.notifier = notifier

    def process_order(self, order: Order, amount: float) -> None:
        if not self.payment_method.pay(amount):
            print('Order cancelled')
            return
        
        self.notifier.send(f'Order confirmed. Total: {amount}')
        # TODO:
        # 1. Провести оплату
        # 2. Отправить уведомление
        

o = Order()
o.show_shop()
o.user()    