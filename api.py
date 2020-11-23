# Setup Flask Server

from flask import Flask, config, jsonify
from flask.json import JSONEncoder
from flask_restful import Api, Resource

from analysis.recurrences import RecurringCalculator, Recurring
from receiver.receiver import LsbReceiver
from receiver.transactions import Transaction


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Recurring):
            return {"members": obj.members, "variance": obj.variance}
        if isinstance(obj, Transaction):
            return {
                "description": obj.description,
                "date": obj.date(),
                "amount": obj.amount,
            }
        return super(CustomEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = CustomEncoder
api = Api(app)

transactions = []


class GetRecurrences(Resource):
    @staticmethod
    def get():
        calculator = RecurringCalculator(transactions)
        recurring = calculator.find_recurrences()
        return jsonify({"data": recurring})


# Api resource routing
api.add_resource(GetRecurrences, "/recurring")

if __name__ == "__main__":
    receiver = LsbReceiver("data/export.csv")
    transactions = receiver.decode()
    app.run(debug=True)
