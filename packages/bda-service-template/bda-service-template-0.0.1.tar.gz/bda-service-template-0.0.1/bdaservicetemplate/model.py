from .service import Service
from abc import ABC, abstractclassmethod
import pandas as pd


class Model(ABC, Service):
    def __init__(self):
        super().__init__()

    @Service.dataset_to_model
    @abstractclassmethod
    def fit(self, dataset) -> str:
        pass

    @Service.dataset_and_model_to_dataset
    @abstractclassmethod
    def predict(self, dataset, model_path) -> pd.DataFrame:
        pass
