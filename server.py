import os
from datetime import date, datetime

from flask import Flask, jsonify, render_template, send_file
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://score:Rysherat2@shopscore.devman.org/shop"
db = SQLAlchemy(app)


class Order(db.Model):
    """This class represent a record in orders table.
    Only two columns from that table matters to the program:
    'created' - order creation date and time,
    'confirmed' - order confirmation date and time
    """

    __table__ = db.Table(
        "orders",
        db.Model.metadata,
        db.Column("created", db.DateTime),
        db.Column("confirmed", db.DateTime),
        autoload=True,
        autoload_with=db.engine,
    )

    def __str__(self):
        return "Order<created: {}, confirmed: {}>".format(
            self.created, self.confirmed
        )


def get_orders_info():
    orders_info = {
        "time_secs": None,
        "confirmed_today": 0,
        "total_uncomfirmed": 0,
    }

    unconfirmed_condition = Order.confirmed.is_(None)
    unconfirmed_orders_count = Order.query.filter(
        unconfirmed_condition
    ).count()
    orders_info["total_uncomfirmed"] = unconfirmed_orders_count
    oldest_unconfirmed_order = None

    if unconfirmed_orders_count > 0:
        oldest_unconfirmed_order = (
            Order.query.filter(unconfirmed_condition)
            .order_by(Order.created)
            .first()
        )
        now = datetime.now()
        delta = now - oldest_unconfirmed_order.created
        orders_info["time_secs"] = delta.seconds

    confirmed_today_count = Order.query.filter(
        db.cast(Order.confirmed, db.Date) == date.today()
    ).count()
    orders_info["confirmed_today"] = confirmed_today_count

    return orders_info


@app.route("/")
def score():
    return render_template("score.html")


@app.route("/info")
def get_orders_info_json():
    return jsonify(get_orders_info())


@app.route("/robots.txt")
def get_robots_file():
    return send_file("robots.txt")


if __name__ == "__main__":
    DEFAULT_PORT = 5000
    debug = bool(os.environ.get("FLASK_DEBUG", False))
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    app.run(debug=debug, host="0.0.0.0", port=port)
