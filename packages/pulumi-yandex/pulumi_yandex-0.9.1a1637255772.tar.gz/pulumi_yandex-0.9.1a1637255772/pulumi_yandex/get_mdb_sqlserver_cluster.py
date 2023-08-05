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
    'GetMdbSqlserverClusterResult',
    'AwaitableGetMdbSqlserverClusterResult',
    'get_mdb_sqlserver_cluster',
    'get_mdb_sqlserver_cluster_output',
]

@pulumi.output_type
class GetMdbSqlserverClusterResult:
    """
    A collection of values returned by getMdbSqlserverCluster.
    """
    def __init__(__self__, backup_window_starts=None, cluster_id=None, created_at=None, databases=None, deletion_protection=None, description=None, environment=None, folder_id=None, health=None, hosts=None, id=None, labels=None, name=None, network_id=None, resources=None, security_group_ids=None, sqlserver_config=None, status=None, users=None, version=None):
        if backup_window_starts and not isinstance(backup_window_starts, list):
            raise TypeError("Expected argument 'backup_window_starts' to be a list")
        pulumi.set(__self__, "backup_window_starts", backup_window_starts)
        if cluster_id and not isinstance(cluster_id, str):
            raise TypeError("Expected argument 'cluster_id' to be a str")
        pulumi.set(__self__, "cluster_id", cluster_id)
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
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if network_id and not isinstance(network_id, str):
            raise TypeError("Expected argument 'network_id' to be a str")
        pulumi.set(__self__, "network_id", network_id)
        if resources and not isinstance(resources, list):
            raise TypeError("Expected argument 'resources' to be a list")
        pulumi.set(__self__, "resources", resources)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if sqlserver_config and not isinstance(sqlserver_config, dict):
            raise TypeError("Expected argument 'sqlserver_config' to be a dict")
        pulumi.set(__self__, "sqlserver_config", sqlserver_config)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)
        if version and not isinstance(version, str):
            raise TypeError("Expected argument 'version' to be a str")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter(name="backupWindowStarts")
    def backup_window_starts(self) -> Sequence['outputs.GetMdbSqlserverClusterBackupWindowStartResult']:
        return pulumi.get(self, "backup_window_starts")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> str:
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Creation timestamp of the key.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def databases(self) -> Sequence['outputs.GetMdbSqlserverClusterDatabaseResult']:
        """
        A database of the SQLServer cluster. The structure is documented below.
        """
        return pulumi.get(self, "databases")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> bool:
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the SQLServer cluster.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def environment(self) -> str:
        """
        Deployment environment of the SQLServer cluster.
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
    def hosts(self) -> Sequence['outputs.GetMdbSqlserverClusterHostResult']:
        """
        A host of the SQLServer cluster. The structure is documented below.
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
        A set of key/value label pairs to assign to the SQLServer cluster.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the database.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="networkId")
    def network_id(self) -> str:
        """
        ID of the network, to which the SQLServer cluster belongs.
        """
        return pulumi.get(self, "network_id")

    @property
    @pulumi.getter
    def resources(self) -> Sequence['outputs.GetMdbSqlserverClusterResourceResult']:
        """
        Resources allocated to hosts of the SQLServer cluster. The structure is documented below.
        """
        return pulumi.get(self, "resources")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        A set of ids of security groups assigned to hosts of the cluster.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="sqlserverConfig")
    def sqlserver_config(self) -> Mapping[str, str]:
        """
        SQLServer cluster config.
        """
        return pulumi.get(self, "sqlserver_config")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the cluster.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def users(self) -> Sequence['outputs.GetMdbSqlserverClusterUserResult']:
        """
        A user of the SQLServer cluster. The structure is documented below.
        """
        return pulumi.get(self, "users")

    @property
    @pulumi.getter
    def version(self) -> str:
        """
        Version of the SQLServer cluster.
        """
        return pulumi.get(self, "version")


class AwaitableGetMdbSqlserverClusterResult(GetMdbSqlserverClusterResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMdbSqlserverClusterResult(
            backup_window_starts=self.backup_window_starts,
            cluster_id=self.cluster_id,
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
            name=self.name,
            network_id=self.network_id,
            resources=self.resources,
            security_group_ids=self.security_group_ids,
            sqlserver_config=self.sqlserver_config,
            status=self.status,
            users=self.users,
            version=self.version)


def get_mdb_sqlserver_cluster(cluster_id: Optional[str] = None,
                              deletion_protection: Optional[bool] = None,
                              folder_id: Optional[str] = None,
                              name: Optional[str] = None,
                              sqlserver_config: Optional[Mapping[str, str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMdbSqlserverClusterResult:
    """
    Get information about a Yandex Managed SQLServer cluster. For more information, see
    [the official documentation](https://cloud.yandex.com/docs/managed-sqlserver/).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_yandex as yandex

    foo = yandex.get_mdb_sqlserver_cluster(name="test")
    pulumi.export("networkId", foo.network_id)
    ```


    :param str cluster_id: The ID of the SQLServer cluster.
    :param str folder_id: The ID of the folder that the resource belongs to. If it is not provided, the default provider folder is used.
    :param str name: The name of the SQLServer cluster.
    :param Mapping[str, str] sqlserver_config: SQLServer cluster config.
    """
    __args__ = dict()
    __args__['clusterId'] = cluster_id
    __args__['deletionProtection'] = deletion_protection
    __args__['folderId'] = folder_id
    __args__['name'] = name
    __args__['sqlserverConfig'] = sqlserver_config
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('yandex:index/getMdbSqlserverCluster:getMdbSqlserverCluster', __args__, opts=opts, typ=GetMdbSqlserverClusterResult).value

    return AwaitableGetMdbSqlserverClusterResult(
        backup_window_starts=__ret__.backup_window_starts,
        cluster_id=__ret__.cluster_id,
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
        name=__ret__.name,
        network_id=__ret__.network_id,
        resources=__ret__.resources,
        security_group_ids=__ret__.security_group_ids,
        sqlserver_config=__ret__.sqlserver_config,
        status=__ret__.status,
        users=__ret__.users,
        version=__ret__.version)


@_utilities.lift_output_func(get_mdb_sqlserver_cluster)
def get_mdb_sqlserver_cluster_output(cluster_id: Optional[pulumi.Input[Optional[str]]] = None,
                                     deletion_protection: Optional[pulumi.Input[Optional[bool]]] = None,
                                     folder_id: Optional[pulumi.Input[Optional[str]]] = None,
                                     name: Optional[pulumi.Input[Optional[str]]] = None,
                                     sqlserver_config: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMdbSqlserverClusterResult]:
    """
    Get information about a Yandex Managed SQLServer cluster. For more information, see
    [the official documentation](https://cloud.yandex.com/docs/managed-sqlserver/).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_yandex as yandex

    foo = yandex.get_mdb_sqlserver_cluster(name="test")
    pulumi.export("networkId", foo.network_id)
    ```


    :param str cluster_id: The ID of the SQLServer cluster.
    :param str folder_id: The ID of the folder that the resource belongs to. If it is not provided, the default provider folder is used.
    :param str name: The name of the SQLServer cluster.
    :param Mapping[str, str] sqlserver_config: SQLServer cluster config.
    """
    ...
