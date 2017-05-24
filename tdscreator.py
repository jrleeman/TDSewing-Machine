"""Main TDSewing Machine App."""

from flask import Flask, redirect, render_template, request, url_for


app = Flask(__name__)
app.secret_key = 'NTOBiFxcjaehKa9nvgTmv5dslPUay7l4QDauEGIV3pSwpZKhpFGqJzestVy\
                  GODNT7BL8mauL38xyzgukYV3cIMix9eO8Jgb3bhvo'

#
# Home route
#


@app.route('/')
def home():
    """Home page."""
    return render_template('index.html')


#
# Dataset routes
#

def find_child_datasets(root):
    ns = {'tdscat': 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'}
    return root.findall('./tdscat:dataset', ns)


def find_child_dataset_scans(root):
    ns = {'tdscat': 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'}
    return root.findall('./tdscat:datasetScan', ns)


def find_child_feature_collections(root):
    ns = {'tdscat': 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'}
    return root.findall('./tdscat:featureCollection', ns)


def make_tree(root, tree={}):
    ns = {'tdscat': 'http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0'}
    for dataset in root.findall('./tdscat:dataset', ns):
        child_datasets = find_child_datasets(dataset)
        local = {}
        for child in child_datasets:
            local[child.attrib['name']] = make_tree(dataset, tree={})

        for child in find_child_feature_collections(dataset):
            local[child.attrib['name']] = {}

        for child in find_child_dataset_scans(dataset):
            local[child.attrib['name']] = {}

        tree[dataset.attrib['name']] = local
    return tree

@app.route('/datasets')
def dataset_view():
    """Show datasets."""
    import xml.etree.ElementTree as ET

    # Read the tree and send to template as a dict of dicts

    xml_files = {'Forecast Model Data': 'forecastModels.xml',
                 'Forecast Products and Analyses': 'forecastProdsAndAna.xml',
                 'Observation Data': 'obsData.xml',
                 'Radar Data': 'radars.xml',
                 'Satellite Data': 'satellite.xml'}

    datasets = {}

    for key in xml_files:
        name = key
        file = xml_files[key]
        tree = ET.parse(file)
        root = tree.getroot()
        datasets[name] = make_tree(root, {})


    print(datasets.keys())
    #print(datasets)
    return render_template('viewdatasets.html', datasets=datasets)


#
# My Servers
#


@app.route('/servers')
def servers():
    """View servers in user's account."""
    return render_template('notready.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
