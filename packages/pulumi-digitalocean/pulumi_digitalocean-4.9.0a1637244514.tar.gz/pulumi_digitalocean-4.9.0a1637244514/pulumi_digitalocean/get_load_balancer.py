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
    'GetLoadBalancerResult',
    'AwaitableGetLoadBalancerResult',
    'get_load_balancer',
    'get_load_balancer_output',
]

@pulumi.output_type
class GetLoadBalancerResult:
    """
    A collection of values returned by getLoadBalancer.
    """
    def __init__(__self__, algorithm=None, droplet_ids=None, droplet_tag=None, enable_backend_keepalive=None, enable_proxy_protocol=None, forwarding_rules=None, healthchecks=None, id=None, ip=None, load_balancer_urn=None, name=None, redirect_http_to_https=None, region=None, size=None, status=None, sticky_sessions=None, vpc_uuid=None):
        if algorithm and not isinstance(algorithm, str):
            raise TypeError("Expected argument 'algorithm' to be a str")
        pulumi.set(__self__, "algorithm", algorithm)
        if droplet_ids and not isinstance(droplet_ids, list):
            raise TypeError("Expected argument 'droplet_ids' to be a list")
        pulumi.set(__self__, "droplet_ids", droplet_ids)
        if droplet_tag and not isinstance(droplet_tag, str):
            raise TypeError("Expected argument 'droplet_tag' to be a str")
        pulumi.set(__self__, "droplet_tag", droplet_tag)
        if enable_backend_keepalive and not isinstance(enable_backend_keepalive, bool):
            raise TypeError("Expected argument 'enable_backend_keepalive' to be a bool")
        pulumi.set(__self__, "enable_backend_keepalive", enable_backend_keepalive)
        if enable_proxy_protocol and not isinstance(enable_proxy_protocol, bool):
            raise TypeError("Expected argument 'enable_proxy_protocol' to be a bool")
        pulumi.set(__self__, "enable_proxy_protocol", enable_proxy_protocol)
        if forwarding_rules and not isinstance(forwarding_rules, list):
            raise TypeError("Expected argument 'forwarding_rules' to be a list")
        pulumi.set(__self__, "forwarding_rules", forwarding_rules)
        if healthchecks and not isinstance(healthchecks, list):
            raise TypeError("Expected argument 'healthchecks' to be a list")
        pulumi.set(__self__, "healthchecks", healthchecks)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip and not isinstance(ip, str):
            raise TypeError("Expected argument 'ip' to be a str")
        pulumi.set(__self__, "ip", ip)
        if load_balancer_urn and not isinstance(load_balancer_urn, str):
            raise TypeError("Expected argument 'load_balancer_urn' to be a str")
        pulumi.set(__self__, "load_balancer_urn", load_balancer_urn)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if redirect_http_to_https and not isinstance(redirect_http_to_https, bool):
            raise TypeError("Expected argument 'redirect_http_to_https' to be a bool")
        pulumi.set(__self__, "redirect_http_to_https", redirect_http_to_https)
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        pulumi.set(__self__, "region", region)
        if size and not isinstance(size, str):
            raise TypeError("Expected argument 'size' to be a str")
        pulumi.set(__self__, "size", size)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if sticky_sessions and not isinstance(sticky_sessions, list):
            raise TypeError("Expected argument 'sticky_sessions' to be a list")
        pulumi.set(__self__, "sticky_sessions", sticky_sessions)
        if vpc_uuid and not isinstance(vpc_uuid, str):
            raise TypeError("Expected argument 'vpc_uuid' to be a str")
        pulumi.set(__self__, "vpc_uuid", vpc_uuid)

    @property
    @pulumi.getter
    def algorithm(self) -> str:
        return pulumi.get(self, "algorithm")

    @property
    @pulumi.getter(name="dropletIds")
    def droplet_ids(self) -> Sequence[int]:
        return pulumi.get(self, "droplet_ids")

    @property
    @pulumi.getter(name="dropletTag")
    def droplet_tag(self) -> str:
        return pulumi.get(self, "droplet_tag")

    @property
    @pulumi.getter(name="enableBackendKeepalive")
    def enable_backend_keepalive(self) -> bool:
        return pulumi.get(self, "enable_backend_keepalive")

    @property
    @pulumi.getter(name="enableProxyProtocol")
    def enable_proxy_protocol(self) -> bool:
        return pulumi.get(self, "enable_proxy_protocol")

    @property
    @pulumi.getter(name="forwardingRules")
    def forwarding_rules(self) -> Sequence['outputs.GetLoadBalancerForwardingRuleResult']:
        return pulumi.get(self, "forwarding_rules")

    @property
    @pulumi.getter
    def healthchecks(self) -> Sequence['outputs.GetLoadBalancerHealthcheckResult']:
        return pulumi.get(self, "healthchecks")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ip(self) -> str:
        return pulumi.get(self, "ip")

    @property
    @pulumi.getter(name="loadBalancerUrn")
    def load_balancer_urn(self) -> str:
        return pulumi.get(self, "load_balancer_urn")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="redirectHttpToHttps")
    def redirect_http_to_https(self) -> bool:
        return pulumi.get(self, "redirect_http_to_https")

    @property
    @pulumi.getter
    def region(self) -> str:
        return pulumi.get(self, "region")

    @property
    @pulumi.getter
    def size(self) -> str:
        return pulumi.get(self, "size")

    @property
    @pulumi.getter
    def status(self) -> str:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="stickySessions")
    def sticky_sessions(self) -> Sequence['outputs.GetLoadBalancerStickySessionResult']:
        return pulumi.get(self, "sticky_sessions")

    @property
    @pulumi.getter(name="vpcUuid")
    def vpc_uuid(self) -> str:
        return pulumi.get(self, "vpc_uuid")


