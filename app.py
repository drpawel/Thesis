from flask import Flask, render_template, jsonify
import uuid

app = Flask(__name__)


@app.route('/')
def get_default_page():
    return render_template('index.html')


@app.route('/result')
def get_result_page():
    return render_template('result.html')


@app.route('/measurement', methods=["POST"])
def add_measurement():
    return jsonify(id=uuid.uuid4())


@app.route('/result/<string:measurement_id>', methods=["GET"])
def get_result(measurement_id):
    return jsonify(id=measurement_id)


if __name__ == '__main__':
    app.run()
