from flask import Flask, render_template, url_for, request, flash
import fastText
app = Flask(__name__)

app.config['SECRET_KEY'] = 'ed025c9f99a6e3d55185'

@app.route("/", methods=['GET', 'POST'])
def home():
    classifier = fastText.load_model('spam_model.bin')
    if request.method == 'POST':
        labels = classifier.predict(request.form['input_text'])
        confidence = float(str(labels[1])[1:-1]) * 100
        if str(labels[0]) == str("('__label__ham',)"):
            flash("Text: " + request.form['input_text'])
            flash("Harmless:   " + "{0}".format(round(confidence)) + "%")
        else:
            flash("Text: " + request.form['input_text'])
            flash("Harmful:    " + "{0}".format(round(confidence)) + "%")
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
