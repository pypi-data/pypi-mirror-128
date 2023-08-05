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
    'GetMdbPostgresqlClusterResult',
    'AwaitableGetMdbPostgresqlClusterResult',
    'get_mdb_postgresql_cluster',
    'get_mdb_postgresql_cluster_output',
]

@pulumi.output_type
class GetMdbPostgresqlClusterResult:
    """
    A collection of values returned by getMdbPostgresqlCluster.
    """
    def __init__(__self__, cluster_id=None, config=None, created_at=None, databases=None, deletion_protection=None, description=None, environment=None, folder_id=None, health=None, hosts=None, id=None, labels=None, maintenance_window=None, name=None, network_id=None, security_group_ids=None, status=None, users=None):
        if cluster_id and not isinstance(cluster_id, str):
            raise TypeError("Expected argument 'cluster_id' to be a str")
        pulumi.set(__self__, "cluster_id", cluster_id)
        if config and not isinstance(config, dict):
            raise TypeError("Expected argument 'config' to be a dict")
        pulumi.set(__self__, "config", config)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if databases and not isinstance(databases, list):
            raise TypeError("Expected argument 'databases' to be a list")
        pulumi.set(__self__, "databases", databases)
        if deletion_protection and not isinstance(deletion_protection, bool):
            raise TypeError("Expected argument 'deletion_protection' to be a bool")
        pulumi.set(__self__, "deletion_protection", deletion_protection)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if environment and not isinstance(environment, str):
            raise TypeError("Expected argument 'environment' to be a str")
        pulumi.set(__self__, "environment", environment)
        if folder_id and not isinstance(folder_id, str):
            raise TypeError("Expected argument 'folder_id' to be a str")
        pulumi.set(__self__, "folder_id", folder_id)
        if health and not isinstance(health, str):
            raise TypeError("Expected argument 'health' to be a str")
        pulumi.set(__self__, "health", health)
        if hosts and not isinstance(hosts, list):
            raise TypeError("Expected argument 'hosts' to be a list")
        pulumi.set(__self__, "hosts", hosts)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if maintenance_window and not isinstance(maintenance_window, dict):
            raise TypeError("Expected argument 'maintenance_window' to be a dict")
        pulumi.set(__self__, "maintenance_window", maintenance_window)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_id and not isinstance(network_id, str):
            raise TypeError("Expected argument 'network_id' to be a str")
        pulumi.set(__self__, "network_id", network_id)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter
    def config(self) -> 'outputs.GetMdbPostgresqlClusterConfigResult':
        """
        Configuration of the PostgreSQL cluster. The structure is documented below.
        """
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Timestamp of cluster creation.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def databases(self) -> Sequence['outputs.GetMdbPostgresqlClusterDatabaseResult']:
        """
        A database of the PostgreSQL cluster. The structure is documented below.
        """
        return pulumi.get(self, "databases")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> bool:
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        Description of the PostgreSQL cluster.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def environment(self) -> str:
        """
        Deployment environment of the PostgreSQL cluster.
        """
        return pulumi.get(self, "environment")

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> str:
        return pulumi.get(self, "folder_id")

    @property
    @pulumi.getter
    def health(self) -> str:
        """
        Aggregated health of the cluster.
        """
        return pulumi.get(self, "health")

    @property
    @pulumi.getter
    def hosts(self) -> Sequence['outputs.GetMdbPostgresqlClusterHostResult']:
        """
        A host of the PostgreSQL cluster. The structure is documented below.
        """
        return pulumi.get(self, "hosts")

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
        A set of key/value label pairs to assign to the PostgreSQL cluster.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="maintenanceWindow")
    def maintenance_window(self) -> 'outputs.GetMdbPostgresqlClusterMaintenanceWindowResult':
        """
        Maintenance window settings of the PostgreSQL cluster. The structure is documented below.
        """
        return pulumi.get(self, "maintenance_window")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the database extension. For more information on available extensions see [the official documentation](https://cloud.yandex.com/docs/managed-postgresql/operations/cluster-extensions).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkId")
    def network_id(self) -> str:
        """
        ID of the network, to which the PostgreSQL cluster belongs.
        """
        return pulumi.get(self, "network_id")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        A set of ids of security groups assigned to hosts of the cluster.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the cluster.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def users(self) -> Sequence['outputs.GetMdbPostgresqlClusterUserResult']:
        """
        A user of the PostgreSQL cluster. The structure is documented below.
        """
        return pulumi.get(self, "users")


class AwaitableGetMdbPostgresqlClusterResult(GetMdbPostgresqlClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMdbPostgresqlClusterResult(
            cluster_id=self.cluster_id,
            config=self.config,
            created_at=self.created_at,
            databases=self.databases,
            deletion_protection=self.deletion_protection,
            description=self.description,
            environment=self.environment,
            folder_id=self.folder_id,
            health=self.health,
            hosts=self.hosts,
            id=self.id,
            labels=self.labels,
            maintenance_window=self.maintenance_window,
            name=self.name,
            network_id=self.network_id,
            security_group_ids=self.security_group_ids,
            status=self.status,
            users=self.users)


def get_mdb_postgresql_cluster(cluster_id: Optional[str] = None,
                               deletion_protection: Optional[bool] = None,
                               description: Optional[str] = None,
                               folder_id: Optional[str] = None,
                               name: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMdbPostgresqlClusterResult:
    """
    Get information about a Yandex Managed PostgreSQL cluster. For more information, see
    [the official documentation](https://cloud.yandex.com/docs/managed-postgresql/).
    [How to connect to the DB](https://cloud.yandex.com/en-ru/docs/managed-postgresql/quickstart#connect). To connect, use port 6432. The port number is not configurable.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_yandex as yandex

    foo = yandex.get_mdb_postgresql_cluster(name="test")
    pulumi.export("fqdn", foo.hosts[0].fqdn)
    ```


    :param str cluster_id: The ID of the PostgreSQL cluster.
    :param str description: Description of the PostgreSQL cluster.
    :param str folder_id: The ID of the folder that the resource belongs to. If it is not provided, the default provider folder is used.
    :param str name: The name of the PostgreSQL cluster.
    """
    __args__ = dict()
    __args__['clusterId'] = cluster_id
    __args__['deletionProtection'] = deletion_protection
    __args__['description'] = description
    __args__['folderId'] = folder_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('yandex:index/getMdbPostgresqlCluster:getMdbPostgresqlCluster', __args__, opts=opts, typ=GetMdbPostgresqlClusterResult).value

    return AwaitableGetMdbPostgresqlClusterResult(
        cluster_id=__ret__.cluster_id,
        config=__ret__.config,
        created_at=__ret__.created_at,
        databases=__ret__.databases,
        deletion_protection=__ret__.deletion_protection,
        description=__ret__.description,
        environment=__ret__.environment,
        folder_id=__ret__.folder_id,
        health=__ret__.health,
        hosts=__ret__.hosts,
        id=__ret__.id,
        labels=__ret__.labels,
        maintenance_window=__ret__.maintenance_window,
        name=__ret__.name,
        network_id=__ret__.network_id,
        security_group_ids=__ret__.security_group_ids,
        status=__ret__.status,
        users=__ret__.users)


@_utilities.lift_output_func(get_mdb_postgresql_cluster)
def get_mdb_postgresql_cluster_output(cluster_id: Optional[pulumi.Input[Optional[str]]] = None,
                                      deletion_protection: Optional[pulumi.Input[Optional[bool]]] = None,
                                      description: Optional[pulumi.Input[Optional[str]]] = None,
                                      folder_id: Optional[pulumi.Input[Optional[str]]] = None,
                                      name: Optional[pulumi.Input[Optional[str]]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMdbPostgresqlClusterResult]:
    """
    Get information about a Yandex Managed PostgreSQL cluster. For more information, see
    [the official documentation](https://cloud.yandex.com/docs/managed-postgresql/).
    [How to connect to the DB](https://cloud.yandex.com/en-ru/docs/managed-postgresql/quickstart#connect). To connect, use port 6432. The port number is not configurable.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_yandex as yandex

    foo = yandex.get_mdb_postgresql_cluster(name="test")
    pulumi.export("fqdn", foo.hosts[0].fqdn)
    ```


    :param str cluster_id: The ID of the PostgreSQL cluster.
    :param str description: Description of the PostgreSQL cluster.
    :param str folder_id: The ID of the folder that the resource belongs to. If it is not provided, the default provider folder is used.
    :param str name: The name of the PostgreSQL cluster.
    """
    ...
