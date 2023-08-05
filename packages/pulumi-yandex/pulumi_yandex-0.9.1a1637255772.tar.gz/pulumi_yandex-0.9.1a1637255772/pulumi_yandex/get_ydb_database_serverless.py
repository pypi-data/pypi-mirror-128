# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetYdbDatabaseServerlessResult',
    'AwaitableGetYdbDatabaseServerlessResult',
    'get_ydb_database_serverless',
    'get_ydb_database_serverless_output',
]

@pulumi.output_type
class GetYdbDatabaseServerlessResult:
    """
    A collection of values returned by getYdbDatabaseServerless.
    """
    def __init__(__self__, created_at=None, database_id=None, database_path=None, description=None, document_api_endpoint=None, folder_id=None, id=None, labels=None, location_id=None, name=None, status=None, tls_enabled=None, ydb_api_endpoint=None, ydb_full_endpoint=None):
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if database_id and not isinstance(database_id, str):
            raise TypeError("Expected argument 'database_id' to be a str")
        pulumi.set(__self__, "database_id", database_id)
        if database_path and not isinstance(database_path, str):
            raise TypeError("Expected argument 'database_path' to be a str")
        pulumi.set(__self__, "database_path", database_path)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if document_api_endpoint and not isinstance(document_api_endpoint, str):
            raise TypeError("Expected argument 'document_api_endpoint' to be a str")
        pulumi.set(__self__, "document_api_endpoint", document_api_endpoint)
        if folder_id and not isinstance(folder_id, str):
            raise TypeError("Expected argument 'folder_id' to be a str")
        pulumi.set(__self__, "folder_id", folder_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if labels and not isinstance(labels, dict):
            raise TypeError("Expected argument 'labels' to be a dict")
        pulumi.set(__self__, "labels", labels)
        if location_id and not isinstance(location_id, str):
            raise TypeError("Expected argument 'location_id' to be a str")
        pulumi.set(__self__, "location_id", location_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tls_enabled and not isinstance(tls_enabled, bool):
            raise TypeError("Expected argument 'tls_enabled' to be a bool")
        pulumi.set(__self__, "tls_enabled", tls_enabled)
        if ydb_api_endpoint and not isinstance(ydb_api_endpoint, str):
            raise TypeError("Expected argument 'ydb_api_endpoint' to be a str")
        pulumi.set(__self__, "ydb_api_endpoint", ydb_api_endpoint)
        if ydb_full_endpoint and not isinstance(ydb_full_endpoint, str):
            raise TypeError("Expected argument 'ydb_full_endpoint' to be a str")
        pulumi.set(__self__, "ydb_full_endpoint", ydb_full_endpoint)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The Yandex Database serverless cluster creation timestamp.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="databaseId")
    def database_id(self) -> Optional[str]:
        return pulumi.get(self, "database_id")

    @property
    @pulumi.getter(name="databasePath")
    def database_path(self) -> str:
        """
        Full database path of the Yandex Database serverless cluster.
        Useful for SDK configuration.
        """
        return pulumi.get(self, "database_path")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        A description of the Yandex Database serverless cluster.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentApiEndpoint")
    def document_api_endpoint(self) -> str:
        """
        Document API endpoint of the Yandex Database serverless cluster.
        """
        return pulumi.get(self, "document_api_endpoint")

    @property
    @pulumi.getter(name="folderId")
    def folder_id(self) -> Optional[str]:
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
        A set of key/value label pairs assigned to the Yandex Database serverless cluster.
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter(name="locationId")
    def location_id(self) -> str:
        """
        Location ID of the Yandex Database serverless cluster.
        """
        return pulumi.get(self, "location_id")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Status of the Yandex Database serverless cluster.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="tlsEnabled")
    def tls_enabled(self) -> bool:
        """
        Whether TLS is enabled for the Yandex Database serverless cluster.
        Useful for SDK configuration.
        """
        return pulumi.get(self, "tls_enabled")

    @property
    @pulumi.getter(name="ydbApiEndpoint")
    def ydb_api_endpoint(self) -> str:
        """
        API endpoint of the Yandex Database serverless cluster.
        Useful for SDK configuration.
        """
        return pulumi.get(self, "ydb_api_endpoint")

    @property
    @pulumi.getter(name="ydbFullEndpoint")
    def ydb_full_endpoint(self) -> str:
        """
        Full endpoint of the Yandex Database serverless cluster.
        """
        return pulumi.get(self, "ydb_full_endpoint")


