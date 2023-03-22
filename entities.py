class Client:
    def __init__(self, name, phone, city, balance):
        self.name = name
        self.phone = phone
        self.city = city
        self.balance = balance
        self.transactions = []
    def update(self, dictionary):
        self.__dict__.update(dictionary)


    def encode(self):
        return self.__dict__

class Transaction:
    def __init__(self, type, sum, receiver, sender):
        self.type = type
        self.sender = sender
        self.receiver = receiver
        self.sum = sum

    def encode(self):
        return self.__dict__