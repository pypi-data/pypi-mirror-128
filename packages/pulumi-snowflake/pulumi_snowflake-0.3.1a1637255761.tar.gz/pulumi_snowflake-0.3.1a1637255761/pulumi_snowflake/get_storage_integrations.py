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
    'GetStorageIntegrationsResult',
    'AwaitableGetStorageIntegrationsResult',
    'get_storage_integrations',
]

@pulumi.output_type
class GetStorageIntegrationsResult:
    """
    A collection of values returned by getStorageIntegrations.
    """
    def __init__(__self__, id=None, storage_integrations=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if storage_integrations and not isinstance(storage_integrations, list):
            raise TypeError("Expected argument 'storage_integrations' to be a list")
        pulumi.set(__self__, "storage_integrations", storage_integrations)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="storageIntegrations")
    def storage_integrations(self) -> Sequence['outputs.GetStorageIntegrationsStorageIntegrationResult']:
        """
        The storage integrations in the database
        """
        return pulumi.get(self, "storage_integrations")


class AwaitableGetStorageIntegrationsResult(GetStorageIntegrationsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetStorageIntegrationsResult(
            id=self.id,
            storage_integrations=self.storage_integrations)


def get_storage_integrations(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetStorageIntegrationsResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_storage_integrations()
    ```
    """
    __args__ = dict()
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('snowflake:index/getStorageIntegrations:getStorageIntegrations', __args__, opts=opts, typ=GetStorageIntegrationsResult).value

    return AwaitableGetStorageIntegrationsResult(
        id=__ret__.id,
        storage_integrations=__ret__.storage_integrations)
