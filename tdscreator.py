from flask import Flask, redirect, render_template, url_for, request
import json

import datasets as ds

from forms import CreateDatasetForm, CreateFeatureCollectionForm

app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVyGODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'

#
# Home route
#
@app.route('/')
def home():
    return render_template('index.html')


#
# Dataset routes
#
@app.route('/datasets')
def dataset_view():
    datasets = ds.read_datasets()
    return render_template('viewdatasets.html', datasets=datasets)


@app.route('/datasets/createdataset', methods=['GET','POST'])
def dataset_createdataset():
    form = CreateDatasetForm(request.form)
    # Populate the possible routes for the datasets
    datasets = ds.read_datasets()
    form.path.choices = populate_choices(datasets)

    # If a valid form is submitted, create the dataset and add it
    if request.method=='POST':# and form.validate():
        # Grab info from the form
        name = form.name.data
        path = form.path.data
        metadata = form.metadata.data

        # Create new dataset dictionary and add it to the json file
        new_dataset = {"name":name, "parent_dataset":path, "metadata":metadata, "feature_collections":[]}
        ds.add_dataset(new_dataset)

        # After sucessful dataset creation, redirect to the dataset view page
        return redirect(url_for('dataset_view'))
    # Render the page
    return render_template('createdataset.html', createdatasetform=form)


@app.route('/datasets/editdataset', methods=['GET','POST'])
def dataset_editdataset():
    form = CreateDatasetForm(request.form)
    # Populate the possible routes for the datasets
    datasets = ds.read_datasets()
    form.path.choices = populate_choices(datasets)

    # If a valid form is submitted, create the dataset and add it
    if request.method=='POST':# and form.validate():
        if request.form['submit'] == 'Save':
            # Grab info from the form
            name = form.name.data
            path = form.path.data
            metadata = form.metadata.data
            old_dataset_id = form.id.data

            # Create new dataset dictionary and add it to the json file
            new_dataset = {"name":name, "parent_dataset":path, "metadata":metadata, "feature_collections":[]}
            ds.edit_dataset(old_dataset_id, new_dataset)
        if request.form['submit'] == 'Delete':
            ds.delete_dataset(form.id.data)

        # After sucessful dataset creation, redirect to the dataset view page
        return redirect(url_for('dataset_view'))

    # Otherwise, pre-populate the form with data on the dataset
    else:
        # Create the form and select the parent dataset of the dataset we
        # are editing
        dataset_id = request.args.get('_id')
        dataset = ds.get_dataset_by_id(dataset_id)
        form = CreateDatasetForm(request.form, path=dataset['parent_dataset'])

        # Populate the possible routes for the datasets
        datasets = ds.read_datasets()
        choices = populate_choices(datasets)
        form.path.choices = choices

        # Get the dataset and pre-populate the form
        print("Getting dataset id: ", dataset_id)
        dataset = ds.get_dataset_by_id(dataset_id)

        form.name.data = dataset['name']
        form.metadata.data = dataset['metadata']
        form.id.data = dataset['_id']

    # Render the page
    return render_template('editdataset.html', createdatasetform=form, dataset=dataset)


@app.route('/datasets/deletedataset')
def dataset_deletedataset():
    dataset_name = request.args.get("dataset_id")
    ds.deletedataset(dataset_id)
    return redirect(url_for('dataset_view'))









#
# Feature Collection routes
#

@app.route('/featurecollections')
def featurecollections_view():
    return render_template('notready.html')
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


#
# My Servers
#

@app.route('/servers')
def servers():
    return render_template('notready.html')

#
# Helpers
#




def get_path(datasets, dataset):
    path = []
    dst = dataset
    while dst['parent_dataset'] != "None":
        path.append(dst['name'])
        dst = ds.get_dataset_by_id(dst['parent_dataset'])
    path_str = ""
    for item in path[::-1]:
        path_str += "/" + item
    return path_str

def populate_choices(datasets):
    choices = []
    paths = []
    for dst in datasets:
        paths.append(get_path(datasets, dst))
        name = paths[-1]
        if name == "":
            name = "/"
        choices.append((dst['_id'], name))
    return choices


if __name__ == "__main__":
    app.run(port=5000, debug=True)
