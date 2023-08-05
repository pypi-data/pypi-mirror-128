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
    'GetVolumesResult',
    'AwaitableGetVolumesResult',
    'get_volumes',
    'get_volumes_output',
]

@pulumi.output_type
class GetVolumesResult:
    """
    A collection of values returned by getVolumes.
    """
    def __init__(__self__, id=None, volumes=None, with_selector=None, with_statuses=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if volumes and not isinstance(volumes, list):
            raise TypeError("Expected argument 'volumes' to be a list")
        pulumi.set(__self__, "volumes", volumes)
        if with_selector and not isinstance(with_selector, str):
            raise TypeError("Expected argument 'with_selector' to be a str")
        pulumi.set(__self__, "with_selector", with_selector)
        if with_statuses and not isinstance(with_statuses, list):
            raise TypeError("Expected argument 'with_statuses' to be a list")
        pulumi.set(__self__, "with_statuses", with_statuses)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def volumes(self) -> Sequence['outputs.GetVolumesVolumeResult']:
        """
        (list) List of all matching volumes. See `data.hcloud_volume` for schema.
        """
        return pulumi.get(self, "volumes")

    @property
    @pulumi.getter(name="withSelector")
    def with_selector(self) -> Optional[str]:
        return pulumi.get(self, "with_selector")

    @property
    @pulumi.getter(name="withStatuses")
    def with_statuses(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "with_statuses")


class AwaitableGetVolumesResult(GetVolumesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVolumesResult(
            id=self.id,
            volumes=self.volumes,
            with_selector=self.with_selector,
            with_statuses=self.with_statuses)


def get_volumes(with_selector: Optional[str] = None,
                with_statuses: Optional[Sequence[str]] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVolumesResult:
    """
    Provides details about multiple Hetzner Cloud volumes.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    volume_ = hcloud.get_volumes()
    volume3 = hcloud.get_volumes(with_selector="key=value")
    ```


    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    :param Sequence[str] with_statuses: List only volumes with the specified status, could contain `creating` or `available`.
    """
    __args__ = dict()
    __args__['withSelector'] = with_selector
    __args__['withStatuses'] = with_statuses
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('hcloud:index/getVolumes:getVolumes', __args__, opts=opts, typ=GetVolumesResult).value

    return AwaitableGetVolumesResult(
        id=__ret__.id,
        volumes=__ret__.volumes,
        with_selector=__ret__.with_selector,
        with_statuses=__ret__.with_statuses)


@_utilities.lift_output_func(get_volumes)
def get_volumes_output(with_selector: Optional[pulumi.Input[Optional[str]]] = None,
                       with_statuses: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetVolumesResult]:
    """
    Provides details about multiple Hetzner Cloud volumes.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_hcloud as hcloud

    volume_ = hcloud.get_volumes()
    volume3 = hcloud.get_volumes(with_selector="key=value")
    ```


    :param str with_selector: [Label selector](https://docs.hetzner.cloud/#overview-label-selector)
    :param Sequence[str] with_statuses: List only volumes with the specified status, could contain `creating` or `available`.
    """
    ...
