import yaml


def load_test_data(path):
    with open(path, "r") as file:
        data = yaml.safe_load(file)
    return data
