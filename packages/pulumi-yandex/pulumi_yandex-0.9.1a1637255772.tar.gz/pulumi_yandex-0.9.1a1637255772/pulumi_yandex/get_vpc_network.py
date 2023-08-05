# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetVpcNetworkResult',
    'AwaitableGetVpcNetworkResult',
    'get_vpc_network',
    'get_vpc_network_output',
]

@pulumi.output_type
class GetVpcNetworkResult:
    """
    A collection of values returned by getVpcNetwork.
    """
    def __init__(__self__, created_at=None, default_security_group_id=None, description=None, folder_id=None, id=None, labels=None, name=None, network_id=None, subnet_ids=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if default_security_group_id and not isinstance(default_security_group_id, str):
            raise TypeError("Expected argument 'default_security_group_id' to be a str")
        pulumi.set(__self__, "default_security_group_id", default_security_group_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
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
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Creation timestamp of this network.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="defaultSecurityGroupId")
    def default_security_group_id(self) -> str:
        """
        ID of default Security Group of this network.
        """
        return pulumi.get(self, "default_security_group_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the network.
        """
        return pulumi.get(self, "description")

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
        Labels assigned to this network.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkId")
    def network_id(self) -> str:
        return pulumi.get(self, "network_id")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        return pulumi.get(self, "subnet_ids")


class AwaitableGetVpcNetworkResult(GetVpcNetworkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcNetworkResult(
            created_at=self.created_at,
            default_security_group_id=self.default_security_group_id,
            description=self.description,
            folder_id=self.folder_id,
            id=self.id,
            labels=self.labels,
            name=self.name,
            network_id=self.network_id,
            subnet_ids=self.subnet_ids)


def get_vpc_network(folder_id: Optional[str] = None,
                    name: Optional[str] = None,
                    network_id: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcNetworkResult:
    """
    Get information about a Yandex VPC network. For more information, see
    [Yandex.Cloud VPC](https://cloud.yandex.com/docs/vpc/concepts/index).

    ```python
    import pulumi
    import pulumi_yandex as yandex

    admin = yandex.get_vpc_network(network_id="my-network-id")
    ```

    This data source is used to define [VPC Networks] that can be used by other resources.


    :param str folder_id: Folder that the resource belongs to. If value is omitted, the default provider folder is used.
    :param str name: Name of the network.
    :param str network_id: ID of the network.
    """
    __args__ = dict()
    __args__['folderId'] = folder_id
    __args__['name'] = name
    __args__['networkId'] = network_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('yandex:index/getVpcNetwork:getVpcNetwork', __args__, opts=opts, typ=GetVpcNetworkResult).value

    return AwaitableGetVpcNetworkResult(
        created_at=__ret__.created_at,
        default_security_group_id=__ret__.default_security_group_id,
        description=__ret__.description,
        folder_id=__ret__.folder_id,
        id=__ret__.id,
        labels=__ret__.labels,
        name=__ret__.name,
        network_id=__ret__.network_id,
        subnet_ids=__ret__.subnet_ids)


@_utilities.lift_output_func(get_vpc_network)
def get_vpc_network_output(folder_id: Optional[pulumi.Input[Optional[str]]] = None,
                           name: Optional[pulumi.Input[Optional[str]]] = None,
                           network_id: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcNetworkResult]:
    """
    Get information about a Yandex VPC network. For more information, see
    [Yandex.Cloud VPC](https://cloud.yandex.com/docs/vpc/concepts/index).

    ```python
    import pulumi
    import pulumi_yandex as yandex

    admin = yandex.get_vpc_network(network_id="my-network-id")
    ```

    This data source is used to define [VPC Networks] that can be used by other resources.


    :param str folder_id: Folder that the resource belongs to. If value is omitted, the default provider folder is used.
    :param str name: Name of the network.
    :param str network_id: ID of the network.
    """
    ...
