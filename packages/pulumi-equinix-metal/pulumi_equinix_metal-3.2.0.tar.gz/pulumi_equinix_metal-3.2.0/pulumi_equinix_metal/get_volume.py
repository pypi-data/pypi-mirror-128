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
    'GetVolumeResult',
    'AwaitableGetVolumeResult',
    'get_volume',
    'get_volume_output',
]

@pulumi.output_type
class GetVolumeResult:
    """
    A collection of values returned by getVolume.
    """
    def __init__(__self__, billing_cycle=None, created=None, description=None, device_ids=None, facility=None, id=None, locked=None, name=None, plan=None, project_id=None, size=None, snapshot_policies=None, state=None, updated=None, volume_id=None):
        if billing_cycle and not isinstance(billing_cycle, str):
            raise TypeError("Expected argument 'billing_cycle' to be a str")
        pulumi.set(__self__, "billing_cycle", billing_cycle)
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if device_ids and not isinstance(device_ids, list):
            raise TypeError("Expected argument 'device_ids' to be a list")
        pulumi.set(__self__, "device_ids", device_ids)
        if facility and not isinstance(facility, str):
            raise TypeError("Expected argument 'facility' to be a str")
        pulumi.set(__self__, "facility", facility)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if locked and not isinstance(locked, bool):
            raise TypeError("Expected argument 'locked' to be a bool")
        pulumi.set(__self__, "locked", locked)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if plan and not isinstance(plan, str):
            raise TypeError("Expected argument 'plan' to be a str")
        pulumi.set(__self__, "plan", plan)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if size and not isinstance(size, int):
            raise TypeError("Expected argument 'size' to be a int")
        pulumi.set(__self__, "size", size)
        if snapshot_policies and not isinstance(snapshot_policies, list):
            raise TypeError("Expected argument 'snapshot_policies' to be a list")
        pulumi.set(__self__, "snapshot_policies", snapshot_policies)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if updated and not isinstance(updated, str):
            raise TypeError("Expected argument 'updated' to be a str")
        pulumi.set(__self__, "updated", updated)
        if volume_id and not isinstance(volume_id, str):
            raise TypeError("Expected argument 'volume_id' to be a str")
        pulumi.set(__self__, "volume_id", volume_id)

    @property
    @pulumi.getter(name="billingCycle")
    def billing_cycle(self) -> str:
        return pulumi.get(self, "billing_cycle")

    @property
    @pulumi.getter
    def created(self) -> str:
        return pulumi.get(self, "created")

    @property
    @pulumi.getter
    def description(self) -> str:
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="deviceIds")
    def device_ids(self) -> Sequence[str]:
        return pulumi.get(self, "device_ids")

    @property
    @pulumi.getter
    def facility(self) -> str:
        return pulumi.get(self, "facility")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def locked(self) -> bool:
        return pulumi.get(self, "locked")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def plan(self) -> str:
        return pulumi.get(self, "plan")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def size(self) -> int:
        return pulumi.get(self, "size")

    @property
    @pulumi.getter(name="snapshotPolicies")
    def snapshot_policies(self) -> Sequence['outputs.GetVolumeSnapshotPolicyResult']:
        return pulumi.get(self, "snapshot_policies")

    @property
    @pulumi.getter
    def state(self) -> str:
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def updated(self) -> str:
        return pulumi.get(self, "updated")

    @property
    @pulumi.getter(name="volumeId")
    def volume_id(self) -> str:
        return pulumi.get(self, "volume_id")


class AwaitableGetVolumeResult(GetVolumeResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVolumeResult(
            billing_cycle=self.billing_cycle,
            created=self.created,
            description=self.description,
            device_ids=self.device_ids,
            facility=self.facility,
            id=self.id,
            locked=self.locked,
            name=self.name,
            plan=self.plan,
            project_id=self.project_id,
            size=self.size,
            snapshot_policies=self.snapshot_policies,
            state=self.state,
            updated=self.updated,
            volume_id=self.volume_id)


def get_volume(name: Optional[str] = None,
               project_id: Optional[str] = None,
               volume_id: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVolumeResult:
    """
    Datasource `Volume` was removed in version 3.0.0, and the API support was deprecated on June 1st 2021. See https://metal.equinix.com/developers/docs/storage/elastic-block-storage/#elastic-block-storage for more details.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['projectId'] = project_id
    __args__['volumeId'] = volume_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('equinix-metal:index/getVolume:getVolume', __args__, opts=opts, typ=GetVolumeResult).value

    return AwaitableGetVolumeResult(
        billing_cycle=__ret__.billing_cycle,
        created=__ret__.created,
        description=__ret__.description,
        device_ids=__ret__.device_ids,
        facility=__ret__.facility,
        id=__ret__.id,
        locked=__ret__.locked,
        name=__ret__.name,
        plan=__ret__.plan,
        project_id=__ret__.project_id,
        size=__ret__.size,
        snapshot_policies=__ret__.snapshot_policies,
        state=__ret__.state,
        updated=__ret__.updated,
        volume_id=__ret__.volume_id)


@_utilities.lift_output_func(get_volume)
def get_volume_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                      project_id: Optional[pulumi.Input[Optional[str]]] = None,
                      volume_id: Optional[pulumi.Input[Optional[str]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVolumeResult]:
    """
    Datasource `Volume` was removed in version 3.0.0, and the API support was deprecated on June 1st 2021. See https://metal.equinix.com/developers/docs/storage/elastic-block-storage/#elastic-block-storage for more details.
    """
    ...
