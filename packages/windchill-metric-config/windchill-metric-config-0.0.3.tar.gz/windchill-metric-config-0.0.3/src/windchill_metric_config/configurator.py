from json import dumps, loads

from ruamel.yaml import YAML, scalarstring, CommentedMap

from windchill_metric_config.description import Description
from windchill_metric_config.system.system import SystemMetrics
from windchill_metric_config.windchill.windchill import WindchillMetrics


class Metrics:
    comment_indent = 80

    def __init__(self):
        self.system = SystemMetrics()
        self.windchill = WindchillMetrics()

    def __str__(self):
        return dumps(self.as_dict())

    def as_dict(self):
        return {
            'system': self.system.as_dict(),
            'windchill': self.windchill.as_dict()
        }

    def as_yaml_dict(self):
        return {
            'system': self.system.as_yaml_dict(),
            'windchill': self.windchill.as_yaml_dict()
        }

    def save_as_yaml(self, config_yaml: str):
        yaml = YAML()
        data = loads(dumps(self.as_yaml_dict()), object_pairs_hook=CommentedMap)
        scalarstring.walk_tree(data)
        self.windchill.generate_yaml(data['windchill'], self.comment_indent)
        self.system.generate_yaml(data['system'], self.comment_indent)
        with open(config_yaml, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)

    def load_config(self, config_yaml: str):
        yaml = YAML()
        with open(config_yaml, 'r', encoding='utf-8') as f:
            data = yaml.load(f)
        for key in self.__dict__.keys():
            if key in data:
                if key == 'system':
                    self.__getattribute__(key).set_config(data[key])

    def metrics_as_list(self):
        metric_list = []
        for item in self.__dict__.keys():
            child = self.__getattribute__(item)
            if type(child) == Description:
                metric_list.append(child.id)
            else:
                child.metrics_as_list(metric_list)

        return metric_list
