from setuptools import setup
from setuptools import find_packages

setup(
    name = 'Dendrite Neural Networks',
    version = '0.0.1',
    description = 'Probando...',
    py_modules = ["DMN","DEN","DSN","PreTrain.HpC.HBpC","PreTrain.HpC.HEpC","PreTrain.HpC.HSpC", "PreTrain.kmeans.bkmeans","PreTrain.kmeans.ekmeans","PreTrain.kmeans.skmeans"],
    packages = find_packages(),
    package_dir = {'':'src'}

)