# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['MetricTagConfigurationArgs', 'MetricTagConfiguration']

@pulumi.input_type
class MetricTagConfigurationArgs:
    def __init__(__self__, *,
                 metric_name: pulumi.Input[str],
                 metric_type: pulumi.Input[str],
                 tags: pulumi.Input[Sequence[pulumi.Input[str]]],
                 include_percentiles: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a MetricTagConfiguration resource.
        :param pulumi.Input[str] metric_name: The metric name for this resource.
        :param pulumi.Input[str] metric_type: The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag keys that will be queryable for your metric.
        :param pulumi.Input[bool] include_percentiles: Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        """
        pulumi.set(__self__, "metric_name", metric_name)
        pulumi.set(__self__, "metric_type", metric_type)
        pulumi.set(__self__, "tags", tags)
        if include_percentiles is not None:
            pulumi.set(__self__, "include_percentiles", include_percentiles)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> pulumi.Input[str]:
        """
        The metric name for this resource.
        """
        return pulumi.get(self, "metric_name")

    @metric_name.setter
    def metric_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "metric_name", value)

    @property
    @pulumi.getter(name="metricType")
    def metric_type(self) -> pulumi.Input[str]:
        """
        The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        """
        return pulumi.get(self, "metric_type")

    @metric_type.setter
    def metric_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "metric_type", value)

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        A list of tag keys that will be queryable for your metric.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="includePercentiles")
    def include_percentiles(self) -> Optional[pulumi.Input[bool]]:
        """
        Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        """
        return pulumi.get(self, "include_percentiles")

    @include_percentiles.setter
    def include_percentiles(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_percentiles", value)


@pulumi.input_type
class _MetricTagConfigurationState:
    def __init__(__self__, *,
                 include_percentiles: Optional[pulumi.Input[bool]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 metric_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering MetricTagConfiguration resources.
        :param pulumi.Input[bool] include_percentiles: Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        :param pulumi.Input[str] metric_name: The metric name for this resource.
        :param pulumi.Input[str] metric_type: The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag keys that will be queryable for your metric.
        """
        if include_percentiles is not None:
            pulumi.set(__self__, "include_percentiles", include_percentiles)
        if metric_name is not None:
            pulumi.set(__self__, "metric_name", metric_name)
        if metric_type is not None:
            pulumi.set(__self__, "metric_type", metric_type)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="includePercentiles")
    def include_percentiles(self) -> Optional[pulumi.Input[bool]]:
        """
        Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        """
        return pulumi.get(self, "include_percentiles")

    @include_percentiles.setter
    def include_percentiles(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_percentiles", value)

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> Optional[pulumi.Input[str]]:
        """
        The metric name for this resource.
        """
        return pulumi.get(self, "metric_name")

    @metric_name.setter
    def metric_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_name", value)

    @property
    @pulumi.getter(name="metricType")
    def metric_type(self) -> Optional[pulumi.Input[str]]:
        """
        The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        """
        return pulumi.get(self, "metric_type")

    @metric_type.setter
    def metric_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "metric_type", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of tag keys that will be queryable for your metric.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


class MetricTagConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 include_percentiles: Optional[pulumi.Input[bool]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 metric_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a Datadog metric tag configuration resource. This can be used to modify tag configurations for metrics.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Manage a tag configuration for a Datadog distribution metric with/without percentiles
        example_dist_metric = datadog.MetricTagConfiguration("exampleDistMetric",
            include_percentiles=False,
            metric_name="example.terraform.dist.metric",
            metric_type="distribution",
            tags=[
                "sport",
                "datacenter",
            ])
        # Manage tag configurations for a Datadog count or gauge metric
        example_count_metric = datadog.MetricTagConfiguration("exampleCountMetric",
            metric_name="example.terraform.count.metric",
            metric_type="count",
            tags=[
                "sport",
                "datacenter",
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] include_percentiles: Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        :param pulumi.Input[str] metric_name: The metric name for this resource.
        :param pulumi.Input[str] metric_type: The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag keys that will be queryable for your metric.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MetricTagConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Datadog metric tag configuration resource. This can be used to modify tag configurations for metrics.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_datadog as datadog

        # Manage a tag configuration for a Datadog distribution metric with/without percentiles
        example_dist_metric = datadog.MetricTagConfiguration("exampleDistMetric",
            include_percentiles=False,
            metric_name="example.terraform.dist.metric",
            metric_type="distribution",
            tags=[
                "sport",
                "datacenter",
            ])
        # Manage tag configurations for a Datadog count or gauge metric
        example_count_metric = datadog.MetricTagConfiguration("exampleCountMetric",
            metric_name="example.terraform.count.metric",
            metric_type="count",
            tags=[
                "sport",
                "datacenter",
            ])
        ```

        :param str resource_name: The name of the resource.
        :param MetricTagConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MetricTagConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 include_percentiles: Optional[pulumi.Input[bool]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 metric_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
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
            __props__ = MetricTagConfigurationArgs.__new__(MetricTagConfigurationArgs)

            __props__.__dict__["include_percentiles"] = include_percentiles
            if metric_name is None and not opts.urn:
                raise TypeError("Missing required property 'metric_name'")
            __props__.__dict__["metric_name"] = metric_name
            if metric_type is None and not opts.urn:
                raise TypeError("Missing required property 'metric_type'")
            __props__.__dict__["metric_type"] = metric_type
            if tags is None and not opts.urn:
                raise TypeError("Missing required property 'tags'")
            __props__.__dict__["tags"] = tags
        super(MetricTagConfiguration, __self__).__init__(
            'datadog:index/metricTagConfiguration:MetricTagConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            include_percentiles: Optional[pulumi.Input[bool]] = None,
            metric_name: Optional[pulumi.Input[str]] = None,
            metric_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None) -> 'MetricTagConfiguration':
        """
        Get an existing MetricTagConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] include_percentiles: Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        :param pulumi.Input[str] metric_name: The metric name for this resource.
        :param pulumi.Input[str] metric_type: The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] tags: A list of tag keys that will be queryable for your metric.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MetricTagConfigurationState.__new__(_MetricTagConfigurationState)

        __props__.__dict__["include_percentiles"] = include_percentiles
        __props__.__dict__["metric_name"] = metric_name
        __props__.__dict__["metric_type"] = metric_type
        __props__.__dict__["tags"] = tags
        return MetricTagConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="includePercentiles")
    def include_percentiles(self) -> pulumi.Output[Optional[bool]]:
        """
        Toggle to include/exclude percentiles for a distribution metric. Defaults to false. Can only be applied to metrics that have a metric_type of distribution.
        """
        return pulumi.get(self, "include_percentiles")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> pulumi.Output[str]:
        """
        The metric name for this resource.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter(name="metricType")
    def metric_type(self) -> pulumi.Output[str]:
        """
        The metric's type. This field can't be updated after creation. Valid values are `gauge`, `count`, `rate`, `distribution`.
        """
        return pulumi.get(self, "metric_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Sequence[str]]:
        """
        A list of tag keys that will be queryable for your metric.
        """
        return pulumi.get(self, "tags")

