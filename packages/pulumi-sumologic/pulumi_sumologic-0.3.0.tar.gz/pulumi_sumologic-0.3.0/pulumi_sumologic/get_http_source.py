# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetHttpSourceResult',
    'AwaitableGetHttpSourceResult',
    'get_http_source',
    'get_http_source_output',
]

@pulumi.output_type
class GetHttpSourceResult:
    """
    A collection of values returned by getHttpSource.
    """
    def __init__(__self__, category=None, collector_id=None, description=None, id=None, multiline=None, name=None, timezone=None, url=None):
        if category and not isinstance(category, str):
            raise TypeError("Expected argument 'category' to be a str")
        pulumi.set(__self__, "category", category)
        if collector_id and not isinstance(collector_id, int):
            raise TypeError("Expected argument 'collector_id' to be a int")
        pulumi.set(__self__, "collector_id", collector_id)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, int):
            raise TypeError("Expected argument 'id' to be a int")
        pulumi.set(__self__, "id", id)
        if multiline and not isinstance(multiline, bool):
            raise TypeError("Expected argument 'multiline' to be a bool")
        pulumi.set(__self__, "multiline", multiline)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if timezone and not isinstance(timezone, str):
            raise TypeError("Expected argument 'timezone' to be a str")
        pulumi.set(__self__, "timezone", timezone)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def category(self) -> str:
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="collectorId")
    def collector_id(self) -> Optional[int]:
        return pulumi.get(self, "collector_id")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> int:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def multiline(self) -> bool:
        return pulumi.get(self, "multiline")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def timezone(self) -> str:
        return pulumi.get(self, "timezone")

    @property
    @pulumi.getter
    def url(self) -> str:
        return pulumi.get(self, "url")


class AwaitableGetHttpSourceResult(GetHttpSourceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHttpSourceResult(
            category=self.category,
            collector_id=self.collector_id,
            description=self.description,
            id=self.id,
            multiline=self.multiline,
            name=self.name,
            timezone=self.timezone,
            url=self.url)


def get_http_source(collector_id: Optional[int] = None,
                    id: Optional[int] = None,
                    name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHttpSourceResult:
    """
    Use this data source to access information about an existing resource.
    """
    __args__ = dict()
    __args__['collectorId'] = collector_id
    __args__['id'] = id
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('sumologic:index/getHttpSource:getHttpSource', __args__, opts=opts, typ=GetHttpSourceResult).value

    return AwaitableGetHttpSourceResult(
        category=__ret__.category,
        collector_id=__ret__.collector_id,
        description=__ret__.description,
        id=__ret__.id,
        multiline=__ret__.multiline,
        name=__ret__.name,
        timezone=__ret__.timezone,
        url=__ret__.url)


@_utilities.lift_output_func(get_http_source)
def get_http_source_output(collector_id: Optional[pulumi.Input[Optional[int]]] = None,
                           id: Optional[pulumi.Input[Optional[int]]] = None,
                           name: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHttpSourceResult]:
    """
    Use this data source to access information about an existing resource.
    """
    ...
