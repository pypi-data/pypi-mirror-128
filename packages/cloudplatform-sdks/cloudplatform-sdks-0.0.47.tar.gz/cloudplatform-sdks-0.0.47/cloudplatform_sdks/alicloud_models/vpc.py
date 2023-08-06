from .clients import vpc_client


class AliVpc:

    STATUS_MAPPER = {
        'Available': 'available',
        'InUse': 'inuse',
        'Deleted': 'deleted',
        'Pending': 'pending',
    }

    def __init__(self, vpc_info):
        self.vpc_info = vpc_info

    @classmethod
    def get_vpc_list(cls, params=None):
        return vpc_client.describe_vpcs(params)

    @classmethod
    def get_vpc_attribute(cls, params=None):
        return vpc_client.describe_vpc_attribute(params)

    @classmethod
    def get_vswitches_list(cls, params=None):
        return vpc_client.describe_vswitches(params)

    @classmethod
    def get_vswitches_attribute(cls, params=None):
        return vpc_client.describe_vswitch_attributes(params)

    @classmethod
    def get_eip_address(cls, params=None):
        return vpc_client.describe_eip_address(params)
