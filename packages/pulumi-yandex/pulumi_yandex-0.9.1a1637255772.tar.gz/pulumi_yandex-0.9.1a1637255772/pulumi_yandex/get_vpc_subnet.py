# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs

__all__ = [
    'GetVpcSubnetResult',
    'AwaitableGetVpcSubnetResult',
    'get_vpc_subnet',
    'get_vpc_subnet_output',
]

@pulumi.output_type
class GetVpcSubnetResult:
    """
    A collection of values returned by getVpcSubnet.
    """
    def __init__(__self__, created_at=None, description=None, dhcp_options=None, folder_id=None, id=None, labels=None, name=None, network_id=None, route_table_id=None, subnet_id=None, v4_cidr_blocks=None, v6_cidr_blocks=None, zone=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if dhcp_options and not isinstance(dhcp_options, dict):
            raise TypeError("Expected argument 'dhcp_options' to be a dict")
        pulumi.set(__self__, "dhcp_options", dhcp_options)
        if folder_id and not isinstance(folder_id, str):
            raise TypeError("Expected argument 'folder_id' to be a str")
        pulumi.set(__self__, "folder_id", folder_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_id and not isinstance(network_id, str):
            raise TypeError("Expected argument 'network_id' to be a str")
        pulumi.set(__self__, "network_id", network_id)
        if route_table_id and not isinstance(route_table_id, str):
            raise TypeError("Expected argument 'route_table_id' to be a str")
        pulumi.set(__self__, "route_table_id", route_table_id)
        if subnet_id and not isinstance(subnet_id, str):
            raise TypeError("Expected argument 'subnet_id' to be a str")
        pulumi.set(__self__, "subnet_id", subnet_id)
        if v4_cidr_blocks and not isinstance(v4_cidr_blocks, list):
            raise TypeError("Expected argument 'v4_cidr_blocks' to be a list")
        pulumi.set(__self__, "v4_cidr_blocks", v4_cidr_blocks)
        if v6_cidr_blocks and not isinstance(v6_cidr_blocks, list):
            raise TypeError("Expected argument 'v6_cidr_blocks' to be a list")
        pulumi.set(__self__, "v6_cidr_blocks", v6_cidr_blocks)
        if zone and not isinstance(zone, str):
            raise TypeError("Expected argument 'zone' to be a str")
        pulumi.set(__self__, "zone", zone)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Creation timestamp of this subnet.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the subnet.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="dhcpOptions")
    def dhcp_options(self) -> 'outputs.GetVpcSubnetDhcpOptionsResult':
        """
        Options for DHCP client. The structure is documented below.
        """
        return pulumi.get(self, "dhcp_options")

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> str:
        return pulumi.get(self, "folder_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def labels(self) -> Mapping[str, str]:
        """
        Labels to assign to this subnet.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkId")
    def network_id(self) -> str:
        """
        ID of the network this subnet belongs to.
        """
        return pulumi.get(self, "network_id")

    @property
    @pulumi.getter(name="routeTableId")
    def route_table_id(self) -> str:
        """
        ID of the route table to assign to this subnet.
        """
        return pulumi.get(self, "route_table_id")

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> str:
        return pulumi.get(self, "subnet_id")

    @property
    @pulumi.getter(name="v4CidrBlocks")
    def v4_cidr_blocks(self) -> Sequence[str]:
        """
        The blocks of internal IPv4 addresses owned by this subnet.
        """
        return pulumi.get(self, "v4_cidr_blocks")

    @property
    @pulumi.getter(name="v6CidrBlocks")
    def v6_cidr_blocks(self) -> Sequence[str]:
        """
        The blocks of internal IPv6 addresses owned by this subnet.
        """
        return pulumi.get(self, "v6_cidr_blocks")

    @property
    @pulumi.getter
    def zone(self) -> str:
        """
        Name of the availability zone for this subnet.
        """
        return pulumi.get(self, "zone")


class AwaitableGetVpcSubnetResult(GetVpcSubnetResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcSubnetResult(
            created_at=self.created_at,
            description=self.description,
            dhcp_options=self.dhcp_options,
            folder_id=self.folder_id,
            id=self.id,
            labels=self.labels,
            name=self.name,
            network_id=self.network_id,
            route_table_id=self.route_table_id,
            subnet_id=self.subnet_id,
            v4_cidr_blocks=self.v4_cidr_blocks,
            v6_cidr_blocks=self.v6_cidr_blocks,
            zone=self.zone)


def get_vpc_subnet(folder_id: Optional[str] = None,
                   name: Optional[str] = None,
                   subnet_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcSubnetResult:
    """
    Get information about a Yandex VPC subnet. For more information, see
    [Yandex.Cloud VPC](https://cloud.yandex.com/docs/vpc/concepts/index).

    ```python
    import pulumi
    import pulumi_yandex as yandex

    admin = yandex.get_vpc_subnet(subnet_id="my-subnet-id")
    ```

    This data source is used to define [VPC Subnets] that can be used by other resources.


    :param str folder_id: Folder that the resource belongs to. If value is omitted, the default provider folder is used.
    :param str name: - Name of the subnet.
    :param str subnet_id: Subnet ID.
    """
    __args__ = dict()
    __args__['folderId'] = folder_id
    __args__['name'] = name
    __args__['subnetId'] = subnet_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('yandex:index/getVpcSubnet:getVpcSubnet', __args__, opts=opts, typ=GetVpcSubnetResult).value

    return AwaitableGetVpcSubnetResult(
        created_at=__ret__.created_at,
        description=__ret__.description,
        dhcp_options=__ret__.dhcp_options,
        folder_id=__ret__.folder_id,
        id=__ret__.id,
        labels=__ret__.labels,
        name=__ret__.name,
        network_id=__ret__.network_id,
        route_table_id=__ret__.route_table_id,
        subnet_id=__ret__.subnet_id,
        v4_cidr_blocks=__ret__.v4_cidr_blocks,
        v6_cidr_blocks=__ret__.v6_cidr_blocks,
        zone=__ret__.zone)


@_utilities.lift_output_func(get_vpc_subnet)
def get_vpc_subnet_output(folder_id: Optional[pulumi.Input[Optional[str]]] = None,
                          name: Optional[pulumi.Input[Optional[str]]] = None,
                          subnet_id: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcSubnetResult]:
    """
    Get information about a Yandex VPC subnet. For more information, see
    [Yandex.Cloud VPC](https://cloud.yandex.com/docs/vpc/concepts/index).

    ```python
    import pulumi
    import pulumi_yandex as yandex

    admin = yandex.get_vpc_subnet(subnet_id="my-subnet-id")
    ```

    This data source is used to define [VPC Subnets] that can be used by other resources.


    :param str folder_id: Folder that the resource belongs to. If value is omitted, the default provider folder is used.
    :param str name: - Name of the subnet.
    :param str subnet_id: Subnet ID.
    """
    ...
