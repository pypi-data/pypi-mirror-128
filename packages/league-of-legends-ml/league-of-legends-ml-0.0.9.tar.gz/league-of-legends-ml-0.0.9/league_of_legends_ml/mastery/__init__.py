import importlib.resources as pkg_resources
from ..common import modes, CLASSIC
from . import files
import pickle
import numpy

__models = {}
__scalers = {}


def __get_model(mode: str = CLASSIC):
    mode = mode.lower()
    if mode not in modes:
        raise ValueError('Undefined mode for model')
    with pkg_resources.open_binary(files, f'{mode}_ensemble_model.pkl') as file:
        model = pickle.load(file)
    with pkg_resources.open_binary(files, f'{mode}_ensemble_scaler.pkl') as file:
        scaler = pickle.load(file)
    return model, scaler


def predict(duration_seconds: int, victory: bool, mode: str = CLASSIC) -> int:
    mode = mode.lower()
    if mode not in __models or mode not in __scalers:
        __models[mode], __scalers[mode] = __get_model(mode)
    model, scaler = __models[mode], __scalers[mode]
    data = numpy.array([[duration_seconds, int(victory)]])
    scaled_data = scaler.transform(data)
    result = model.predict(scaled_data)
    return round(result[0])
