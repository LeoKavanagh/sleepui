from flask import Flask, request, render_template, url_for, redirect
import datetime as dt
app = Flask(__name__)


# Database lol
today = dt.date.today().strftime('%Y-%m-%d')
latest_pred = []

def deep_sleep_pct(steps, mean_rate, sd_rate, last_night):

    b0 = 0.0
    b1 = 1.0
    b2 = 2.0
    b3 = 3.0
    b4 = 4.0

    return b0 + b1 * steps + b2 * mean_rate + b3 * sd_rate + b4 * last_night

def log_prediction(pred):
    latest_pred.append(pred)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', latest_pred=latest_pred)

@app.route('/predict', methods=['GET', 'POST'])
def predict():

    if request.method == 'POST':
        data = request.form.to_dict()

        pred = deep_sleep_pct(float(data['steps']),
                                  float(data['mean_rate']),
                                  float(data['sd_rate']),
                                  float(data['last_night']))
        data['pred'] = pred
        # Log to the 'database' so that we can show something in the if statement
        # in the index.html template
        log_prediction(pred)

        return render_template('show_prediction.html',
                               today=today,
                               steps=float(data['steps']),
                               mean_rate=float(data['mean_rate']),
                               sd_rate=float(data['sd_rate']),
                               last_night=float(data['last_night']),
                               pred=float(data['pred']))

    return render_template('input_data.html')

if __name__ == '__main__':
    app.run(debug=True)
