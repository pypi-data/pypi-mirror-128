import yaml

from miniscule.base import ConfigLoader, read_config
from miniscule.logs import set_up_logging
from miniscule.hooks import set_except_hook


def _read_logging_config(path: str):
    with open(path, "r") as stream:
        return yaml.safe_load(stream.read())


def init(path=None, key="log_config", Loader=ConfigLoader, **kwargs):
    """Read configuration from a file, initialize logging and embed the logging
    configuration under ``key``.

    :param path: Path of the file from which to read the configuration.  If
        None, the path is read from the value of the ``CONFIG`` environment
        variable.  If no such variable, path defaults to ``config.yaml``.
    :param key: The key under which to find the path to the logging
        configuration.
    :param Loader: See :func:`miniscule.load_config`.
    :param kwargs: Passed directly to :func:`miniscule.logs.init_logging`.

    :returns: See :func:`miniscule.load_config`.
    """
    config = read_config(path, Loader)
    if "logging" not in config and config.get(key):
        config["logging"] = _read_logging_config(config.pop(key))
    if "logging" in config:
        set_up_logging(config["logging"], **kwargs)
    set_except_hook()
    return config
