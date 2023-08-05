# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['LogsIndexOrderArgs', 'LogsIndexOrder']

@pulumi.input_type
class LogsIndexOrderArgs:
    def __init__(__self__, *,
                 indexes: pulumi.Input[Sequence[pulumi.Input[str]]],
                 name: pulumi.Input[str]):
        """
        The set of arguments for constructing a LogsIndexOrder resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] indexes: The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        :param pulumi.Input[str] name: The unique name of the index order resource.
        """
        pulumi.set(__self__, "indexes", indexes)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def indexes(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        """
        return pulumi.get(self, "indexes")

    @indexes.setter
    def indexes(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "indexes", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The unique name of the index order resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _LogsIndexOrderState:
    def __init__(__self__, *,
                 indexes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering LogsIndexOrder resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] indexes: The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        :param pulumi.Input[str] name: The unique name of the index order resource.
        """
        if indexes is not None:
            pulumi.set(__self__, "indexes", indexes)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def indexes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        """
        return pulumi.get(self, "indexes")

    @indexes.setter
    def indexes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "indexes", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The unique name of the index order resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


class LogsIndexOrder(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 indexes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Datadog Logs Index API resource. This can be used to manage the order of Datadog logs indexes.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        sample_index_order = datadog.LogsIndexOrder("sampleIndexOrder",
            name="sample_index_order",
            indexes=[datadog_logs_index["sample_index"]["id"]],
            opts=pulumi.ResourceOptions(depends_on=["datadog_logs_index.sample_index"]))
        ```

        ## Import

        # The Datadog Terraform Provider does not support the creation and deletion of index orders. There must be at most one `datadog_logs_index_order` resource

        ```sh
         $ pulumi import datadog:index/logsIndexOrder:LogsIndexOrder name> <name>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] indexes: The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        :param pulumi.Input[str] name: The unique name of the index order resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: LogsIndexOrderArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog Logs Index API resource. This can be used to manage the order of Datadog logs indexes.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        sample_index_order = datadog.LogsIndexOrder("sampleIndexOrder",
            name="sample_index_order",
            indexes=[datadog_logs_index["sample_index"]["id"]],
            opts=pulumi.ResourceOptions(depends_on=["datadog_logs_index.sample_index"]))
        ```

        ## Import

        # The Datadog Terraform Provider does not support the creation and deletion of index orders. There must be at most one `datadog_logs_index_order` resource

        ```sh
         $ pulumi import datadog:index/logsIndexOrder:LogsIndexOrder name> <name>
        ```

        :param str resource_name: The name of the resource.
        :param LogsIndexOrderArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(LogsIndexOrderArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 indexes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
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
            __props__ = LogsIndexOrderArgs.__new__(LogsIndexOrderArgs)

            if indexes is None and not opts.urn:
                raise TypeError("Missing required property 'indexes'")
            __props__.__dict__["indexes"] = indexes
            if name is None and not opts.urn:
                raise TypeError("Missing required property 'name'")
            __props__.__dict__["name"] = name
        super(LogsIndexOrder, __self__).__init__(
            'datadog:index/logsIndexOrder:LogsIndexOrder',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            indexes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            name: Optional[pulumi.Input[str]] = None) -> 'LogsIndexOrder':
        """
        Get an existing LogsIndexOrder resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] indexes: The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        :param pulumi.Input[str] name: The unique name of the index order resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _LogsIndexOrderState.__new__(_LogsIndexOrderState)

        __props__.__dict__["indexes"] = indexes
        __props__.__dict__["name"] = name
        return LogsIndexOrder(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def indexes(self) -> pulumi.Output[Sequence[str]]:
        """
        The index resource list. Logs are tested against the query filter of each index one by one following the order of the list.
        """
        return pulumi.get(self, "indexes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The unique name of the index order resource.
        """
        return pulumi.get(self, "name")

