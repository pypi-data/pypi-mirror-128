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

import ibm_boto3
from ibm_watson_machine_learning.experiment import AutoAI
from ibm_watson_machine_learning.helpers.connections import DataConnection, ContainerLocation
from ibm_watson_machine_learning.tests.utils import is_cp4d, save_data_to_container
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import AbstractTestWebservice, \
    AbstractTestAutoAIAsync, AbstractTestBatch

from ibm_watson_machine_learning.utils.autoai.enums import PredictionType, Metrics, ClassificationAlgorithms


class TestAutoAIRemote(AbstractTestAutoAIAsync, AbstractTestWebservice, AbstractTestBatch, unittest.TestCase):
    """
    The test can be run on CLOUD, and CPD
    """

    cos_resource = None
    data_location = './autoai/data/Corona_NLP_test_utf8.csv'

    data_cos_path = 'data/Corona_NLP_test_utf8.csv'

    SPACE_ONLY = False

    OPTIMIZER_NAME = "Corona NLP Text Transformer test sdk"

    batch_payload_location = './autoai/data/Corona_NLP_scoring_payload.csv'
    batch_payload_cos_location = "Corona_NLP_scoring_payload.csv"

    BATCH_DEPLOYMENT_WITH_CA = True
    BATCH_DEPLOYMENT_WITH_CDA = False
    BATCH_DEPLOYMENT_WITH_DA = False
    BATCH_DEPLOYMENT_WITH_DF = True

    target_space_id = None

    experiment_info = dict(
        name=OPTIMIZER_NAME,
        prediction_type=PredictionType.MULTICLASS,
        prediction_column='Sentiment',
        scoring=Metrics.F1_SCORE_MACRO,
        holdout_size=0.1,
        text_processing=True,
        text_columns_names=['OriginalTweet', 'Location'],
        word2vec_feature_number=4,
        max_number_of_estimators=1,
        daub_give_priority_to_runtime=3.0,
    )

    def test_00b_write_data_to_container(self):
        if self.SPACE_ONLY:
            self.wml_client.set.default_space(self.space_id)
        else:
            self.wml_client.set.default_project(self.project_id)

        save_data_to_container(self.data_location, self.data_cos_path, self.wml_client)

    def test_02_data_reference_setup(self):
        TestAutoAIRemote.data_connection = DataConnection(
            location=ContainerLocation(path=self.data_cos_path
                                       ))
        TestAutoAIRemote.results_connection = None

        self.assertIsNotNone(obj=TestAutoAIRemote.data_connection)

    def test_08_get_run_details(self):
        parameters = self.remote_auto_pipelines.get_run_details()
        print(parameters)
        self.assertIsNotNone(parameters)

    def test_08a_get_feature_importance(self):
        feature_importance_df = self.remote_auto_pipelines.get_pipeline_details(pipeline_name='Pipeline_1').get('features_importance')
        self.assertIsNotNone(feature_importance_df)

        str_feature_importance_index_list = str(list(feature_importance_df.sort_index().index))

        text_columns = self.experiment_info['text_columns_names']

        for column in text_columns:
            self.assertIn(f'word2vec({column})', str_feature_importance_index_list,
                          msg=f"word2vec({column}) is not in features importance table. Full table: {feature_importance_df}")

        self.assertIn('NewTextFeature_0', str_feature_importance_index_list,
                      msg="Text features were numerated incorrectly.")
        self.assertIn(f"NewTextFeature_{self.experiment_info['word2vec_feature_number']*len(text_columns)-1}",
                      str_feature_importance_index_list, msg="Text features were numerated incorrectly.")


if __name__ == '__main__':
    unittest.main()
