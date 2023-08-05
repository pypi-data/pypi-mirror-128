# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['ContainerRegistryArgs', 'ContainerRegistry']

@pulumi.input_type
class ContainerRegistryArgs:
    def __init__(__self__, *,
                 subscription_tier_slug: pulumi.Input[str],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ContainerRegistry resource.
        :param pulumi.Input[str] subscription_tier_slug: The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        :param pulumi.Input[str] name: The name of the container_registry
        """
        pulumi.set(__self__, "subscription_tier_slug", subscription_tier_slug)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="subscriptionTierSlug")
    def subscription_tier_slug(self) -> pulumi.Input[str]:
        """
        The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        """
        return pulumi.get(self, "subscription_tier_slug")

    @subscription_tier_slug.setter
    def subscription_tier_slug(self, value: pulumi.Input[str]):
        pulumi.set(self, "subscription_tier_slug", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container_registry
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ContainerRegistryState:
    def __init__(__self__, *,
                 endpoint: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 server_url: Optional[pulumi.Input[str]] = None,
                 subscription_tier_slug: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering ContainerRegistry resources.
        :param pulumi.Input[str] name: The name of the container_registry
        :param pulumi.Input[str] subscription_tier_slug: The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        """
        if endpoint is not None:
            pulumi.set(__self__, "endpoint", endpoint)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if server_url is not None:
            pulumi.set(__self__, "server_url", server_url)
        if subscription_tier_slug is not None:
            pulumi.set(__self__, "subscription_tier_slug", subscription_tier_slug)

    @property
    @pulumi.getter
    def endpoint(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "endpoint")

    @endpoint.setter
    def endpoint(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "endpoint", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the container_registry
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="serverUrl")
    def server_url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "server_url")

    @server_url.setter
    def server_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_url", value)

    @property
    @pulumi.getter(name="subscriptionTierSlug")
    def subscription_tier_slug(self) -> Optional[pulumi.Input[str]]:
        """
        The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        """
        return pulumi.get(self, "subscription_tier_slug")

    @subscription_tier_slug.setter
    def subscription_tier_slug(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subscription_tier_slug", value)


class ContainerRegistry(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subscription_tier_slug: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a DigitalOcean Container Registry resource. A Container Registry is
        a secure, private location to store your containers for rapid deployment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_digitalocean as digitalocean

        # Create a new container registry
        foobar = digitalocean.ContainerRegistry("foobar", subscription_tier_slug="starter")
        ```

        ## Import

        Container Registries can be imported using the `name`, e.g.

        ```sh
         $ pulumi import digitalocean:index/containerRegistry:ContainerRegistry myregistry registryname
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the container_registry
        :param pulumi.Input[str] subscription_tier_slug: The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ContainerRegistryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a DigitalOcean Container Registry resource. A Container Registry is
        a secure, private location to store your containers for rapid deployment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_digitalocean as digitalocean

        # Create a new container registry
        foobar = digitalocean.ContainerRegistry("foobar", subscription_tier_slug="starter")
        ```

        ## Import

        Container Registries can be imported using the `name`, e.g.

        ```sh
         $ pulumi import digitalocean:index/containerRegistry:ContainerRegistry myregistry registryname
        ```

        :param str resource_name: The name of the resource.
        :param ContainerRegistryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ContainerRegistryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 subscription_tier_slug: Optional[pulumi.Input[str]] = None,
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
            __props__ = ContainerRegistryArgs.__new__(ContainerRegistryArgs)

            __props__.__dict__["name"] = name
            if subscription_tier_slug is None and not opts.urn:
                raise TypeError("Missing required property 'subscription_tier_slug'")
            __props__.__dict__["subscription_tier_slug"] = subscription_tier_slug
            __props__.__dict__["endpoint"] = None
            __props__.__dict__["server_url"] = None
        super(ContainerRegistry, __self__).__init__(
            'digitalocean:index/containerRegistry:ContainerRegistry',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            endpoint: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            server_url: Optional[pulumi.Input[str]] = None,
            subscription_tier_slug: Optional[pulumi.Input[str]] = None) -> 'ContainerRegistry':
        """
        Get an existing ContainerRegistry resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the container_registry
        :param pulumi.Input[str] subscription_tier_slug: The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ContainerRegistryState.__new__(_ContainerRegistryState)

        __props__.__dict__["endpoint"] = endpoint
        __props__.__dict__["name"] = name
        __props__.__dict__["server_url"] = server_url
        __props__.__dict__["subscription_tier_slug"] = subscription_tier_slug
        return ContainerRegistry(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def endpoint(self) -> pulumi.Output[str]:
        return pulumi.get(self, "endpoint")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the container_registry
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="serverUrl")
    def server_url(self) -> pulumi.Output[str]:
        return pulumi.get(self, "server_url")

    @property
    @pulumi.getter(name="subscriptionTierSlug")
    def subscription_tier_slug(self) -> pulumi.Output[str]:
        """
        The slug identifier for the subscription tier to use (`starter`, `basic`, or `professional`)
        """
        return pulumi.get(self, "subscription_tier_slug")

