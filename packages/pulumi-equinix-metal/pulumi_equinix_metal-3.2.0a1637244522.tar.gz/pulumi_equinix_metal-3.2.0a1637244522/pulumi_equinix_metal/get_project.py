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
    'GetProjectResult',
    'AwaitableGetProjectResult',
    'get_project',
    'get_project_output',
]

@pulumi.output_type
class GetProjectResult:
    """
    A collection of values returned by getProject.
    """
    def __init__(__self__, backend_transfer=None, bgp_configs=None, created=None, id=None, name=None, organization_id=None, payment_method_id=None, project_id=None, updated=None, user_ids=None):
        if backend_transfer and not isinstance(backend_transfer, bool):
            raise TypeError("Expected argument 'backend_transfer' to be a bool")
        pulumi.set(__self__, "backend_transfer", backend_transfer)
        if bgp_configs and not isinstance(bgp_configs, list):
            raise TypeError("Expected argument 'bgp_configs' to be a list")
        pulumi.set(__self__, "bgp_configs", bgp_configs)
        if created and not isinstance(created, str):
            raise TypeError("Expected argument 'created' to be a str")
        pulumi.set(__self__, "created", created)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if organization_id and not isinstance(organization_id, str):
            raise TypeError("Expected argument 'organization_id' to be a str")
        pulumi.set(__self__, "organization_id", organization_id)
        if payment_method_id and not isinstance(payment_method_id, str):
            raise TypeError("Expected argument 'payment_method_id' to be a str")
        pulumi.set(__self__, "payment_method_id", payment_method_id)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)
        if updated and not isinstance(updated, str):
            raise TypeError("Expected argument 'updated' to be a str")
        pulumi.set(__self__, "updated", updated)
        if user_ids and not isinstance(user_ids, list):
            raise TypeError("Expected argument 'user_ids' to be a list")
        pulumi.set(__self__, "user_ids", user_ids)

    @property
    @pulumi.getter(name="backendTransfer")
    def backend_transfer(self) -> bool:
        """
        Whether Backend Transfer is enabled for this project
        """
        return pulumi.get(self, "backend_transfer")

    @property
    @pulumi.getter(name="bgpConfigs")
    def bgp_configs(self) -> Sequence['outputs.GetProjectBgpConfigResult']:
        """
        Optional BGP settings. Refer to [Equinix Metal guide for BGP](https://metal.equinix.com/developers/docs/networking/local-global-bgp/).
        """
        return pulumi.get(self, "bgp_configs")

    @property
    @pulumi.getter
    def created(self) -> str:
        """
        The timestamp for when the project was created
        """
        return pulumi.get(self, "created")

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
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="organizationId")
    def organization_id(self) -> str:
        """
        The UUID of this project's parent organization
        """
        return pulumi.get(self, "organization_id")

    @property
    @pulumi.getter(name="paymentMethodId")
    def payment_method_id(self) -> str:
        """
        The UUID of payment method for this project
        """
        return pulumi.get(self, "payment_method_id")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        return pulumi.get(self, "project_id")

    @property
    @pulumi.getter
    def updated(self) -> str:
        """
        The timestamp for the last time the project was updated
        """
        return pulumi.get(self, "updated")

    @property
    @pulumi.getter(name="userIds")
    def user_ids(self) -> Sequence[str]:
        """
        List of UUIDs of user accounts which belong to this project
        """
        return pulumi.get(self, "user_ids")


class AwaitableGetProjectResult(GetProjectResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetProjectResult(
            backend_transfer=self.backend_transfer,
            bgp_configs=self.bgp_configs,
            created=self.created,
            id=self.id,
            name=self.name,
            organization_id=self.organization_id,
            payment_method_id=self.payment_method_id,
            project_id=self.project_id,
            updated=self.updated,
            user_ids=self.user_ids)


def get_project(name: Optional[str] = None,
                project_id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetProjectResult:
    """
    Use this datasource to retrieve attributes of the Project API resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_equinix_metal as equinix_metal

    tf_project1 = equinix_metal.get_project(name="Terraform Fun")
    pulumi.export("usersOfTerraformFun", tf_project1.user_ids)
    ```


    :param str name: The name which is used to look up the project
    :param str project_id: The UUID by which to look up the project
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['projectId'] = project_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('equinix-metal:index/getProject:getProject', __args__, opts=opts, typ=GetProjectResult).value

    return AwaitableGetProjectResult(
        backend_transfer=__ret__.backend_transfer,
        bgp_configs=__ret__.bgp_configs,
        created=__ret__.created,
        id=__ret__.id,
        name=__ret__.name,
        organization_id=__ret__.organization_id,
        payment_method_id=__ret__.payment_method_id,
        project_id=__ret__.project_id,
        updated=__ret__.updated,
        user_ids=__ret__.user_ids)


@_utilities.lift_output_func(get_project)
def get_project_output(name: Optional[pulumi.Input[Optional[str]]] = None,
                       project_id: Optional[pulumi.Input[Optional[str]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetProjectResult]:
    """
    Use this datasource to retrieve attributes of the Project API resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_equinix_metal as equinix_metal

    tf_project1 = equinix_metal.get_project(name="Terraform Fun")
    pulumi.export("usersOfTerraformFun", tf_project1.user_ids)
    ```


    :param str name: The name which is used to look up the project
    :param str project_id: The UUID by which to look up the project
    """
    ...
