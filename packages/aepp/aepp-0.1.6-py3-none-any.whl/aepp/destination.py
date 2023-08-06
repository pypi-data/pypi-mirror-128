# Internal Library
import aepp
from aepp import connector
from aepp import config
from copy import deepcopy
from typing import Union
import time
import logging

class Authoring:
    """
    This class is referring to Destination Authoring capability for AEP. 
    It is a suite of configuration APIs that allow you to configure destination integration patterns for Experience Platform to deliver audience and profile data to your endpoint, based on data and authentication formats of your choice.
    """

    def __init__(self, 
        config_object: dict = aepp.config.config_object,
        header: dict = aepp.config.header,
        loggingObject: dict = None,
        **kwargs,):
        """
        Instanciating the class for Authoring.

        Arguments:
            loggingObject : OPTIONAL : logging object to log messages.
            config_object : OPTIONAL : config object in the config module.
            header : OPTIONAL : header object  in the config module.
        possible kwargs:
        """
        if loggingObject is not None and sorted(
            ["level", "stream", "format", "filename", "file"]
        ) == sorted(list(loggingObject.keys())):
            self.loggingEnabled = True
            self.logger = logging.getLogger(f"{__name__}")
            self.logger.setLevel(loggingObject["level"])
            formatter = logging.Formatter(loggingObject["format"])
            if loggingObject["file"]:
                fileHandler = logging.FileHandler(loggingObject["filename"])
                fileHandler.setFormatter(formatter)
                self.logger.addHandler(fileHandler)
            if loggingObject["stream"]:
                streamHandler = logging.StreamHandler()
                streamHandler.setFormatter(formatter)
                self.logger.addHandler(streamHandler)
        self.connector = connector.AdobeRequest(
            config_object=config_object,
            header=header,
            loggingEnabled=self.loggingEnabled,
            logger=self.logger,
        )
        self.header = self.connector.header
        # self.header.update({"Accept": "application/json"})
        self.header.update(**kwargs)
        self.sandbox = self.connector.config["sandbox"]
        self.endpoint = config.endpoints["global"] + config.endpoints["destinationAuthoring"]