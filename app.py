from flask import Flask, render_template, jsonify
import uuid

app = Flask(__name__)


@app.route('/')
def get_default_page():
    return render_template('index.html')


@app.route('/analyze/<string:measurement_id>')
def get_analysis_page(measurement_id):
    # return render_template('analysis.html', measurement_id)
    return render_template('analysis.html')


@app.route('/measurements', methods=["POST"])
def add_measurement():
    return jsonify(id=uuid.uuid4())


@app.route('/results/<string:measurement_id>', methods=["GET"])
def get_result(measurement_id):
    return jsonify(id=measurement_id)


if __name__ == '__main__':
    app.run()
