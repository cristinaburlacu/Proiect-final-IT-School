from datetime import date
import entities
import stringUtils
import exceptionUtils

class ClientManager:
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer

    def add_client(self, name, phone, city):
        if stringUtils.is_none_or_empty(name):
            raise exceptionUtils.get_value_error("name")

        if stringUtils.is_none_or_empty(phone):
            raise exceptionUtils.get_value_error("phone")

        if stringUtils.is_none_or_empty(city):
            raise exceptionUtils.get_value_error("city")

        client = entities.Client(name, phone, city, 0)
        self.db_writer.insert_one(client.encode())

    def transfer(self, sum, receiver, sender):
        found_sender = self.db_reader.find_one({"name": sender})
        if found_sender == None:
            raise exceptionUtils.get_client_not_found_error(sender)

        found_receiver = self.db_reader.find_one({"name": receiver})
        if found_receiver == None:
            raise exceptionUtils.get_client_not_found_error(receiver)

        if found_sender['balance'] < sum:
            raise exceptionUtils.get_insufficient_funds_error(sender)

        transaction = entities.Transaction("Transfer", sum, receiver, sender)
        found_sender['balance'] -= sum
        found_sender['transactions'].append(transaction.encode())
        self.db_writer.update({"name": sender}, {"$set": {'balance': found_sender['balance'], 'transactions': found_sender['transactions']}})

        found_receiver['balance'] += sum
        found_receiver['transactions'].append(transaction.encode())
        print(found_receiver)
        self.db_writer.update({"name": receiver}, {"$set": {"balance": found_receiver['balance'], "transactions": found_receiver['transactions']}})

    def deposit(self, receiver, sum):
        found_receiver = self.db_reader.find_one({"name": receiver})
        if found_receiver == None:
            raise exceptionUtils.get_client_not_found_error(receiver)

        found_receiver['balance'] += sum
        transaction = entities.Transaction("Deposit", sum, receiver, None)
        found_receiver['transactions'].append(transaction.encode())
        print(found_receiver)
        self.db_writer.update({"name": receiver}, {"$set": {"balance": found_receiver['balance'], "transactions": found_receiver['transactions']}})

    def withdraw(self, client, sum):
        found_sender = self.db_reader.find_one({"name": client})
        if found_sender == None:
            raise exceptionUtils.get_client_not_found_error(client)

        if found_sender['balance'] < sum:
            raise Exception("Insufficient funds for withdrawal!")

        transaction = entities.Transaction("Withdrawal", sum, client, None)
        found_sender['balance'] -= sum
        found_sender['transactions'].append(transaction.encode())
        self.db_writer.update({"name": client}, {"$set": {'balance': found_sender['balance'], 'transactions': found_sender['transactions']}})

    def get_client_by_name(self, name):
        found_client = self.db_reader.find_one({"name": name})
        if found_client == None:
            raise exceptionUtils.get_client_not_found_error(name)

        client = entities.Client("", "", "", "")
        client.update(found_client)
        return client

class ReportGenerator:
    def generate_report(self, client):
        # folder = "Folder_extrase"
        # if not os.path.exists(folder):
        #     os.mkdir(folder)

        extras = ''
        today = date.today()

        description = f"Nume: {client.name}\n Data generarii extrasului de cont: {today}\nTotal cont: {client.balance}\nTelefon: {client.phone}\nOras: {client.city}\n"
        extras += description
        extras += "Tranzactii:\n"

        for value in client.transactions:
            extras += f"{value}\n"

        return extras