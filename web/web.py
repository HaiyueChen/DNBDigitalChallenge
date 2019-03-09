from flask import *

app = Flask(__name__)

localhost = '127.0.0.1'

@app.route('/')
def index():
    """
    goto overview.html
    """
    return redirect(url_for('overview'))

@app.route('/overview')
def overview():
    """
    Renders overview.html
    """
    return render_template('overview.html')

@app.route('/add_receipt')
def add_receipt():
    """
    Renders add_receipt.html
    """
    return render_template('add_receipt.html')


if __name__ == "__main__":
    app.run(host=localhost, port=5005, debug=True)
