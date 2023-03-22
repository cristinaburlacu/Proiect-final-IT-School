def get_value_error(parameter):
    return ValueError(f"Parameter {parameter} does not have a valid value.")

def get_client_not_found_error(client):
    return ClientNotFoundException(f"Client {client} not found.")

def get_insufficient_funds_error(client):
    raise ClientNotFoundException(f"Client {client} does not have sufficient funds for making the transaction.")

class ClientNotFoundException(Exception):
    pass