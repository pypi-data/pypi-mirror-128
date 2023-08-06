# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sensor_position_dataset_helper']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'c3d>=0.3.0,<0.4.0',
 'imucal>=2.0.0,<3.0.0',
 'joblib>=1.0.0,<2.0.0',
 'nilspodlib>=3.1,<4.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.2,<2.0.0',
 'scipy>=1,<2',
 'tpcp>=0.3.0,<0.4.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'sensor-position-dataset-helper',
    'version': '1.0.0',
    'description': 'A helper for the SensorPositionDateset (recorded 2019, published 2021)',
    'long_description': '# SensorPositionComparison Helper\n\nThis is a helper module to extract and handle the data of the [SensorPositionComparison Dataset](TODO: Add updated link).\n\nIf you use the dataset and this module, please cite:\nTODO: Add citation once published\n\n## Installation and Usage\n\nInstall the project via `pip` or `poetry`:\n\n```\npip install sensor_position_dataset_helper\n```\n\n## Dataset Handling\nYou also need to download the actual Dataset from [here](TODO: Add updated link).\nIf you are member of the matlab, you can also get a git-lfs version from \n[our internal server](https://mad-srv.informatik.uni-erlangen.de/MadLab/data/sensorpositoncomparison).\n\nThen you need to tell this library about the position of the dataset.\nNote that the path should point to the top-level repo folder of the dataset.\n\n```python\nfrom sensor_position_dataset_helper import set_data_folder\n\nset_data_folder("PATH/TO/THE_DATASET")\n```\n\nYou can also overwrite this pass on a per-function basis:\n\n```python\nfrom sensor_position_dataset_helper import get_all_subjects\n\nget_all_subjects(data_folder="PATH/TO/THE_DATASET")\n```\n\nIf you are using the tpcp-dataset objects, you need to provide the path in the init.\n\n```python\nfrom sensor_position_dataset_helper.tpcp_dataset import SensorPositionDatasetSegmentation\n\ndataset = SensorPositionDatasetSegmentation(dataset_path="PATH/TO/THE_DATASET")\n```\n\n## Managing Dataset Revisions\n\nTo ensure reproducibility, you should save the version of the dataset that was used for a certain analysis.\nThis can be easily done by placing the following line at the top of your script:\n\nTODO: Add information for non git versions of the dataset\n```python\nfrom sensor_position_dataset_helper import ensure_git_revision\n\nensure_git_revision(data_folder="PATH/TO/THE_DATASET", version="EXPECTED GIT HASH")\n```\n\nThis will produce an error, if the dataset version you are using is not the one you expect, or if the dataset repo has \nuncommitted changes.\nThis will prevent bugs, because you accidentally use the wrong dataset version and will directly document the correct \nversion.\n',
    'author': 'Arne Küderle',
    'author_email': 'arne.kuederle@fau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mad-lab-fau/sensor_position_dataset_helper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<3.9',
}


setup(**setup_kwargs)
