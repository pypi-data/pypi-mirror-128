# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['HardcodedAttributeIdentityProviderMapperArgs', 'HardcodedAttributeIdentityProviderMapper']

@pulumi.input_type
class HardcodedAttributeIdentityProviderMapperArgs:
    def __init__(__self__, *,
                 identity_provider_alias: pulumi.Input[str],
                 realm: pulumi.Input[str],
                 user_session: pulumi.Input[bool],
                 attribute_name: Optional[pulumi.Input[str]] = None,
                 attribute_value: Optional[pulumi.Input[str]] = None,
                 extra_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a HardcodedAttributeIdentityProviderMapper resource.
        :param pulumi.Input[str] identity_provider_alias: IDP Alias
        :param pulumi.Input[str] realm: Realm Name
        :param pulumi.Input[bool] user_session: Is Attribute Related To a User Session
        :param pulumi.Input[str] attribute_name: OIDC Claim
        :param pulumi.Input[str] attribute_value: User Attribute
        :param pulumi.Input[str] name: IDP Mapper Name
        """
        pulumi.set(__self__, "identity_provider_alias", identity_provider_alias)
        pulumi.set(__self__, "realm", realm)
        pulumi.set(__self__, "user_session", user_session)
        if attribute_name is not None:
            pulumi.set(__self__, "attribute_name", attribute_name)
        if attribute_value is not None:
            pulumi.set(__self__, "attribute_value", attribute_value)
        if extra_config is not None:
            pulumi.set(__self__, "extra_config", extra_config)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="identityProviderAlias")
    def identity_provider_alias(self) -> pulumi.Input[str]:
        """
        IDP Alias
        """
        return pulumi.get(self, "identity_provider_alias")

    @identity_provider_alias.setter
    def identity_provider_alias(self, value: pulumi.Input[str]):
        pulumi.set(self, "identity_provider_alias", value)

    @property
    @pulumi.getter
    def realm(self) -> pulumi.Input[str]:
        """
        Realm Name
        """
        return pulumi.get(self, "realm")

    @realm.setter
    def realm(self, value: pulumi.Input[str]):
        pulumi.set(self, "realm", value)

    @property
    @pulumi.getter(name="userSession")
    def user_session(self) -> pulumi.Input[bool]:
        """
        Is Attribute Related To a User Session
        """
        return pulumi.get(self, "user_session")

    @user_session.setter
    def user_session(self, value: pulumi.Input[bool]):
        pulumi.set(self, "user_session", value)

    @property
    @pulumi.getter(name="attributeName")
    def attribute_name(self) -> Optional[pulumi.Input[str]]:
        """
        OIDC Claim
        """
        return pulumi.get(self, "attribute_name")

    @attribute_name.setter
    def attribute_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attribute_name", value)

    @property
    @pulumi.getter(name="attributeValue")
    def attribute_value(self) -> Optional[pulumi.Input[str]]:
        """
        User Attribute
        """
        return pulumi.get(self, "attribute_value")

    @attribute_value.setter
    def attribute_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attribute_value", value)

    @property
    @pulumi.getter(name="extraConfig")
    def extra_config(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        return pulumi.get(self, "extra_config")

    @extra_config.setter
    def extra_config(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "extra_config", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        IDP Mapper Name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _HardcodedAttributeIdentityProviderMapperState:
    def __init__(__self__, *,
                 attribute_name: Optional[pulumi.Input[str]] = None,
                 attribute_value: Optional[pulumi.Input[str]] = None,
                 extra_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 identity_provider_alias: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 realm: Optional[pulumi.Input[str]] = None,
                 user_session: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering HardcodedAttributeIdentityProviderMapper resources.
        :param pulumi.Input[str] attribute_name: OIDC Claim
        :param pulumi.Input[str] attribute_value: User Attribute
        :param pulumi.Input[str] identity_provider_alias: IDP Alias
        :param pulumi.Input[str] name: IDP Mapper Name
        :param pulumi.Input[str] realm: Realm Name
        :param pulumi.Input[bool] user_session: Is Attribute Related To a User Session
        """
        if attribute_name is not None:
            pulumi.set(__self__, "attribute_name", attribute_name)
        if attribute_value is not None:
            pulumi.set(__self__, "attribute_value", attribute_value)
        if extra_config is not None:
            pulumi.set(__self__, "extra_config", extra_config)
        if identity_provider_alias is not None:
            pulumi.set(__self__, "identity_provider_alias", identity_provider_alias)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if realm is not None:
            pulumi.set(__self__, "realm", realm)
        if user_session is not None:
            pulumi.set(__self__, "user_session", user_session)

    @property
    @pulumi.getter(name="attributeName")
    def attribute_name(self) -> Optional[pulumi.Input[str]]:
        """
        OIDC Claim
        """
        return pulumi.get(self, "attribute_name")

    @attribute_name.setter
    def attribute_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attribute_name", value)

    @property
    @pulumi.getter(name="attributeValue")
    def attribute_value(self) -> Optional[pulumi.Input[str]]:
        """
        User Attribute
        """
        return pulumi.get(self, "attribute_value")

    @attribute_value.setter
    def attribute_value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "attribute_value", value)

    @property
    @pulumi.getter(name="extraConfig")
    def extra_config(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        return pulumi.get(self, "extra_config")

    @extra_config.setter
    def extra_config(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "extra_config", value)

    @property
    @pulumi.getter(name="identityProviderAlias")
    def identity_provider_alias(self) -> Optional[pulumi.Input[str]]:
        """
        IDP Alias
        """
        return pulumi.get(self, "identity_provider_alias")

    @identity_provider_alias.setter
    def identity_provider_alias(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "identity_provider_alias", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        IDP Mapper Name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def realm(self) -> Optional[pulumi.Input[str]]:
        """
        Realm Name
        """
        return pulumi.get(self, "realm")

    @realm.setter
    def realm(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "realm", value)

    @property
    @pulumi.getter(name="userSession")
    def user_session(self) -> Optional[pulumi.Input[bool]]:
        """
        Is Attribute Related To a User Session
        """
        return pulumi.get(self, "user_session")

    @user_session.setter
    def user_session(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "user_session", value)


class HardcodedAttributeIdentityProviderMapper(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attribute_name: Optional[pulumi.Input[str]] = None,
                 attribute_value: Optional[pulumi.Input[str]] = None,
                 extra_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 identity_provider_alias: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 realm: Optional[pulumi.Input[str]] = None,
                 user_session: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Create a HardcodedAttributeIdentityProviderMapper resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attribute_name: OIDC Claim
        :param pulumi.Input[str] attribute_value: User Attribute
        :param pulumi.Input[str] identity_provider_alias: IDP Alias
        :param pulumi.Input[str] name: IDP Mapper Name
        :param pulumi.Input[str] realm: Realm Name
        :param pulumi.Input[bool] user_session: Is Attribute Related To a User Session
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: HardcodedAttributeIdentityProviderMapperArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a HardcodedAttributeIdentityProviderMapper resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param HardcodedAttributeIdentityProviderMapperArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HardcodedAttributeIdentityProviderMapperArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attribute_name: Optional[pulumi.Input[str]] = None,
                 attribute_value: Optional[pulumi.Input[str]] = None,
                 extra_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 identity_provider_alias: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 realm: Optional[pulumi.Input[str]] = None,
                 user_session: Optional[pulumi.Input[bool]] = None,
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
            __props__ = HardcodedAttributeIdentityProviderMapperArgs.__new__(HardcodedAttributeIdentityProviderMapperArgs)

            __props__.__dict__["attribute_name"] = attribute_name
            __props__.__dict__["attribute_value"] = attribute_value
            __props__.__dict__["extra_config"] = extra_config
            if identity_provider_alias is None and not opts.urn:
                raise TypeError("Missing required property 'identity_provider_alias'")
            __props__.__dict__["identity_provider_alias"] = identity_provider_alias
            __props__.__dict__["name"] = name
            if realm is None and not opts.urn:
                raise TypeError("Missing required property 'realm'")
            __props__.__dict__["realm"] = realm
            if user_session is None and not opts.urn:
                raise TypeError("Missing required property 'user_session'")
            __props__.__dict__["user_session"] = user_session
        super(HardcodedAttributeIdentityProviderMapper, __self__).__init__(
            'keycloak:index/hardcodedAttributeIdentityProviderMapper:HardcodedAttributeIdentityProviderMapper',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            attribute_name: Optional[pulumi.Input[str]] = None,
            attribute_value: Optional[pulumi.Input[str]] = None,
            extra_config: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            identity_provider_alias: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            realm: Optional[pulumi.Input[str]] = None,
            user_session: Optional[pulumi.Input[bool]] = None) -> 'HardcodedAttributeIdentityProviderMapper':
        """
        Get an existing HardcodedAttributeIdentityProviderMapper resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] attribute_name: OIDC Claim
        :param pulumi.Input[str] attribute_value: User Attribute
        :param pulumi.Input[str] identity_provider_alias: IDP Alias
        :param pulumi.Input[str] name: IDP Mapper Name
        :param pulumi.Input[str] realm: Realm Name
        :param pulumi.Input[bool] user_session: Is Attribute Related To a User Session
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HardcodedAttributeIdentityProviderMapperState.__new__(_HardcodedAttributeIdentityProviderMapperState)

        __props__.__dict__["attribute_name"] = attribute_name
        __props__.__dict__["attribute_value"] = attribute_value
        __props__.__dict__["extra_config"] = extra_config
        __props__.__dict__["identity_provider_alias"] = identity_provider_alias
        __props__.__dict__["name"] = name
        __props__.__dict__["realm"] = realm
        __props__.__dict__["user_session"] = user_session
        return HardcodedAttributeIdentityProviderMapper(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="attributeName")
    def attribute_name(self) -> pulumi.Output[Optional[str]]:
        """
        OIDC Claim
        """
        return pulumi.get(self, "attribute_name")

    @property
    @pulumi.getter(name="attributeValue")
    def attribute_value(self) -> pulumi.Output[Optional[str]]:
        """
        User Attribute
        """
        return pulumi.get(self, "attribute_value")

    @property
    @pulumi.getter(name="extraConfig")
    def extra_config(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        return pulumi.get(self, "extra_config")

    @property
    @pulumi.getter(name="identityProviderAlias")
    def identity_provider_alias(self) -> pulumi.Output[str]:
        """
        IDP Alias
        """
        return pulumi.get(self, "identity_provider_alias")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        IDP Mapper Name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def realm(self) -> pulumi.Output[str]:
        """
        Realm Name
        """
        return pulumi.get(self, "realm")

    @property
    @pulumi.getter(name="userSession")
    def user_session(self) -> pulumi.Output[bool]:
        """
        Is Attribute Related To a User Session
        """
        return pulumi.get(self, "user_session")

