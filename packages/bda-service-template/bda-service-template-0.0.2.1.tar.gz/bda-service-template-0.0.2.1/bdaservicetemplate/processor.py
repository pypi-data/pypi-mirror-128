from .service import Service
from abc import ABC, abstractclassmethod
import pandas as pd


class Processor(ABC, Service):
    def __init__(self):
        super().__init__()

    @Service.dataset_to_dataset
    @abstractclassmethod
    def process(self, dataset) -> pd.DataFrame:
        pass
