# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['CseAggregationRuleArgs', 'CseAggregationRule']

@pulumi.input_type
class CseAggregationRuleArgs:
    def __init__(__self__, *,
                 aggregation_functions: pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleAggregationFunctionArgs']]],
                 description_expression: pulumi.Input[str],
                 enabled: pulumi.Input[bool],
                 entity_selectors: pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleEntitySelectorArgs']]],
                 match_expression: pulumi.Input[str],
                 name_expression: pulumi.Input[str],
                 severity_mapping: pulumi.Input['CseAggregationRuleSeverityMappingArgs'],
                 trigger_expression: pulumi.Input[str],
                 window_size: pulumi.Input[str],
                 group_by_entity: Optional[pulumi.Input[bool]] = None,
                 group_by_fields: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 is_prototype: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 summary_expression: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a CseAggregationRule resource.
        """
        pulumi.set(__self__, "aggregation_functions", aggregation_functions)
        pulumi.set(__self__, "description_expression", description_expression)
        pulumi.set(__self__, "enabled", enabled)
        pulumi.set(__self__, "entity_selectors", entity_selectors)
        pulumi.set(__self__, "match_expression", match_expression)
        pulumi.set(__self__, "name_expression", name_expression)
        pulumi.set(__self__, "severity_mapping", severity_mapping)
        pulumi.set(__self__, "trigger_expression", trigger_expression)
        pulumi.set(__self__, "window_size", window_size)
        if group_by_entity is not None:
            pulumi.set(__self__, "group_by_entity", group_by_entity)
        if group_by_fields is not None:
            pulumi.set(__self__, "group_by_fields", group_by_fields)
        if is_prototype is not None:
            pulumi.set(__self__, "is_prototype", is_prototype)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if summary_expression is not None:
            pulumi.set(__self__, "summary_expression", summary_expression)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="aggregationFunctions")
    def aggregation_functions(self) -> pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleAggregationFunctionArgs']]]:
        return pulumi.get(self, "aggregation_functions")

    @aggregation_functions.setter
    def aggregation_functions(self, value: pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleAggregationFunctionArgs']]]):
        pulumi.set(self, "aggregation_functions", value)

    @property
    @pulumi.getter(name="descriptionExpression")
    def description_expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "description_expression")

    @description_expression.setter
    def description_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "description_expression", value)

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Input[bool]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: pulumi.Input[bool]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="entitySelectors")
    def entity_selectors(self) -> pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleEntitySelectorArgs']]]:
        return pulumi.get(self, "entity_selectors")

    @entity_selectors.setter
    def entity_selectors(self, value: pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleEntitySelectorArgs']]]):
        pulumi.set(self, "entity_selectors", value)

    @property
    @pulumi.getter(name="matchExpression")
    def match_expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "match_expression")

    @match_expression.setter
    def match_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "match_expression", value)

    @property
    @pulumi.getter(name="nameExpression")
    def name_expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "name_expression")

    @name_expression.setter
    def name_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "name_expression", value)

    @property
    @pulumi.getter(name="severityMapping")
    def severity_mapping(self) -> pulumi.Input['CseAggregationRuleSeverityMappingArgs']:
        return pulumi.get(self, "severity_mapping")

    @severity_mapping.setter
    def severity_mapping(self, value: pulumi.Input['CseAggregationRuleSeverityMappingArgs']):
        pulumi.set(self, "severity_mapping", value)

    @property
    @pulumi.getter(name="triggerExpression")
    def trigger_expression(self) -> pulumi.Input[str]:
        return pulumi.get(self, "trigger_expression")

    @trigger_expression.setter
    def trigger_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "trigger_expression", value)

    @property
    @pulumi.getter(name="windowSize")
    def window_size(self) -> pulumi.Input[str]:
        return pulumi.get(self, "window_size")

    @window_size.setter
    def window_size(self, value: pulumi.Input[str]):
        pulumi.set(self, "window_size", value)

    @property
    @pulumi.getter(name="groupByEntity")
    def group_by_entity(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "group_by_entity")

    @group_by_entity.setter
    def group_by_entity(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "group_by_entity", value)

    @property
    @pulumi.getter(name="groupByFields")
    def group_by_fields(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "group_by_fields")

    @group_by_fields.setter
    def group_by_fields(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "group_by_fields", value)

    @property
    @pulumi.getter(name="isPrototype")
    def is_prototype(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_prototype")

    @is_prototype.setter
    def is_prototype(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_prototype", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="summaryExpression")
    def summary_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "summary_expression")

    @summary_expression.setter
    def summary_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "summary_expression", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _CseAggregationRuleState:
    def __init__(__self__, *,
                 aggregation_functions: Optional[pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleAggregationFunctionArgs']]]] = None,
                 description_expression: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 entity_selectors: Optional[pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleEntitySelectorArgs']]]] = None,
                 group_by_entity: Optional[pulumi.Input[bool]] = None,
                 group_by_fields: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 is_prototype: Optional[pulumi.Input[bool]] = None,
                 match_expression: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_expression: Optional[pulumi.Input[str]] = None,
                 severity_mapping: Optional[pulumi.Input['CseAggregationRuleSeverityMappingArgs']] = None,
                 summary_expression: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 trigger_expression: Optional[pulumi.Input[str]] = None,
                 window_size: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering CseAggregationRule resources.
        """
        if aggregation_functions is not None:
            pulumi.set(__self__, "aggregation_functions", aggregation_functions)
        if description_expression is not None:
            pulumi.set(__self__, "description_expression", description_expression)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if entity_selectors is not None:
            pulumi.set(__self__, "entity_selectors", entity_selectors)
        if group_by_entity is not None:
            pulumi.set(__self__, "group_by_entity", group_by_entity)
        if group_by_fields is not None:
            pulumi.set(__self__, "group_by_fields", group_by_fields)
        if is_prototype is not None:
            pulumi.set(__self__, "is_prototype", is_prototype)
        if match_expression is not None:
            pulumi.set(__self__, "match_expression", match_expression)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_expression is not None:
            pulumi.set(__self__, "name_expression", name_expression)
        if severity_mapping is not None:
            pulumi.set(__self__, "severity_mapping", severity_mapping)
        if summary_expression is not None:
            pulumi.set(__self__, "summary_expression", summary_expression)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if trigger_expression is not None:
            pulumi.set(__self__, "trigger_expression", trigger_expression)
        if window_size is not None:
            pulumi.set(__self__, "window_size", window_size)

    @property
    @pulumi.getter(name="aggregationFunctions")
    def aggregation_functions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleAggregationFunctionArgs']]]]:
        return pulumi.get(self, "aggregation_functions")

    @aggregation_functions.setter
    def aggregation_functions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleAggregationFunctionArgs']]]]):
        pulumi.set(self, "aggregation_functions", value)

    @property
    @pulumi.getter(name="descriptionExpression")
    def description_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "description_expression")

    @description_expression.setter
    def description_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description_expression", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="entitySelectors")
    def entity_selectors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleEntitySelectorArgs']]]]:
        return pulumi.get(self, "entity_selectors")

    @entity_selectors.setter
    def entity_selectors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['CseAggregationRuleEntitySelectorArgs']]]]):
        pulumi.set(self, "entity_selectors", value)

    @property
    @pulumi.getter(name="groupByEntity")
    def group_by_entity(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "group_by_entity")

    @group_by_entity.setter
    def group_by_entity(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "group_by_entity", value)

    @property
    @pulumi.getter(name="groupByFields")
    def group_by_fields(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "group_by_fields")

    @group_by_fields.setter
    def group_by_fields(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "group_by_fields", value)

    @property
    @pulumi.getter(name="isPrototype")
    def is_prototype(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "is_prototype")

    @is_prototype.setter
    def is_prototype(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_prototype", value)

    @property
    @pulumi.getter(name="matchExpression")
    def match_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "match_expression")

    @match_expression.setter
    def match_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "match_expression", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="nameExpression")
    def name_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "name_expression")

    @name_expression.setter
    def name_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_expression", value)

    @property
    @pulumi.getter(name="severityMapping")
    def severity_mapping(self) -> Optional[pulumi.Input['CseAggregationRuleSeverityMappingArgs']]:
        return pulumi.get(self, "severity_mapping")

    @severity_mapping.setter
    def severity_mapping(self, value: Optional[pulumi.Input['CseAggregationRuleSeverityMappingArgs']]):
        pulumi.set(self, "severity_mapping", value)

    @property
    @pulumi.getter(name="summaryExpression")
    def summary_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "summary_expression")

    @summary_expression.setter
    def summary_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "summary_expression", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="triggerExpression")
    def trigger_expression(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "trigger_expression")

    @trigger_expression.setter
    def trigger_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "trigger_expression", value)

    @property
    @pulumi.getter(name="windowSize")
    def window_size(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "window_size")

    @window_size.setter
    def window_size(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "window_size", value)


