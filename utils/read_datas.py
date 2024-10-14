import yaml

class ReadDatas:
    def __init__(self) -> None:
        pass

    def read_yaml(self, path, encoding="utf-8"):
        with open(path, "r", encoding=encoding) as datas:
            data = yaml.safe_load(datas)
        return data