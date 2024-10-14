import yaml

def read_test_datas(title, encoding="utf-8"):
    with open(f".\config\{title}.yaml", "r", encoding=encoding) as datas:
        data = yaml.safe_load(datas)
    return data