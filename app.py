from flask import Flask, render_template, redirect, url_for, request
import uuid

app = Flask(__name__)


@app.route('/')
def get_default_page():
    return render_template('index.html')


@app.route('/add', methods=["POST"])
def add_measurement():
    return redirect(url_for('get_result', measurement_id=uuid.uuid4()))


@app.route('/result/<string:measurement_id>')
def get_result(measurement_id):
    print(measurement_id)
    return render_template('result.html')


if __name__ == '__main__':
    app.run()
