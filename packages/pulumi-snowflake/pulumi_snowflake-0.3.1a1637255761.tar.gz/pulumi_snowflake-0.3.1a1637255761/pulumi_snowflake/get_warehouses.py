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
    'GetWarehousesResult',
    'AwaitableGetWarehousesResult',
    'get_warehouses',
]

@pulumi.output_type
class GetWarehousesResult:
    """
    A collection of values returned by getWarehouses.
    """
    def __init__(__self__, id=None, warehouses=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if warehouses and not isinstance(warehouses, list):
            raise TypeError("Expected argument 'warehouses' to be a list")
        pulumi.set(__self__, "warehouses", warehouses)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def warehouses(self) -> Sequence['outputs.GetWarehousesWarehouseResult']:
        """
        The warehouses in the database
        """
        return pulumi.get(self, "warehouses")


class AwaitableGetWarehousesResult(GetWarehousesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWarehousesResult(
            id=self.id,
            warehouses=self.warehouses)


def get_warehouses(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWarehousesResult:
    """
    ## Example Usage

    ```python
    import pulumi
    import pulumi_snowflake as snowflake

    current = snowflake.get_warehouses()
    ```
    """
    __args__ = dict()
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('snowflake:index/getWarehouses:getWarehouses', __args__, opts=opts, typ=GetWarehousesResult).value

    return AwaitableGetWarehousesResult(
        id=__ret__.id,
        warehouses=__ret__.warehouses)
