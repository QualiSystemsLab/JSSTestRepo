import logging
import requests
import json
import time
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue
from robot.api import logger
from uuid import UUID


class CloudShellAPILibrary(object):
    def __init__(self, cloudshell_address, user="admin", auth_token='', domain="Global", sandbox_uuid=""):
        self.api_session = CloudShellAPISession(cloudshell_address, user, token_id=auth_token, domain=domain)
        if sandbox_uuid:
            self.sandbox_id = str(sandbox_uuid)

    def write_sandbox_message(self, message):
        self.api_session.WriteMessageToReservationOutput(self.sandbox_id, message)

    def execute_command(self, resource, resource_type, command_name, command_params: dict):
        if command_params:
            api_params = [InputNameValue(param.name, param.value) for param in command_params.items()]
            output = self.api_session.ExecuteCommand(self.sandbox_id, resource, resource_type, command_name, api_params)
        else:
            output = self.api_session.ExecuteCommand(self.sandbox_id, resource, resource_type, command_name)

        return output

    def execute_blueprint_command(self, command_name, command_params: dict = {}):
        if command_params:
            api_params = [InputNameValue(param.name, param.value) for param in command_params.items()]
            output = self.api_session.ExecuteEnvironmentCommand(self.sandbox_id, command_name, api_params, printOutput=True)
        else:
            output = self.api_session.ExecuteEnvironmentCommand(self.sandbox_id, command_name, printOutput=True)

        return output

    def set_sandbox_status(self, status_name, status_reason):
        self.api_session.SetReservationLiveStatus(self.sandbox_id, status_name, status_reason)
