import hashlib
import json


def read_datasets(fname='datasets.json'):
    """Read the datasets json file and return a list of dictionaries."""
    jsondata = open(fname, 'r').read()
    ret = json.loads(jsondata)
    return ret


def _write_datasets(datasets, fname='datasets.json'):
    """Write out a list of dictionaries to the datasets json file."""
    with open(fname, 'w') as outfile:
        json.dump(datasets, outfile)


def _rebuild_children_parent_id(old_parent_dataset_id, new_parent_dataset_id):
    """If any datasets have this parent, update their parent hash"""
    datasets = read_datasets()
    for ds in datasets:
        if ds['parent_dataset'] == old_parent_dataset_id:
            ds['parent_dataset'] = new_parent_dataset_id
    _write_datasets(datasets)


def _create_dataset_id(dataset):
    """Create a unique dataset id by hashing the dataset minus the id."""
    dataset.pop('_id', None)
    dataset_id = hashlib.sha1(json.dumps(dataset, sort_keys=True).encode('utf-8')).hexdigest()
    dataset['_id'] = dataset_id
    return dataset


def add_dataset(dataset):
    """Add a new dataset"""
    datasets = read_datasets()
    dataset = _create_dataset_id(dataset)
    datasets.append(dataset)
    _write_datasets(datasets)
    return dataset['_id']


def delete_dataset(dataset_id, delete_below=True):
    """Delete a dataset and by default all datasets below that dataset."""
    datasets = read_datasets()
    for i, dataset in enumerate(datasets):
        if dataset['_id'] == dataset_id:
            del datasets[i]
            break

    # Check for datasets below this dataset and delete them as well
    if delete_below:
        pass

    _write_datasets(datasets)

def edit_dataset(dataset_id, dataset):
    """Given the old dataset id and new data, update the record and children"""
    old_dataset_id = dataset_id
    delete_dataset(dataset_id)
    new_dataset_id = add_dataset(dataset)
    print("EDITING : ", old_dataset_id, new_dataset_id)
    _rebuild_children_parent_id(old_dataset_id, new_dataset_id)


def get_dataset_by_id(id):
    """Return a dataset with the given ID"""
    datasets = read_datasets()
    for dataset in datasets:
        if dataset['_id'] == id:
            return dataset
