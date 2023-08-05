# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetVpcInfoResult',
    'AwaitableGetVpcInfoResult',
    'get_vpc_info',
    'get_vpc_info_output',
]

@pulumi.output_type
class GetVpcInfoResult:
    """
    A collection of values returned by getVpcInfo.
    """
    def __init__(__self__, id=None, instance_id=None, name=None, owner_id=None, security_group_id=None, vpc_subnet=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, int):
            raise TypeError("Expected argument 'instance_id' to be a int")
        pulumi.set(__self__, "instance_id", instance_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if security_group_id and not isinstance(security_group_id, str):
            raise TypeError("Expected argument 'security_group_id' to be a str")
        pulumi.set(__self__, "security_group_id", security_group_id)
        if vpc_subnet and not isinstance(vpc_subnet, str):
            raise TypeError("Expected argument 'vpc_subnet' to be a str")
        pulumi.set(__self__, "vpc_subnet", vpc_subnet)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> int:
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter(name="securityGroupId")
    def security_group_id(self) -> str:
        return pulumi.get(self, "security_group_id")

    @property
    @pulumi.getter(name="vpcSubnet")
    def vpc_subnet(self) -> str:
        return pulumi.get(self, "vpc_subnet")


class AwaitableGetVpcInfoResult(GetVpcInfoResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVpcInfoResult(
            id=self.id,
            instance_id=self.instance_id,
            name=self.name,
            owner_id=self.owner_id,
            security_group_id=self.security_group_id,
            vpc_subnet=self.vpc_subnet)


def get_vpc_info(instance_id: Optional[int] = None,
                 opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVpcInfoResult:
    """
    Use this data source to retrieve information about VPC for a CloudAMQP instance.

    Only available for CloudAMQP instances hosted in AWS.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudamqp as cloudamqp

    vpc_info = cloudamqp.get_vpc_info(instance_id=cloudamqp_instance["instance"]["id"])
    ```
    ## Argument reference

    * `instance_id` - (Required) The CloudAMQP instance identifier.

    ## Attributes reference

    All attributes reference are computed

    * `id`                  - The identifier for this resource.
    * `name`                - The name of the CloudAMQP instance.
    * `vpc_subnet`          - Dedicated VPC subnet.
    * `owner_id`            - AWS account identifier.
    * `security_group_id`   - AWS security group identifier.

    ## Dependency

    This data source depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.
    """
    __args__ = dict()
    __args__['instanceId'] = instance_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('cloudamqp:index/getVpcInfo:getVpcInfo', __args__, opts=opts, typ=GetVpcInfoResult).value

    return AwaitableGetVpcInfoResult(
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        name=__ret__.name,
        owner_id=__ret__.owner_id,
        security_group_id=__ret__.security_group_id,
        vpc_subnet=__ret__.vpc_subnet)


@_utilities.lift_output_func(get_vpc_info)
def get_vpc_info_output(instance_id: Optional[pulumi.Input[int]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVpcInfoResult]:
    """
    Use this data source to retrieve information about VPC for a CloudAMQP instance.

    Only available for CloudAMQP instances hosted in AWS.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudamqp as cloudamqp

    vpc_info = cloudamqp.get_vpc_info(instance_id=cloudamqp_instance["instance"]["id"])
    ```
    ## Argument reference

    * `instance_id` - (Required) The CloudAMQP instance identifier.

    ## Attributes reference

    All attributes reference are computed

    * `id`                  - The identifier for this resource.
    * `name`                - The name of the CloudAMQP instance.
    * `vpc_subnet`          - Dedicated VPC subnet.
    * `owner_id`            - AWS account identifier.
    * `security_group_id`   - AWS security group identifier.

    ## Dependency

    This data source depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.
    """
    ...
