from jujubigdata.utils import DistConfig
from charms.layer import LayerOptions


def get_dist_config():
    return DistConfig(data=LayerOptions('hadoop-client'))
