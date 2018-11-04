from flask import Flask, request, render_template, url_for, redirect
import datetime as dt
app = Flask(__name__)


# Database lol
today = dt.date.today().strftime('%Y-%m-%d')
latest_pred = []


def deep_sleep_pct(steps, mean_rate, sd_rate, dsp_lag):

    b0 = -0.1176
    b1 = 0.00
    b2 = 0.048
    b3 = -0.0029
    b4 = 0.2040

    return b0 + b2 * mean_rate + b3 * sd_rate + b4 * dsp_lag

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
                                  float(data['dsp_lag']))
        data['pred'] = pred
        # Log to the 'database' so that we can show something in the if statement
        # in the index.html template
        log_prediction(pred)

        return render_template('show_prediction.html',
                               today=today,
                               steps=float(data['steps']),
                               mean_rate=float(data['mean_rate']),
                               sd_rate=float(data['sd_rate']),
                               dsp_lag=float(data['dsp_lag']),
                               pred=float(data['pred']))

    return render_template('input_data.html')


if __name__ == '__main__':
    app.run(debug=True)
