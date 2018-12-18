from flask import Flask, render_template, jsonify
import sys
import spidev

spi = spidev.SpiDev()
spi.open(1, 0)
spi.max_speed_hz = 90000

# Crane's movements int value
move = {
    'up': 1,
    'down': 2,
    'left': 3,
    'right': 4,
    'high': 5,
    'low': 6
}
message = 0
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/press/<movement>')
def press(movement):
    global message
    if message != move[movement]:
        message = move[movement]
        spi.xfer([message])

    return jsonify(message),200


@app.route('/release/<movement>')
def release(movement):
    spi.xfer([0])
    return jsonify(0),200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
