from typing import Optional, List
from enum import Enum

from cloudrail.knowledge.context.gcp.resources.constants.gcp_resource_type import GcpResourceType
from cloudrail.knowledge.context.gcp.resources.gcp_resource import GcpResource


class GcpComputeNetworkRoutingMode(Enum):
    REGIONAL = 'REGIONAL'
    GLOBAL = 'GLOBAL'


class GcpComputeNetwork(GcpResource):
    """
        Attributes:
        name: (Required) A unique name of the resource.
        auto_create_subnetworks: (Optional) When set to true, the network is created in "auto subnet mode" and it will
        create a subnet for each region automatically across the 10.128.0.0/9 address range.
        routing_mode: (Optional) The network-wide routing mode to use. Possible values are REGIONAL and GLOBAL.
    """

    def __init__(self,
                 name: str,
                 auto_create_subnetworks: Optional[bool],
                 routing_mode: Optional[GcpComputeNetworkRoutingMode]):
        super().__init__(GcpResourceType.GOOGLE_COMPUTE_NETWORK)
        self.name: str = name
        self.auto_create_subnetworks: Optional[bool] = auto_create_subnetworks
        self.routing_mode: Optional[GcpComputeNetworkRoutingMode] = routing_mode

    def get_keys(self) -> List[str]:
        return [self.name, self.project_id]

    def get_name(self) -> str:
        return self.name

    @property
    def is_labeled(self) -> bool:
        return False

    @property
    def is_tagable(self) -> bool:
        return False

    def get_cloud_resource_url(self) -> Optional[str]:
        return f'{self._BASE_URL}/networking/networks/details/{self.name}?project={self.project_id}'

    def get_type(self, is_plural: bool = False) -> str:
        return 'Compute Network Details'

    def to_drift_detection_object(self) -> dict:
        return {'auto_create_subnetworks': self.auto_create_subnetworks,
                'routing_mode': self.routing_mode}
