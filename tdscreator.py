from flask import Flask, redirect, render_template, url_for, request
import json

from forms import CreateDatasetForm

app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVyGODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/datasets/createdataset', methods=['GET','POST'])
def dataset_createdataset():
    form = CreateDatasetForm(request.form)
    if request.method=='POST' and form.validate():
        name = form.name.data
        path = form.path.data
        metadata = form.metadata.data
        jsondata = open('datasets.json', 'r').read()
        datasets = json.loads(jsondata)
        datasets.append({"name":name, "path":name, "metadata":name})
        with open('datasets.json', 'w') as outfile:
            json.dump(datasets, outfile)
        return redirect(url_for('dataset_view'))
    return render_template('createdataset.html', createdatasetform=form)


@app.route('/datasets')
def dataset_view():
    jsondata = open('datasets.json', 'r').read()
    datasets = json.loads(jsondata)
    return render_template('viewdatasets.html', datasets=datasets)


@app.route('/datasets/deletedataset')
def dataset_deletedataset():
    dataset_name = request.args.get("dataset_name")
    jsondata = open('datasets.json', 'r').read()
    datasets = json.loads(jsondata)
    for i, dataset in enumerate(datasets):
        print("Comparing", dataset["name"], dataset_name)
        if dataset["name"] == dataset_name:
            print("Deleting!", dataset_name)
            del datasets[i]
            break

    with open('datasets.json', 'w') as outfile:
        json.dump(datasets, outfile)
    return redirect(url_for('dataset_view'))


@app.route('/featurecollections')
def featurecollections_view():
    return render_template('viewfeaturecollections.html')


if __name__ == "__main__":
    app.run(port=5000, debug=True)