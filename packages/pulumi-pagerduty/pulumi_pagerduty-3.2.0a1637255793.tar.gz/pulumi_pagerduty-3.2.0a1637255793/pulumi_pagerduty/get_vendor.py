# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetVendorResult',
    'AwaitableGetVendorResult',
    'get_vendor',
    'get_vendor_output',
]

@pulumi.output_type
class GetVendorResult:
    """
    A collection of values returned by getVendor.
    """
    def __init__(__self__, id=None, name=None, type=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The short name of the found vendor.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The generic service type for this vendor.
        """
        return pulumi.get(self, "type")


class AwaitableGetVendorResult(GetVendorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVendorResult(
            id=self.id,
            name=self.name,
            type=self.type)


def get_vendor(name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVendorResult:
    """
    Use this data source to get information about a specific [vendor](https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1vendors/get) that you can use for a service integration (e.g Amazon Cloudwatch, Splunk, Datadog).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    datadog = pagerduty.get_vendor(name="Datadog")
    example_user = pagerduty.User("exampleUser",
        email="125.greenholt.earline@graham.name",
        teams=[pagerduty_team["example"]["id"]])
    foo = pagerduty.EscalationPolicy("foo",
        num_loops=2,
        rules=[pagerduty.EscalationPolicyRuleArgs(
            escalation_delay_in_minutes=10,
            targets=[pagerduty.EscalationPolicyRuleTargetArgs(
                type="user",
                id=example_user.id,
            )],
        )])
    example_service = pagerduty.Service("exampleService",
        auto_resolve_timeout="14400",
        acknowledgement_timeout="600",
        escalation_policy=pagerduty_escalation_policy["example"]["id"])
    example_service_integration = pagerduty.ServiceIntegration("exampleServiceIntegration",
        vendor=datadog.id,
        service=example_service.id,
        type="generic_events_api_inbound_integration")
    ```


    :param str name: The vendor name to use to find a vendor in the PagerDuty API.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('pagerduty:index/getVendor:getVendor', __args__, opts=opts, typ=GetVendorResult).value

    return AwaitableGetVendorResult(
        id=__ret__.id,
        name=__ret__.name,
        type=__ret__.type)


@_utilities.lift_output_func(get_vendor)
def get_vendor_output(name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVendorResult]:
    """
    Use this data source to get information about a specific [vendor](https://developer.pagerduty.com/api-reference/reference/REST/openapiv3.json/paths/~1vendors/get) that you can use for a service integration (e.g Amazon Cloudwatch, Splunk, Datadog).

    ## Example Usage

    ```python
    import pulumi
    import pulumi_pagerduty as pagerduty

    datadog = pagerduty.get_vendor(name="Datadog")
    example_user = pagerduty.User("exampleUser",
        email="125.greenholt.earline@graham.name",
        teams=[pagerduty_team["example"]["id"]])
    foo = pagerduty.EscalationPolicy("foo",
        num_loops=2,
        rules=[pagerduty.EscalationPolicyRuleArgs(
            escalation_delay_in_minutes=10,
            targets=[pagerduty.EscalationPolicyRuleTargetArgs(
                type="user",
                id=example_user.id,
            )],
        )])
    example_service = pagerduty.Service("exampleService",
        auto_resolve_timeout="14400",
        acknowledgement_timeout="600",
        escalation_policy=pagerduty_escalation_policy["example"]["id"])
    example_service_integration = pagerduty.ServiceIntegration("exampleServiceIntegration",
        vendor=datadog.id,
        service=example_service.id,
        type="generic_events_api_inbound_integration")
    ```


    :param str name: The vendor name to use to find a vendor in the PagerDuty API.
    """
    ...
