from workerA import add_nums, get_accuracy, get_predictions

from flask import (
   Flask,
   request,
   jsonify,
   Markup,
   render_template 
)

#app = Flask(__name__, template_folder='./templates',static_folder='./static')
app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Welcome to the Group 6's project</h1>"

@app.route("/accuracy", methods=['POST', 'GET'])
def accuracy():
    if request.method == 'POST':
        r = get_accuracy.delay()
        a = r.get()
        return '<h1>The r2score is {}</h1>'.format(a)

    return '''<form method="POST">
    <input type="submit">
    </form>'''

@app.route("/predictions", methods=['POST', 'GET'])
def predictions():
    if request.method == 'POST':
        results = get_predictions.delay()
        predictions = results.get()

        results = get_accuracy.delay()
        score = results.get()

        final_results = predictions

        return render_template('result.html', score=score ,final_results=final_results)

    return '''<form method="POST">
    <input type="submit">
    </form>'''

if __name__ == '__main__':
    app.run(host = '0.0.0.0',port=5100,debug=True)
