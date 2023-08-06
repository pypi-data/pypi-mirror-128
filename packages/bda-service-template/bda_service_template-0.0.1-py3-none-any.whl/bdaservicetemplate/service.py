import pandas as pd
import os
from fileioutilities.file_io import FileIO
from bdaserviceutils import get_args, TaskStatus
from pysparkutilities.spark_initializer import spark_initializer
from pysparkutilities import ds_initializer



class Service():
    def __init__(self):
        super().__init__()

        self.args = get_args()
        print(self.args)
        self.spark = spark_initializer("Test-model", self.args)

    def download_model(self, path):
        fileIO = FileIO(storage_type=self.args['dataStorageType-input-model'])
        fileIO.download(remote_path=get_args()['input-model'], local_path=path)

    def get_dataset(self):
        self.data = ds_initializer.load_dataset(sc=self.spark, read_all=False).na.drop()
        return self.data.toPandas()

    def save_dataset(self, dataset):
        df = self.spark.createDataFrame(dataset)
        ds_initializer.save_dataset(df=df, output_dest=self.args['output-dataset'])

    def upload_model(self, path):
        fileIO = FileIO() #storage_type=self.args['dataStorageType-output-model'])
        fileIO.upload(local_path=path, remote_path=self.args['output-model'])

    def get_model_path(self):
        pass


    @staticmethod
    def dataset_to_dataset(func):
        
        def wrapper(*args):
            self = args[0]
            dataset = self.get_dataset()
            resulting_dataset = func(self, dataset)
            self.save_dataset(resulting_dataset)

        return wrapper


    @staticmethod
    def dataset_to_model(func):
        
        def wrapper(*args):
            self = args[0]
            dataset = self.get_dataset()
            model_path = func(self, dataset)
            self.upload_model(model_path)

        return wrapper


    @staticmethod
    def dataset_and_model_to_dataset(func):
        
        def wrapper(*args):
            self = args[0]
            dataset = self.get_dataset()
            model_path = os.path.join(".", "model")
            self.download_model(path=model_path)
            resulting_dataset = func(self, dataset, model_path)
            self.save_dataset(resulting_dataset)

        return wrapper

