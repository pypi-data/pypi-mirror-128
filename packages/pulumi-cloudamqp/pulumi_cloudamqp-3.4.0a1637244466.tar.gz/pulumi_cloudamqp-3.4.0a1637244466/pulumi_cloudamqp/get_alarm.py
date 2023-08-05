# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetAlarmResult',
    'AwaitableGetAlarmResult',
    'get_alarm',
    'get_alarm_output',
]

@pulumi.output_type
class GetAlarmResult:
    """
    A collection of values returned by getAlarm.
    """
    def __init__(__self__, alarm_id=None, enabled=None, id=None, instance_id=None, message_type=None, queue_regex=None, recipients=None, time_threshold=None, type=None, value_threshold=None, vhost_regex=None):
        if alarm_id and not isinstance(alarm_id, int):
            raise TypeError("Expected argument 'alarm_id' to be a int")
        pulumi.set(__self__, "alarm_id", alarm_id)
        if enabled and not isinstance(enabled, bool):
            raise TypeError("Expected argument 'enabled' to be a bool")
        pulumi.set(__self__, "enabled", enabled)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, int):
            raise TypeError("Expected argument 'instance_id' to be a int")
        pulumi.set(__self__, "instance_id", instance_id)
        if message_type and not isinstance(message_type, str):
            raise TypeError("Expected argument 'message_type' to be a str")
        pulumi.set(__self__, "message_type", message_type)
        if queue_regex and not isinstance(queue_regex, str):
            raise TypeError("Expected argument 'queue_regex' to be a str")
        pulumi.set(__self__, "queue_regex", queue_regex)
        if recipients and not isinstance(recipients, list):
            raise TypeError("Expected argument 'recipients' to be a list")
        pulumi.set(__self__, "recipients", recipients)
        if time_threshold and not isinstance(time_threshold, int):
            raise TypeError("Expected argument 'time_threshold' to be a int")
        pulumi.set(__self__, "time_threshold", time_threshold)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if value_threshold and not isinstance(value_threshold, int):
            raise TypeError("Expected argument 'value_threshold' to be a int")
        pulumi.set(__self__, "value_threshold", value_threshold)
        if vhost_regex and not isinstance(vhost_regex, str):
            raise TypeError("Expected argument 'vhost_regex' to be a str")
        pulumi.set(__self__, "vhost_regex", vhost_regex)

    @property
    @pulumi.getter(name="alarmId")
    def alarm_id(self) -> Optional[int]:
        return pulumi.get(self, "alarm_id")

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        return pulumi.get(self, "enabled")

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
    @pulumi.getter(name="messageType")
    def message_type(self) -> str:
        return pulumi.get(self, "message_type")

    @property
    @pulumi.getter(name="queueRegex")
    def queue_regex(self) -> str:
        return pulumi.get(self, "queue_regex")

    @property
    @pulumi.getter
    def recipients(self) -> Sequence[int]:
        return pulumi.get(self, "recipients")

    @property
    @pulumi.getter(name="timeThreshold")
    def time_threshold(self) -> int:
        return pulumi.get(self, "time_threshold")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="valueThreshold")
    def value_threshold(self) -> int:
        return pulumi.get(self, "value_threshold")

    @property
    @pulumi.getter(name="vhostRegex")
    def vhost_regex(self) -> str:
        return pulumi.get(self, "vhost_regex")


class AwaitableGetAlarmResult(GetAlarmResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAlarmResult(
            alarm_id=self.alarm_id,
            enabled=self.enabled,
            id=self.id,
            instance_id=self.instance_id,
            message_type=self.message_type,
            queue_regex=self.queue_regex,
            recipients=self.recipients,
            time_threshold=self.time_threshold,
            type=self.type,
            value_threshold=self.value_threshold,
            vhost_regex=self.vhost_regex)


def get_alarm(alarm_id: Optional[int] = None,
              instance_id: Optional[int] = None,
              type: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAlarmResult:
    """
    Use this data source to retrieve information about default or created alarms. Either use `alarm_id` or `type` to retrieve the alarm.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudamqp as cloudamqp

    default_cpu_alarm = cloudamqp.get_alarm(instance_id=cloudamqp_instance["instance"]["id"],
        type="cpu")
    ```
    ## Argument reference

    * `instance_id` - (Required) The CloudAMQP instance identifier.
    * `alarm_id`    - (Optional) The alarm identifier. Either use this or `type` to give `Alarm` necessary information to retrieve the alarm.
    * `type`        - (Optional) The alarm type. Either use this or `alarm_id` to give `Alarm` necessary information when retrieve the alarm.

    ## Attributes reference

    All attributes reference are computed

    * `id`              - The identifier for this resource.
    * `enabled`         - Enable/disable status of the alarm.
    * `value_threshold` - The value threshold that triggers the alarm.
    * `time_threshold`  - The time interval (in seconds) the `value_threshold` should be active before trigger an alarm.
    * `queue_regex`     - Regular expression for which queue to check.
    * `vhost_regex`     - Regular expression for which vhost to check
    * `recipients`      - Identifier for recipient to be notified.
    * `message_type`    - Message type `(total, unacked, ready)` used by queue alarm type.

    ## Dependency

    This data source depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.
    """
    __args__ = dict()
    __args__['alarmId'] = alarm_id
    __args__['instanceId'] = instance_id
    __args__['type'] = type
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('cloudamqp:index/getAlarm:getAlarm', __args__, opts=opts, typ=GetAlarmResult).value

    return AwaitableGetAlarmResult(
        alarm_id=__ret__.alarm_id,
        enabled=__ret__.enabled,
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        message_type=__ret__.message_type,
        queue_regex=__ret__.queue_regex,
        recipients=__ret__.recipients,
        time_threshold=__ret__.time_threshold,
        type=__ret__.type,
        value_threshold=__ret__.value_threshold,
        vhost_regex=__ret__.vhost_regex)


@_utilities.lift_output_func(get_alarm)
def get_alarm_output(alarm_id: Optional[pulumi.Input[Optional[int]]] = None,
                     instance_id: Optional[pulumi.Input[int]] = None,
                     type: Optional[pulumi.Input[Optional[str]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAlarmResult]:
    """
    Use this data source to retrieve information about default or created alarms. Either use `alarm_id` or `type` to retrieve the alarm.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_cloudamqp as cloudamqp

    default_cpu_alarm = cloudamqp.get_alarm(instance_id=cloudamqp_instance["instance"]["id"],
        type="cpu")
    ```
    ## Argument reference

    * `instance_id` - (Required) The CloudAMQP instance identifier.
    * `alarm_id`    - (Optional) The alarm identifier. Either use this or `type` to give `Alarm` necessary information to retrieve the alarm.
    * `type`        - (Optional) The alarm type. Either use this or `alarm_id` to give `Alarm` necessary information when retrieve the alarm.

    ## Attributes reference

    All attributes reference are computed

    * `id`              - The identifier for this resource.
    * `enabled`         - Enable/disable status of the alarm.
    * `value_threshold` - The value threshold that triggers the alarm.
    * `time_threshold`  - The time interval (in seconds) the `value_threshold` should be active before trigger an alarm.
    * `queue_regex`     - Regular expression for which queue to check.
    * `vhost_regex`     - Regular expression for which vhost to check
    * `recipients`      - Identifier for recipient to be notified.
    * `message_type`    - Message type `(total, unacked, ready)` used by queue alarm type.

    ## Dependency

    This data source depends on CloudAMQP instance identifier, `cloudamqp_instance.instance.id`.
    """
    ...
