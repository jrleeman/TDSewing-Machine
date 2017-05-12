from flask import Flask, redirect, render_template, url_for
import json

from forms import CreateDatasetForm

app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVyGODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/datasets/createdataset')
def dataset_createdataset():
    return render_template('createdataset.html', createdatasetform = CreateDatasetForm())


@app.route('/datasets')
def dataset_view():
    jsondata = open('datasets.json', 'r').read()
    datasets = json.loads(jsondata)
    return render_template('viewdatasets.html', datasets=datasets)


@app.route('/datasets/deletedataset')
def dataset_deletedataset():
    return redirect(url_for('dataset_view'))


if __name__ == "__main__":
    app.run(port=5000, debug=True)
