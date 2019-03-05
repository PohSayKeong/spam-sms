from flask import Flask, render_template, url_for, request, flash
import fastText
import re
app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkey'

def strip_formatting(string):
    string = string.lower()
    string = re.sub(r"([.!?,'/()])", r" \1 ", string)
    return string

@app.route("/", methods=['GET', 'POST'])
def home():
    harmless_green = True
    classifier = fastText.load_model('spam_model.bin')
    if request.method == 'POST':
        normalized = strip_formatting(request.form['input_text'])
        labels = classifier.predict(normalized)
        confidence = float(str(labels[1])[1:-1]) * 100
        if str(labels[0]) == str("('__label__ham',)"):
            flash(request.form['input_text'])
            harmless_green = True
            #flash("Harmless:   " + "{0}".format(round(confidence)) + "%")
        else:
            flash(request.form['input_text'])
            harmless_green = False
            #flash("Harmful:    " + "{0}".format(round(confidence)) + "%")
    return render_template('home.html', harmless_green=harmless_green)

@app.route("/help", methods=['GET', 'POST'])
def help():
    return render_template('help.html')

if __name__ == "__main__":
    app.run(debug=True)
