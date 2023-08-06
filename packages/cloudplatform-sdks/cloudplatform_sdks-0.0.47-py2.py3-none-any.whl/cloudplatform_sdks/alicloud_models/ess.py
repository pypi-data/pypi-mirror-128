from .clients import ess_client


class AliEss:

    def __init__(self, ess_info=None):
        self.ess_info = ess_info

    @classmethod
    def get_list(cls, params=None):
        return ess_client.describe_scaling_instances(params)

    @classmethod
    def get_scaling_groups(cls, params=None):
        return ess_client.describe_scaling_groups(params)