class AwaitableGetYdbDatabaseServerlessResult(GetYdbDatabaseServerlessResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetYdbDatabaseServerlessResult(
            created_at=self.created_at,
            database_id=self.database_id,
            database_path=self.database_path,
            description=self.description,
            document_api_endpoint=self.document_api_endpoint,
            folder_id=self.folder_id,
            id=self.id,
            labels=self.labels,
            location_id=self.location_id,
            name=self.name,
            status=self.status,
            tls_enabled=self.tls_enabled,
            ydb_api_endpoint=self.ydb_api_endpoint,
            ydb_full_endpoint=self.ydb_full_endpoint)


def get_ydb_database_serverless(database_id: Optional[str] = None,
                                folder_id: Optional[str] = None,
                                name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetYdbDatabaseServerlessResult:
    """
    Get information about a Yandex Database serverless cluster.
    For more information, see [the official documentation](https://cloud.yandex.com/en/docs/ydb/concepts/serverless_and_dedicated).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_yandex as yandex

    my_database = yandex.get_ydb_database_serverless(database_id="some_ydb_serverless_database_id")
    pulumi.export("ydbApiEndpoint", my_database.ydb_api_endpoint)
    ```


    :param str database_id: ID of the Yandex Database serverless cluster.
    :param str folder_id: ID of the folder that the Yandex Database serverless cluster belongs to.
           It will be deduced from provider configuration if not set explicitly.
    :param str name: Name of the Yandex Database serverless cluster.
    """
    __args__ = dict()
    __args__['databaseId'] = database_id
    __args__['folderId'] = folder_id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('yandex:index/getYdbDatabaseServerless:getYdbDatabaseServerless', __args__, opts=opts, typ=GetYdbDatabaseServerlessResult).value

    return AwaitableGetYdbDatabaseServerlessResult(
        created_at=__ret__.created_at,
        database_id=__ret__.database_id,
        database_path=__ret__.database_path,
        description=__ret__.description,
        document_api_endpoint=__ret__.document_api_endpoint,
        folder_id=__ret__.folder_id,
        id=__ret__.id,
        labels=__ret__.labels,
        location_id=__ret__.location_id,
        name=__ret__.name,
        status=__ret__.status,
        tls_enabled=__ret__.tls_enabled,
        ydb_api_endpoint=__ret__.ydb_api_endpoint,
        ydb_full_endpoint=__ret__.ydb_full_endpoint)


@_utilities.lift_output_func(get_ydb_database_serverless)
def get_ydb_database_serverless_output(database_id: Optional[pulumi.Input[Optional[str]]] = None,
                                       folder_id: Optional[pulumi.Input[Optional[str]]] = None,
                                       name: Optional[pulumi.Input[Optional[str]]] = None,
                                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetYdbDatabaseServerlessResult]:
    """
    Get information about a Yandex Database serverless cluster.
    For more information, see [the official documentation](https://cloud.yandex.com/en/docs/ydb/concepts/serverless_and_dedicated).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_yandex as yandex

    my_database = yandex.get_ydb_database_serverless(database_id="some_ydb_serverless_database_id")
    pulumi.export("ydbApiEndpoint", my_database.ydb_api_endpoint)
    ```


    :param str database_id: ID of the Yandex Database serverless cluster.
    :param str folder_id: ID of the folder that the Yandex Database serverless cluster belongs to.
           It will be deduced from provider configuration if not set explicitly.
    :param str name: Name of the Yandex Database serverless cluster.
    """
    ...