class AwaitableGetLoadBalancerResult(GetLoadBalancerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoadBalancerResult(
            algorithm=self.algorithm,
            droplet_ids=self.droplet_ids,
            droplet_tag=self.droplet_tag,
            enable_backend_keepalive=self.enable_backend_keepalive,
            enable_proxy_protocol=self.enable_proxy_protocol,
            forwarding_rules=self.forwarding_rules,
            healthchecks=self.healthchecks,
            id=self.id,
            ip=self.ip,
            load_balancer_urn=self.load_balancer_urn,
            name=self.name,
            redirect_http_to_https=self.redirect_http_to_https,
            region=self.region,
            size=self.size,
            status=self.status,
            sticky_sessions=self.sticky_sessions,
            vpc_uuid=self.vpc_uuid)


def get_load_balancer(name: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoadBalancerResult:
    """
    Get information on a load balancer for use in other resources. This data source
    provides all of the load balancers properties as configured on your DigitalOcean
    account. This is useful if the load balancer in question is not managed by
    the provider or you need to utilize any of the load balancers data.

    An error is triggered if the provided load balancer name does not exist.

    ## Example Usage

    Get the load balancer:

    ```python
    import pulumi
    import pulumi_digitalocean as digitalocean

    example = digitalocean.get_load_balancer(name="app")
    pulumi.export("lbOutput", example.ip)
    ```


    :param str name: The name of load balancer.
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('digitalocean:index/getLoadBalancer:getLoadBalancer', __args__, opts=opts, typ=GetLoadBalancerResult).value

    return AwaitableGetLoadBalancerResult(
        algorithm=__ret__.algorithm,
        droplet_ids=__ret__.droplet_ids,
        droplet_tag=__ret__.droplet_tag,
        enable_backend_keepalive=__ret__.enable_backend_keepalive,
        enable_proxy_protocol=__ret__.enable_proxy_protocol,
        forwarding_rules=__ret__.forwarding_rules,
        healthchecks=__ret__.healthchecks,
        id=__ret__.id,
        ip=__ret__.ip,
        load_balancer_urn=__ret__.load_balancer_urn,
        name=__ret__.name,
        redirect_http_to_https=__ret__.redirect_http_to_https,
        region=__ret__.region,
        size=__ret__.size,
        status=__ret__.status,
        sticky_sessions=__ret__.sticky_sessions,
        vpc_uuid=__ret__.vpc_uuid)


@_utilities.lift_output_func(get_load_balancer)
def get_load_balancer_output(name: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLoadBalancerResult]:
    """
    Get information on a load balancer for use in other resources. This data source
    provides all of the load balancers properties as configured on your DigitalOcean
    account. This is useful if the load balancer in question is not managed by
    the provider or you need to utilize any of the load balancers data.

    An error is triggered if the provided load balancer name does not exist.

    ## Example Usage

    Get the load balancer:

    ```python
    import pulumi
    import pulumi_digitalocean as digitalocean

    example = digitalocean.get_load_balancer(name="app")
    pulumi.export("lbOutput", example.ip)
    ```


    :param str name: The name of load balancer.
    """
    ...
