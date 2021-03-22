from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.cloudformation.checks.resource.base_resource_check import BaseResourceCheck
from checkov.common.util.secrets import string_has_secrets, AWS

class LambdaEnvironmentCredentials(BaseResourceCheck):
    def __init__(self):
        name = "Ensure no hard-coded secrets exist in lambda environment"
        id = "CKV_AWS_45"
        supported_resources = ['AWS::Lambda::Function']
        categories = [CheckCategories.SECRETS]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'Properties' in conf.keys():
            properties = conf['Properties']
            if 'Environment' in properties.keys():
                environment = properties['Environment']
                if 'Variables' in environment.keys():
                    variables = environment['Variables']
                    for value in variables.values():
                        if string_has_secrets(str(value), AWS):
                            return CheckResult.FAILED

        return CheckResult.PASSED


check = LambdaEnvironmentCredentials()
