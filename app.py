# import dependencies
from flask import Flask, jsonify

# flask setup
app = Flask(__name__)

# define home route
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )















if __name__ == "__main__":
    app.run(debug=True)
