import sys
import managers
import database
from flask import Flask
from flask import request
import httpResponseUtils
import exceptionUtils

app = Flask(__name__)

reader = database.DBReader("MongoDB server url here")
writer = database.DBWriter("MongoDB server url here")
client_manager = managers.ClientManager(reader, writer)
report_generator = managers.ReportGenerator()

@app.route("/")
def home():
    return "Cristina-Alexandra Burlacu, Python project."

@app.post("/api/client")
def add_client():
    try:
        name = request.form["name"]
        telephone = request.form["telephone"]
        city = request.form["city"]
        client_manager.add_client(name, telephone, city)
        return httpResponseUtils.get_success_response()
    except ValueError as e:
        return httpResponseUtils.get_error_response(str(e), 400)
    except:
        e = sys.exc_info()[1]
        return httpResponseUtils.httpResponseUtils.get_error_response(str(e), 500)

@app.get("/api/client/balance")
def show_balance():
    try:
        name = request.args.get("name")
        client = client_manager.get_client_by_name(name)
        return httpResponseUtils.get_response({'balance' : client.balance}, 200)
    except exceptionUtils.ClientNotFoundException as e:
        return httpResponseUtils.get_error_response(str(e), 400)
    except:
        e = sys.exc_info()[1]
        return httpResponseUtils.httpResponseUtils.get_error_response(str(e), 500)

@app.post("/api/client/deposit")
def deposit():
    try:
        name = request.form["name"]
        sum = float(request.form["sum"])
        client_manager.deposit(name, sum)
        return httpResponseUtils.get_success_response()
    except exceptionUtils.ClientNotFoundException as e:
        return httpResponseUtils.get_error_response(str(e), 400)
    except:
        e = sys.exc_info()[1]
        return httpResponseUtils.get_error_response(str(e), 500)

@app.post("/api/client/withdraw")
def withdraw():
    try:
        name = request.form["name"]
        sum = float(request.form["sum"])
        client_manager.withdraw(name, sum)
        return httpResponseUtils.get_success_response()
    except exceptionUtils.ClientNotFoundException as e:
        return httpResponseUtils.get_response({"error": str(e)}, 400)
    except:
        e = sys.exc_info()[1]
        return httpResponseUtils.get_error_response(str(e), 500)

@app.post("/api/client/transfer")
def transfer():
    try:
        sum = float(request.form["sum"])
        sender = request.form["sender"]
        receiver = request.form["receiver"]
        client_manager.transfer(sum, receiver, sender)
        return httpResponseUtils.get_success_response()
    except exceptionUtils.ClientNotFoundException as e:
        return httpResponseUtils.get_response({"error": str(e)}, 400)
    except:
        e = sys.exc_info()[1]
        return httpResponseUtils.get_error_response(str(e), 500)
@app.get("/api/client/extras")
def get_extras():
    try:
        name = request.args.get("client")
        client = client_manager.get_client_by_name(name)
        extras = report_generator.generate_report(client)
        return httpResponseUtils.get_response({"extras": extras}, 200)
    except exceptionUtils.ClientNotFoundException as e:
        return httpResponseUtils.get_response({"error": str(e)}, 400)
    except:
        e = sys.exc_info()[1]
        return httpResponseUtils.get_error_response(str(e), 500)

app.run(debug=True)

