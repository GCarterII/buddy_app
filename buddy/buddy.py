from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def testing_page():
    return render_template('walk.html')




if __name__=="__main__":
    app.run(debug=True)