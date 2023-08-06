#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest
import json
from configparser import ConfigParser

from ibm_watson_machine_learning.experiment.autoai.optimizers import RemoteAutoPipelines
from ibm_watson_machine_learning.helpers.connections import DataConnection, DatabaseLocation
from ibm_watson_machine_learning.tests.utils import is_cp4d, get_env
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import (
    AbstractTestAutoAIRemote)

from ibm_watson_machine_learning.wml_client_error import WMLClientError

configDir = "./config.ini"

config = ConfigParser()
config.read(configDir)


@unittest.skip("Skip due to issue 25182")
@unittest.skipIf(not is_cp4d(), "JDBC is not tested on cloud yet.")
class TestAutoAIRemote(AbstractTestAutoAIRemote, unittest.TestCase):
    """
    The test can be run on CPD
    The test covers:
    - JDBC DB2 connection set-up
    - downloading training data from connection
    - downloading all generated pipelines to lale pipeline
    - deployment with lale pipeline
    - deployment deletion
    Connection used in test:
     - input: Database connection pointing to DB2.
     - output: null
    """
    prediction_column = 'SPECIES'
    connection_asset_details = json.loads(config.get(get_env(), 'jdbc_db2_connection_asset_details'))

    def test_00c_prepare_connection_to_db2(self):
        # import urllib
        # import requests
        #
        # driver_file_path = self.connection_asset_details['driver_file_path']
        # driver_file_name = driver_file_path.split('/')[-1]
        #
        # signed_url = self.wml_client.service_instance._href_definitions.get_wsd_model_attachment_href() + '/' + \
        #                              urllib.parse.quote("dbdrivers/" + driver_file_name + "/sign", safe='')
        # params = self.wml_client._params()
        #
        # params['expires_in'] = 60*60*24
        #
        # response = requests.post(
        #     signed_url,
        #     headers=self.wml_client._get_headers(no_content_type=True),
        #     params=params,
        #     verify=False
        # )
        #
        # print(response.json())


        # with open(driver_file_path, 'rb') as fdata:
        #     content_upload_url = self.wml_client.service_instance._href_definitions.get_wsd_model_attachment_href() + '/' + \
        #                          urllib.parse.quote("dbdrivers/" + driver_file_name, safe='')
        #     response = requests.put(
        #         content_upload_url,
        #         files={'file': ('native', fdata, 'application/octet-stream', {'Expires': '0'})},
        #         headers=self.wml_client._get_headers(no_content_type=True),
        #         params=self.wml_client._params(),
        #         verify=False
        #     )
        #     if response.status_code == 201:
        #         print(response.text)
        #         # asset_body = {
        #         #     "asset_type": "wml_model",
        #         #     "name": "native",
        #         #     "object_key": asset_uid + "/" + file_name_to_attach,
        #         #     "object_key_is_read_only": True
        #         # }
        #         # attach_payload = json.dumps(asset_body, separators=(',', ':'))
        #         #
        #         # attach_response = requests.post(attach_url,
        #         #                                 data=attach_payload,
        #         #                                 params=params,
        #         #                                 headers=headers,
        #         #                                 verify=False)
        #     else:
        #         print(response.text)
        #         raise Exception(f"Failed while uploading driver: {response.text}")

        connection_details = self.wml_client.connections.create({
            'datasource_type': self.wml_client.connections.get_datasource_type_uid_by_name(
                self.connection_asset_details['datasource_type_name']
            ),
            'name': 'Connection to DB2 for tests',
            'properties': self.connection_asset_details['properties']
        })

        TestAutoAIRemote.connection_id = self.wml_client.connections.get_uid(connection_details)
        self.assertIsInstance(self.connection_id, str)

    def test_00d_prepare_connected_data_asset(self):
        asset_details = self.wml_client.data_assets.store({
            self.wml_client.data_assets.ConfigurationMetaNames.CONNECTION_ID: self.connection_id,
            self.wml_client.data_assets.ConfigurationMetaNames.NAME: "Iris - training asset",
            self.wml_client.data_assets.ConfigurationMetaNames.DATA_CONTENT_NAME: f"/{self.connection_asset_details['schema_name']}/{self.connection_asset_details['table_name']}",
            "connectionPath": f"/{self.connection_asset_details['schema_name']}/{self.connection_asset_details['table_name']}"
        })

        print(asset_details)

        TestAutoAIRemote.asset_id = self.wml_client.data_assets.get_id(asset_details)
        self.assertIsInstance(self.asset_id, str)

    def test_02_DataConnection_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(data_asset_id=self.asset_id)

        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)
        # self.assertIsNotNone(obj=TestAutoAIRemote.results_connection)

    def test_02a_read_saved_remote_data_before_fit(self):
        TestAutoAIRemote.data = self.data_connection.read()
        print("Data sample:")
        print(self.data.head())
        self.assertGreater(len(self.data), 0)

    def test_03_initialize_optimizer(self):
        AbstractTestAutoAIRemote.remote_auto_pipelines = self.experiment.optimizer(
            name='Iris - AutoAI',
            prediction_type=self.experiment.PredictionType.MULTICLASS,
            prediction_column=self.prediction_column,
            scoring=self.experiment.Metrics.ACCURACY_SCORE,
            drop_duplicates=False,
            enable_all_data_sources=True,

        )

        self.assertIsInstance(self.remote_auto_pipelines, RemoteAutoPipelines,
                              msg="experiment.optimizer did not return RemoteAutoPipelines object")

    def test_29_delete_connection_and_connected_data_asset(self):
        self.wml_client.data_assets.delete(self.asset_id)
        self.wml_client.connections.delete(self.connection_id)

        with self.assertRaises(WMLClientError):
            self.wml_client.connections.get_details(self.connection_id)


if __name__ == '__main__':
    unittest.main()