class CseAggregationRule(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aggregation_functions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CseAggregationRuleAggregationFunctionArgs']]]]] = None,
                 description_expression: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 entity_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CseAggregationRuleEntitySelectorArgs']]]]] = None,
                 group_by_entity: Optional[pulumi.Input[bool]] = None,
                 group_by_fields: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 is_prototype: Optional[pulumi.Input[bool]] = None,
                 match_expression: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_expression: Optional[pulumi.Input[str]] = None,
                 severity_mapping: Optional[pulumi.Input[pulumi.InputType['CseAggregationRuleSeverityMappingArgs']]] = None,
                 summary_expression: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 trigger_expression: Optional[pulumi.Input[str]] = None,
                 window_size: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Sumo Logic CSE [Aggregation Rule](https://help.sumologic.com/Cloud_SIEM_Enterprise/CSE_Rules/09_Write_an_Aggregation_Rule).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        aggregation_rule = sumologic.CseAggregationRule("aggregationRule",
            aggregation_functions=[sumologic.CseAggregationRuleAggregationFunctionArgs(
                arguments=["metadata_deviceEventId"],
                function="count_distinct",
                name="distinct_eventid_count",
            )],
            description_expression="Signal description",
            enabled=True,
            entity_selectors=[sumologic.CseAggregationRuleEntitySelectorArgs(
                entity_type="_ip",
                expression="srcDevice_ip",
            )],
            group_by_entity=True,
            group_by_fields=["dstDevice_hostname"],
            is_prototype=False,
            match_expression="objectType = \"Network\"",
            name_expression="Signal name",
            severity_mapping=sumologic.CseAggregationRuleSeverityMappingArgs(
                default=5,
                type="constant",
            ),
            summary_expression="Signal summary",
            tags=["_mitreAttackTactic:TA0009"],
            trigger_expression="distinct_eventid_count > 5",
            window_size="T30M")
        ```
        ## Argument reference

        The following arguments are supported:

        - `aggregation_functions` - (Required) One or more named aggregation functions
          + `name` - (Required) The name to use to reference the result in the trigger_expression
          + `function` - (Required) The function to aggregate with
          + `arguments` - (Required) One or more expressions to pass as arguments to the function
        - `description_expression` - (Required) The description of the generated Signals
        - `enabled` - (Required) Whether the rule should generate Signals
        - `entity_selectors` - (Required) The entities to generate Signals on
          + `entityType` - (Required) The type of the entity to generate the Signal on.
          + `expression` - (Required) The expression or field name to generate the Signal on.
        - `group_by_entity` - (Optional; defaults to true) Whether to group records by the specified entity fields
        - `group_by_fields` - (Optional) A list of fields to group records by
        - `is_prototype` - (Optional) Whether the generated Signals should be prototype Signals
        - `match_expression` - (Required) The expression for which records to match on
        - `name` - (Required) The name of the Rule
        - `name_expression` - (Required) The name of the generated Signals
        - `severity_mapping` - (Required) The configuration of how the severity of the Signals should be mapped from the Records
          + `type` - (Required) Whether to set a constant severity ("constant"), set the severity based on the direct value of a record field ("fieldValue"), or map a record field value to a severity ("fieldValueMapping").
          + `default` - (Optional) The severity to use in the "constant" case or to fall back to if the field used by "fieldValue"/"fieldValueMapping" is not populated.
          + `field` - (Optional) The field to use in the "fieldValue"/"fieldValueMapping" cases.
          + `mapping` - (Optional) The map of record values to severities to use in the "fieldValueMapping" case
            - `type` - (Required) Must be set to "eq" currently
            - `from` - (Required) The record value to map from
            - `to` - (Required) The severity value to map to
        - `summary_expression` - (Optional) The summary of the generated Signals
        - `tags` - (Required) The tags of the generated Signals
        - `trigger_expression` - (Required) The expression to determine whether a Signal should be created based on the aggregation results
        - `window_size` - (Required) How long of a window to aggregate records for. Current acceptable values are T05M, T10M, T30M, T60M, T24H, T12H, or T05D.

        The following attributes are exported:

        - `id` - The internal ID of the aggregation rule.

        ## Import

        Aggregation Rules can be imported using the field id, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/cseAggregationRule:CseAggregationRule aggregation_rule id
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: CseAggregationRuleArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Sumo Logic CSE [Aggregation Rule](https://help.sumologic.com/Cloud_SIEM_Enterprise/CSE_Rules/09_Write_an_Aggregation_Rule).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_sumologic as sumologic

        aggregation_rule = sumologic.CseAggregationRule("aggregationRule",
            aggregation_functions=[sumologic.CseAggregationRuleAggregationFunctionArgs(
                arguments=["metadata_deviceEventId"],
                function="count_distinct",
                name="distinct_eventid_count",
            )],
            description_expression="Signal description",
            enabled=True,
            entity_selectors=[sumologic.CseAggregationRuleEntitySelectorArgs(
                entity_type="_ip",
                expression="srcDevice_ip",
            )],
            group_by_entity=True,
            group_by_fields=["dstDevice_hostname"],
            is_prototype=False,
            match_expression="objectType = \"Network\"",
            name_expression="Signal name",
            severity_mapping=sumologic.CseAggregationRuleSeverityMappingArgs(
                default=5,
                type="constant",
            ),
            summary_expression="Signal summary",
            tags=["_mitreAttackTactic:TA0009"],
            trigger_expression="distinct_eventid_count > 5",
            window_size="T30M")
        ```
        ## Argument reference

        The following arguments are supported:

        - `aggregation_functions` - (Required) One or more named aggregation functions
          + `name` - (Required) The name to use to reference the result in the trigger_expression
          + `function` - (Required) The function to aggregate with
          + `arguments` - (Required) One or more expressions to pass as arguments to the function
        - `description_expression` - (Required) The description of the generated Signals
        - `enabled` - (Required) Whether the rule should generate Signals
        - `entity_selectors` - (Required) The entities to generate Signals on
          + `entityType` - (Required) The type of the entity to generate the Signal on.
          + `expression` - (Required) The expression or field name to generate the Signal on.
        - `group_by_entity` - (Optional; defaults to true) Whether to group records by the specified entity fields
        - `group_by_fields` - (Optional) A list of fields to group records by
        - `is_prototype` - (Optional) Whether the generated Signals should be prototype Signals
        - `match_expression` - (Required) The expression for which records to match on
        - `name` - (Required) The name of the Rule
        - `name_expression` - (Required) The name of the generated Signals
        - `severity_mapping` - (Required) The configuration of how the severity of the Signals should be mapped from the Records
          + `type` - (Required) Whether to set a constant severity ("constant"), set the severity based on the direct value of a record field ("fieldValue"), or map a record field value to a severity ("fieldValueMapping").
          + `default` - (Optional) The severity to use in the "constant" case or to fall back to if the field used by "fieldValue"/"fieldValueMapping" is not populated.
          + `field` - (Optional) The field to use in the "fieldValue"/"fieldValueMapping" cases.
          + `mapping` - (Optional) The map of record values to severities to use in the "fieldValueMapping" case
            - `type` - (Required) Must be set to "eq" currently
            - `from` - (Required) The record value to map from
            - `to` - (Required) The severity value to map to
        - `summary_expression` - (Optional) The summary of the generated Signals
        - `tags` - (Required) The tags of the generated Signals
        - `trigger_expression` - (Required) The expression to determine whether a Signal should be created based on the aggregation results
        - `window_size` - (Required) How long of a window to aggregate records for. Current acceptable values are T05M, T10M, T30M, T60M, T24H, T12H, or T05D.

        The following attributes are exported:

        - `id` - The internal ID of the aggregation rule.

        ## Import

        Aggregation Rules can be imported using the field id, e.g.hcl

        ```sh
         $ pulumi import sumologic:index/cseAggregationRule:CseAggregationRule aggregation_rule id
        ```

        :param str resource_name: The name of the resource.
        :param CseAggregationRuleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(CseAggregationRuleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 aggregation_functions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CseAggregationRuleAggregationFunctionArgs']]]]] = None,
                 description_expression: Optional[pulumi.Input[str]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 entity_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CseAggregationRuleEntitySelectorArgs']]]]] = None,
                 group_by_entity: Optional[pulumi.Input[bool]] = None,
                 group_by_fields: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 is_prototype: Optional[pulumi.Input[bool]] = None,
                 match_expression: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_expression: Optional[pulumi.Input[str]] = None,
                 severity_mapping: Optional[pulumi.Input[pulumi.InputType['CseAggregationRuleSeverityMappingArgs']]] = None,
                 summary_expression: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 trigger_expression: Optional[pulumi.Input[str]] = None,
                 window_size: Optional[pulumi.Input[str]] = None,
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
            __props__ = CseAggregationRuleArgs.__new__(CseAggregationRuleArgs)

            if aggregation_functions is None and not opts.urn:
                raise TypeError("Missing required property 'aggregation_functions'")
            __props__.__dict__["aggregation_functions"] = aggregation_functions
            if description_expression is None and not opts.urn:
                raise TypeError("Missing required property 'description_expression'")
            __props__.__dict__["description_expression"] = description_expression
            if enabled is None and not opts.urn:
                raise TypeError("Missing required property 'enabled'")
            __props__.__dict__["enabled"] = enabled
            if entity_selectors is None and not opts.urn:
                raise TypeError("Missing required property 'entity_selectors'")
            __props__.__dict__["entity_selectors"] = entity_selectors
            __props__.__dict__["group_by_entity"] = group_by_entity
            __props__.__dict__["group_by_fields"] = group_by_fields
            __props__.__dict__["is_prototype"] = is_prototype
            if match_expression is None and not opts.urn:
                raise TypeError("Missing required property 'match_expression'")
            __props__.__dict__["match_expression"] = match_expression
            __props__.__dict__["name"] = name
            if name_expression is None and not opts.urn:
                raise TypeError("Missing required property 'name_expression'")
            __props__.__dict__["name_expression"] = name_expression
            if severity_mapping is None and not opts.urn:
                raise TypeError("Missing required property 'severity_mapping'")
            __props__.__dict__["severity_mapping"] = severity_mapping
            __props__.__dict__["summary_expression"] = summary_expression
            __props__.__dict__["tags"] = tags
            if trigger_expression is None and not opts.urn:
                raise TypeError("Missing required property 'trigger_expression'")
            __props__.__dict__["trigger_expression"] = trigger_expression
            if window_size is None and not opts.urn:
                raise TypeError("Missing required property 'window_size'")
            __props__.__dict__["window_size"] = window_size
        super(CseAggregationRule, __self__).__init__(
            'sumologic:index/cseAggregationRule:CseAggregationRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            aggregation_functions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CseAggregationRuleAggregationFunctionArgs']]]]] = None,
            description_expression: Optional[pulumi.Input[str]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            entity_selectors: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['CseAggregationRuleEntitySelectorArgs']]]]] = None,
            group_by_entity: Optional[pulumi.Input[bool]] = None,
            group_by_fields: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            is_prototype: Optional[pulumi.Input[bool]] = None,
            match_expression: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            name_expression: Optional[pulumi.Input[str]] = None,
            severity_mapping: Optional[pulumi.Input[pulumi.InputType['CseAggregationRuleSeverityMappingArgs']]] = None,
            summary_expression: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            trigger_expression: Optional[pulumi.Input[str]] = None,
            window_size: Optional[pulumi.Input[str]] = None) -> 'CseAggregationRule':
        """
        Get an existing CseAggregationRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _CseAggregationRuleState.__new__(_CseAggregationRuleState)

        __props__.__dict__["aggregation_functions"] = aggregation_functions
        __props__.__dict__["description_expression"] = description_expression
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["entity_selectors"] = entity_selectors
        __props__.__dict__["group_by_entity"] = group_by_entity
        __props__.__dict__["group_by_fields"] = group_by_fields
        __props__.__dict__["is_prototype"] = is_prototype
        __props__.__dict__["match_expression"] = match_expression
        __props__.__dict__["name"] = name
        __props__.__dict__["name_expression"] = name_expression
        __props__.__dict__["severity_mapping"] = severity_mapping
        __props__.__dict__["summary_expression"] = summary_expression
        __props__.__dict__["tags"] = tags
        __props__.__dict__["trigger_expression"] = trigger_expression
        __props__.__dict__["window_size"] = window_size
        return CseAggregationRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="aggregationFunctions")
    def aggregation_functions(self) -> pulumi.Output[Sequence['outputs.CseAggregationRuleAggregationFunction']]:
        return pulumi.get(self, "aggregation_functions")

    @property
    @pulumi.getter(name="descriptionExpression")
    def description_expression(self) -> pulumi.Output[str]:
        return pulumi.get(self, "description_expression")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="entitySelectors")
    def entity_selectors(self) -> pulumi.Output[Sequence['outputs.CseAggregationRuleEntitySelector']]:
        return pulumi.get(self, "entity_selectors")

    @property
    @pulumi.getter(name="groupByEntity")
    def group_by_entity(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "group_by_entity")

    @property
    @pulumi.getter(name="groupByFields")
    def group_by_fields(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "group_by_fields")

    @property
    @pulumi.getter(name="isPrototype")
    def is_prototype(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "is_prototype")

    @property
    @pulumi.getter(name="matchExpression")
    def match_expression(self) -> pulumi.Output[str]:
        return pulumi.get(self, "match_expression")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nameExpression")
    def name_expression(self) -> pulumi.Output[str]:
        return pulumi.get(self, "name_expression")

    @property
    @pulumi.getter(name="severityMapping")
    def severity_mapping(self) -> pulumi.Output['outputs.CseAggregationRuleSeverityMapping']:
        return pulumi.get(self, "severity_mapping")

    @property
    @pulumi.getter(name="summaryExpression")
    def summary_expression(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "summary_expression")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence[str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="triggerExpression")
    def trigger_expression(self) -> pulumi.Output[str]:
        return pulumi.get(self, "trigger_expression")

    @property
    @pulumi.getter(name="windowSize")
    def window_size(self) -> pulumi.Output[str]:
        return pulumi.get(self, "window_size")

