from flask import Flask, render_template, jsonify, request, abort
from service import service

app = Flask(__name__)


@app.route('/')
def get_default_page():
    return render_template('index.html')


@app.route('/analyze/<string:measurement_id>')
def get_analysis_page(measurement_id):
    return render_template('analysis.html', measurement_id=measurement_id)


@app.route('/measurements', methods=['POST'])
def add_measurement():
    try:
        measurement_id = service.insert_measurement(request.json)
    except Exception as err:
        return 'Occurred error: ' + str(err)

    return jsonify(id=measurement_id)


@app.route('/retrain', methods=['POST'])
def retrain_model():
    try:
        service.retrain_model()
    except Exception as err:
        return 'Occurred error: ' + str(err)
    return '', 202


@app.route('/results/<string:measurement_id>', methods=['GET'])
def get_result(measurement_id):
    is_success, probability = service.get_result(measurement_id)
    return jsonify(id=measurement_id, isSuccess=is_success, probability=probability)


if __name__ == '__main__':
    app.run()
