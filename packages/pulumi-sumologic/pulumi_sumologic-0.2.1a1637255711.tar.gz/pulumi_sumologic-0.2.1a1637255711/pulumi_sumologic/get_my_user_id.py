# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetMyUserIdResult',
    'AwaitableGetMyUserIdResult',
    'get_my_user_id',
    'get_my_user_id_output',
]

@pulumi.output_type
class GetMyUserIdResult:
    """
    A collection of values returned by getMyUserId.
    """
    def __init__(__self__, id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")


class AwaitableGetMyUserIdResult(GetMyUserIdResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMyUserIdResult(
            id=self.id)


def get_my_user_id(id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMyUserIdResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['id'] = id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('sumologic:index/getMyUserId:getMyUserId', __args__, opts=opts, typ=GetMyUserIdResult).value

    return AwaitableGetMyUserIdResult(
        id=__ret__.id)


@_utilities.lift_output_func(get_my_user_id)
def get_my_user_id_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetMyUserIdResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
