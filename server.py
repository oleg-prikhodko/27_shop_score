import os
from datetime import datetime

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://score:Rysherat2@shopscore.devman.org/shop"
db = SQLAlchemy(app)
db.Model.metadata.reflect(db.engine)


class Order(db.Model):
    __table__ = db.Model.metadata.tables["orders"]

    def __str__(self):
        return "Order: {}, {}".format(self.created, self.status)


@app.route("/")
def score():
    return render_template("score.html")


@app.route("/time")
def get_order_processing_time():
    oldest_unconfirmed_order = (
        Order.query.filter(Order.confirmed.is_(None))
        .order_by(Order.created)
        .first()
    )
    response = {"time_secs": None, "message": None}
    if oldest_unconfirmed_order is not None:
        now = datetime.now()
        delta = now - oldest_unconfirmed_order.created
        response["time_secs"] = delta.seconds
    else:
        response["message"] = "No unconfirmed orders"
    return jsonify(response)


if __name__ == "__main__":
    debug = bool(os.environ.get("FLASK_DEBUG", False))
    app.run(debug=debug)
