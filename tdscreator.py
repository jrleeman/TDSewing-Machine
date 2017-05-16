from flask import Flask, redirect, render_template, url_for, request
import json

from forms import CreateDatasetForm, CreateFeatureCollectionForm

app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVyGODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/datasets/createdataset', methods=['GET','POST'])
def dataset_createdataset():
    form = CreateDatasetForm(request.form)
    jsondata = open('datasets.json', 'r').read()
    datasets = json.loads(jsondata)
    form.path.choices = populate_choices(datasets)
    if request.method=='POST':# and form.validate():
        name = form.name.data
        path = form.path.data
        metadata = form.metadata.data
        jsondata = open('datasets.json', 'r').read()
        datasets = json.loads(jsondata)
        id = datasets[-1]['_id'] + 1
        datasets.append({"_id":id, "name":name, "parent_dataset":int(path), "metadata":metadata, "feature_collections":[]})
        with open('datasets.json', 'w') as outfile:
            json.dump(datasets, outfile)
        return redirect(url_for('dataset_view'))
    return render_template('createdataset.html', createdatasetform=form)


@app.route('/datasets/editdataset', methods=['GET','POST'])
def dataset_editdataset():
    form = CreateDatasetForm(request.form)
    jsondata = open('datasets.json', 'r').read()
    datasets = json.loads(jsondata)
    form.path.choices = populate_choices(datasets)
    if request.method=='POST':# and form.validate():
        name = form.name.data
        path = form.path.data
        metadata = form.metadata.data
        jsondata = open('datasets.json', 'r').read()
        datasets = json.loads(jsondata)
        id = datasets[-1]['_id'] + 1
        datasets.append({"_id":id, "name":name, "parent_dataset":int(path), "metadata":metadata, "feature_collections":[]})
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
    jsondata = open('featurecollections.json', 'r').read()
    featurecollections = json.loads(jsondata)
    return render_template('viewfeaturecollections.html', featurecollections=featurecollections)


@app.route('/featurecollections/createfeaturecollection', methods=['GET','POST'])
def featurecollections_createfeaturecollection():
    form = CreateFeatureCollectionForm(request.form)
    if request.method=='POST' and form.validate():
        name = form.name.data
        xml = form.xml.data
        jsondata = open('featurecollections.json', 'r').read()
        datasets = json.loads(jsondata)
        datasets.append({"name":name, "xml":xml})
        with open('featurecollections.json', 'w') as outfile:
            json.dump(datasets, outfile)
        return redirect(url_for('featurecollections_view'))
    return render_template('createfeaturecollection.html', createfeaturecollectionform=form)


@app.route('/featurecollections/deletefeaturecollection')
def featurecollections_deletefeaturecollection():
    featurecollection_name = request.args.get("featurecollection_name")
    jsondata = open('featurecollections.json', 'r').read()
    featurecollections = json.loads(jsondata)
    for i, featurecollection in enumerate(featurecollections):
        if featurecollection["name"] == featurecollection_name:
            del featurecollections[i]
            break

    with open('featurecollections.json', 'w') as outfile:
        json.dump(featurecollections, outfile)
    return redirect(url_for('featurecollections_view'))


def get_dataset_byid(datasets, id):
    for dataset in datasets:
        if dataset['_id'] == id:
            return dataset


def get_path(datasets, dataset):
    path = []
    ds = dataset
    while ds['parent_dataset'] != "None":
        path.append(ds['name'])
        ds = get_dataset_byid(datasets, ds['parent_dataset'])
    path_str = ""
    for item in path[::-1]:
        path_str += "/" + item
    return path_str

def populate_choices(datasets):
    choices = []
    paths = []
    for ds in datasets:
        paths.append(get_path(datasets, ds))
        name = paths[-1]
        if name == "":
            name = "/"
        choices.append((ds['_id'], name))
    return choices


if __name__ == "__main__":
    app.run(port=5000, debug=True)
