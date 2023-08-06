""" This module implement data functionality  """
import re
from typing import List
from typing import Optional

from superwise.controller.base import BaseController
from superwise.controller.exceptions import SuperwiseValidationException
from superwise.models.task import Task


class TransactionController(BaseController):
    """Transaction Controller is in-charge for create transaction using file and batch request """

    def __init__(self, client, sw):
        """
        constructer for DataController class

        :param client:

        """
        super().__init__(client, sw)
        self.path = "gateway/v1/transaction"
        self.model_name = None

    def log_batch(self, task_id: str, records: List[dict], version_id: Optional[str] = None):
        """
        stream data of a given file path

        :param
        - task_id: string - model which the data associated to him.
        - version_id: string - version of the model -   Optional
        - records: List[dict] - list of records of data,  each record is a dict.
        :return transaction_id
        """
        self.logger.info("transaction batch")
        payload = dict(records=records, task_id=task_id)
        if version_id is not None:
            payload["version_id"] = version_id
        r = self.client.post(self.build_url("{}".format(self.path + "/batch")), payload)
        self.logger.info("file_log server response: {}".format(r.content))
        if r.status_code == 201:
            return r.json()
        else:
            raise Exception("send records to superwise failed, server error")

    def log_file(self, file_path):
        """
        stream data of a given file path
        :param file_path: url for file stored in cloud str
        :return transaction_id
        """
        self.logger.info("transaction file %s ", file_path)
        pattern = "(s3|gs)://.+"
        if not re.match(pattern, file_path):
            raise SuperwiseValidationException(
                "transaction file failed because of wrong file path. file path should be gcs or s3 path."
            )
        params = {"file": file_path}
        r = self.client.post(url=self.build_url("{}".format(self.path + "/file")), params=params)
        self.logger.info("transaction file server response: {}".format(r.content))
        if r.status_code == 201:
            return r.json()
        else:
            raise Exception("send file to superwise failed, server error")
