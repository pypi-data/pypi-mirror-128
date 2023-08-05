# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ContentArgs', 'Content']

@pulumi.input_type
class ContentArgs:
    def __init__(__self__, *,
                 config: pulumi.Input[str],
                 parent_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a Content resource.
        """
        pulumi.set(__self__, "config", config)
        pulumi.set(__self__, "parent_id", parent_id)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Input[str]:
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: pulumi.Input[str]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "parent_id")

    @parent_id.setter
    def parent_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "parent_id", value)


@pulumi.input_type
class _ContentState:
    def __init__(__self__, *,
                 config: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Content resources.
        """
        if config is not None:
            pulumi.set(__self__, "config", config)
        if parent_id is not None:
            pulumi.set(__self__, "parent_id", parent_id)

    @property
    @pulumi.getter
    def config(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "config")

    @config.setter
    def config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "config", value)

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "parent_id")

    @parent_id.setter
    def parent_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "parent_id", value)


class Content(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Create a Content resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a Content resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ContentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 config: Optional[pulumi.Input[str]] = None,
                 parent_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ContentArgs.__new__(ContentArgs)

            if config is None and not opts.urn:
                raise TypeError("Missing required property 'config'")
            __props__.__dict__["config"] = config
            if parent_id is None and not opts.urn:
                raise TypeError("Missing required property 'parent_id'")
            __props__.__dict__["parent_id"] = parent_id
        super(Content, __self__).__init__(
            'sumologic:index/content:Content',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            config: Optional[pulumi.Input[str]] = None,
            parent_id: Optional[pulumi.Input[str]] = None) -> 'Content':
        """
        Get an existing Content resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ContentState.__new__(_ContentState)

        __props__.__dict__["config"] = config
        __props__.__dict__["parent_id"] = parent_id
        return Content(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def config(self) -> pulumi.Output[str]:
        return pulumi.get(self, "config")

    @property
    @pulumi.getter(name="parentId")
    def parent_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "parent_id")

