#!/usr/bin/env python
# -*- coding utf-8 -*-

import _io
import os
import json
import requests
import urllib.parse
import zipfile
import tempfile
import shutil
import mlflow

###########################################

MODEL_ZIP_NAME = 'model.zip'

routes = {
    'build': '/build',
    'job': '/job',
}

###########################################

class CustomModel(mlflow.pyfunc.PythonModel):
    """The Chassis CustomModel object.

    This class inherits from mlflow.pyfunc.PythonModel and adds Chassis functionality.

    Attributes:
        model_context (dict): Should contain all necessary objects to be used across
            inferences in all user-provided functions (model, human-readable labels, etc...).
        process_fn (function): User-provided function responsible for running inference. 
            Takes two arguments, model_input and model_context. If preprocess_fn provided, process_fn 
            must be able to directly accept output of preprocess_fn as model_input. Otherwise, 
            process_fn must handle bytes provided as the model_input. If postprocess_fn provided, 
            process_fn output must be compatible with postprocess_fn input. Otherwise, process_fn is 
            responsible for producing final formatted model output. 
        preprocess_fn (function, optional): Optional user-provided preprocessing function. Takes two 
            arguments, model_input and model_context. model_input will contain bytes.
        postprocess_fn (function, optional): Optional user-provided postprocesing function. Takes two 
            arguments, output and model_context. Output will contain output of proceess_fn. Must 
            return final output.
    """

    def __init__(self,model_context,process_fn,preprocess_fn=None,postprocess_fn=None):
        def predict(context,model_input):
            if preprocess_fn:
                model_input = preprocess_fn(model_input,model_context)
            output = process_fn(model_input,model_context)
            if postprocess_fn:
                output = postprocess_fn(output,model_context)   
            return output
        self.predict = predict

    def test(self,test_input):
        if isinstance(test_input,_io.BufferedReader):
            return self.predict(None,test_input.read())
        elif isinstance(test_input,bytes):
            return self.predict(None,test_input)
        elif isinstance(test_input,str):
            if os.path.exists(test_input):
                return self.predict(None,open(test_input,'rb').read())
            else:
                return self.predict(None,bytes(test_input,encoding='utf8'))
        else:
            print("Invalid input. Must be buffered reader, bytes, valid filepath, or text input.")
            return False

    def save(self,path,conda_env=None,overwrite=False):
        if overwrite and os.path.exists(path):
            shutil.rmtree(path)
        mlflow.pyfunc.save_model(path=path, python_model=self, conda_env=conda_env)
        print("Chassis model saved.")


class ChassisML:
    """The ChassisML object.

    This class is used to interact with the Kaniko service.

    Attributes:
        base_url (str): The base url for the API.
        tar_path (str): The path to the generated tar in the Kaniko service.
        model_data (json): Object that contains all the container data.
    """

    def __init__(self):
        self.base_url = 'http://localhost:5000'

    def _zipdir(self, model_directory):
        tmppath = tempfile.mkdtemp()

        # Compress all files in model directory to send them as a zip.
        with zipfile.ZipFile(f'{tmppath}/{MODEL_ZIP_NAME}', 'w', zipfile.ZIP_DEFLATED) as ziph:
            for root, dirs, files in os.walk(model_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    ziph.write(file_path, file_path[len(model_directory):])

        return tmppath

    def _add_mody_files_to_request(self, files, modzy_data):
        for key, file_key in [('metadata_path', 'modzy_metadata_data'),
                              ('sample_input_path', 'modzy_sample_input_data')]:
            value = modzy_data.get(key)

            if value:
                files.append((file_key, open(value, 'rb')))

    def publish(self, image_data, modzy_data, base_url):
        self.base_url = base_url if base_url else self.base_url

        tmp_zip_dir = self._zipdir(image_data.get('model_path'))

        files = [
            ('image_data', json.dumps(image_data)),
            ('modzy_data', json.dumps(modzy_data or {})),
            ('model', open(f'{tmp_zip_dir}/{MODEL_ZIP_NAME}', 'rb')),
        ]

        if modzy_data:
            self._add_mody_files_to_request(files, modzy_data)

        route = urllib.parse.urljoin(self.base_url, routes['build'])

        print('Building image... ', end='', flush=True)
        res = requests.post(route, files=files)
        res.raise_for_status()
        print('Ok!')

        # Remove the zip since it's no longer needed.
        shutil.rmtree(tmp_zip_dir)

        return res.json()

    def get_job_status(self, job_id):
        route = f'{urllib.parse.urljoin(self.base_url, routes["job"])}/{job_id}'

        res = requests.get(route)

        data = res.json()

        return data

    def download_tar(self, job_id, output_filename):
        url = f'{urllib.parse.urljoin(self.base_url, routes["job"])}/{job_id}/download-tar'
        r = requests.get(url)

        if r.status_code == 200:
            with open(output_filename, 'wb') as f:
                f.write(r.content)
        else:
            print(f'Error download tar: {r.text}')

###########################################

# ChassisML instance that is used in the SDK.
_defaultChassisML = ChassisML()

###########################################

def publish(image_data, modzy_data=None, base_url=None):
    """Makes a request agains Chassis service to build the image.

    Example of image_data:
    ```
    {
        'name': '<username>/chassisml-sklearn-demo:latest',
        'model_name': 'digits',
        'model_path': './mlflow_custom_pyfunc_svm',
        'registry_auth': 'base64(<username>:<password>)',
        'publish': False
    }
    ```

    Example of modzy_data:
    ```
    {
        'metadata_path': './modzy/model.yaml'
        'sample_input_path': './modzy/sample_input.json',
        'deploy': False,
        'api_key': 'XxXxXxXx:XxXxXxXx',
    }
    ```

    Args:
        image_data (json): Required data to build and deploy the model.
        modzy_data (json): In case we need to deploy the image to Modzy.
        base_url (str): Default base_url is localhost:5000.
    """
    return _defaultChassisML.publish(image_data, modzy_data, base_url)

def get_job_status(job_id):
    """Returns the data once the model has been deployed.
    """
    return _defaultChassisML.get_job_status(job_id)

def download_tar(job_id, output_filename):
    """Returns the data once the model has been deployed.
    """
    return _defaultChassisML.download_tar(job_id, output_filename)

def create_model(context,process_fn,preprocess_fn=None,postprocess_fn=None):
    """Returns an initialized CustomModel customized with user-provided functions.
    """
    return CustomModel(context,process_fn,preprocess_fn,postprocess_fn)

def load_model(model_path):
    """Returns mlflow.pyfunc.PyFuncModel loaded from model_path.
    """
    return mlflow.pyfunc.load_model(model_path)