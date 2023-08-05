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
    'GetNodesResult',
    'AwaitableGetNodesResult',
    'get_nodes',
    'get_nodes_output',
]

@pulumi.output_type
class GetNodesResult:
    """
    A collection of values returned by getNodes.
    """
    def __init__(__self__, id=None, instance_id=None, nodes=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, int):
            raise TypeError("Expected argument 'instance_id' to be a int")
        pulumi.set(__self__, "instance_id", instance_id)
        if nodes and not isinstance(nodes, list):
            raise TypeError("Expected argument 'nodes' to be a list")
        pulumi.set(__self__, "nodes", nodes)

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
    def nodes(self) -> Sequence['outputs.GetNodesNodeResult']:
        return pulumi.get(self, "nodes")


class AwaitableGetNodesResult(GetNodesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNodesResult(
            id=self.id,
            instance_id=self.instance_id,
            nodes=self.nodes)


def get_nodes(instance_id: Optional[int] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetNodesResult:
    """
    Use this data source to retrieve information about the node(s) created by CloudAMQP instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudamqp as cloudamqp

    nodes = cloudamqp.get_nodes(instance_id=cloudamqp_instance["instance"]["id"])
    ```
    ## Argument reference

    * `instance_id` - (Required) The CloudAMQP instance identifier.

    ## Attributes reference

    All attributes reference are computed

    * `id`    - The identifier for this resource.
    * `nodes` - An array of node information. Each `nodes` block consists of the fields documented below.

    ***

    The `nodes` block consist of

    * `hostname`          - Hostname assigned to the node.
    * `name`              - Name of the node.
    * `running`           - Is the node running?
    * `rabbitmq_version`  - Currently configured Rabbit MQ version on the node.
    * `erlang_version`    - Currently used Erlanbg version on the node.
    * `hipe`              - Enable or disable High-performance Erlang.
    * `configured`        - Is the node configured?

    ## Dependency

    This data source depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.
    """
    __args__ = dict()
    __args__['instanceId'] = instance_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('cloudamqp:index/getNodes:getNodes', __args__, opts=opts, typ=GetNodesResult).value

    return AwaitableGetNodesResult(
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        nodes=__ret__.nodes)


@_utilities.lift_output_func(get_nodes)
def get_nodes_output(instance_id: Optional[pulumi.Input[int]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetNodesResult]:
    """
    Use this data source to retrieve information about the node(s) created by CloudAMQP instance.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudamqp as cloudamqp

    nodes = cloudamqp.get_nodes(instance_id=cloudamqp_instance["instance"]["id"])
    ```
    ## Argument reference

    * `instance_id` - (Required) The CloudAMQP instance identifier.

    ## Attributes reference

    All attributes reference are computed

    * `id`    - The identifier for this resource.
    * `nodes` - An array of node information. Each `nodes` block consists of the fields documented below.

    ***

    The `nodes` block consist of

    * `hostname`          - Hostname assigned to the node.
    * `name`              - Name of the node.
    * `running`           - Is the node running?
    * `rabbitmq_version`  - Currently configured Rabbit MQ version on the node.
    * `erlang_version`    - Currently used Erlanbg version on the node.
    * `hipe`              - Enable or disable High-performance Erlang.
    * `configured`        - Is the node configured?

    ## Dependency

    This data source depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.
    """
    ...
