# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ConfigurationArgs', 'Configuration']

@pulumi.input_type
class ConfigurationArgs:
    def __init__(__self__, *,
                 datastore: pulumi.Input['ConfigurationDatastoreArgs'],
                 description: pulumi.Input[str],
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Configuration resource.
        :param pulumi.Input['ConfigurationDatastoreArgs'] datastore: An array of database engine type and version. The datastore
               object structure is documented below. Changing this creates resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]] configurations: An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        :param pulumi.Input[str] name: Configuration parameter name. Changing this creates a new resource.
        :param pulumi.Input[str] region: The region in which to create the db instance. Changing this
               creates a new instance.
        """
        pulumi.set(__self__, "datastore", datastore)
        pulumi.set(__self__, "description", description)
        if configurations is not None:
            pulumi.set(__self__, "configurations", configurations)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def datastore(self) -> pulumi.Input['ConfigurationDatastoreArgs']:
        """
        An array of database engine type and version. The datastore
        object structure is documented below. Changing this creates resource.
        """
        return pulumi.get(self, "datastore")

    @datastore.setter
    def datastore(self, value: pulumi.Input['ConfigurationDatastoreArgs']):
        pulumi.set(self, "datastore", value)

    @property
    @pulumi.getter
    def description(self) -> pulumi.Input[str]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: pulumi.Input[str]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]]]:
        """
        An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        """
        return pulumi.get(self, "configurations")

    @configurations.setter
    def configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]]]):
        pulumi.set(self, "configurations", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Configuration parameter name. Changing this creates a new resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to create the db instance. Changing this
        creates a new instance.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


@pulumi.input_type
class _ConfigurationState:
    def __init__(__self__, *,
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]]] = None,
                 datastore: Optional[pulumi.Input['ConfigurationDatastoreArgs']] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Configuration resources.
        :param pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]] configurations: An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        :param pulumi.Input['ConfigurationDatastoreArgs'] datastore: An array of database engine type and version. The datastore
               object structure is documented below. Changing this creates resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] name: Configuration parameter name. Changing this creates a new resource.
        :param pulumi.Input[str] region: The region in which to create the db instance. Changing this
               creates a new instance.
        """
        if configurations is not None:
            pulumi.set(__self__, "configurations", configurations)
        if datastore is not None:
            pulumi.set(__self__, "datastore", datastore)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if region is not None:
            pulumi.set(__self__, "region", region)

    @property
    @pulumi.getter
    def configurations(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]]]:
        """
        An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        """
        return pulumi.get(self, "configurations")

    @configurations.setter
    def configurations(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ConfigurationConfigurationArgs']]]]):
        pulumi.set(self, "configurations", value)

    @property
    @pulumi.getter
    def datastore(self) -> Optional[pulumi.Input['ConfigurationDatastoreArgs']]:
        """
        An array of database engine type and version. The datastore
        object structure is documented below. Changing this creates resource.
        """
        return pulumi.get(self, "datastore")

    @datastore.setter
    def datastore(self, value: Optional[pulumi.Input['ConfigurationDatastoreArgs']]):
        pulumi.set(self, "datastore", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Configuration parameter name. Changing this creates a new resource.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def region(self) -> Optional[pulumi.Input[str]]:
        """
        The region in which to create the db instance. Changing this
        creates a new instance.
        """
        return pulumi.get(self, "region")

    @region.setter
    def region(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "region", value)


class Configuration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ConfigurationConfigurationArgs']]]]] = None,
                 datastore: Optional[pulumi.Input[pulumi.InputType['ConfigurationDatastoreArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a V1 DB configuration resource within OpenStack.

        ## Example Usage
        ### Configuration

        ```python
        import pulumi
        import pulumi_openstack as openstack

        test = openstack.database.Configuration("test",
            configurations=[openstack.database.ConfigurationConfigurationArgs(
                name="max_connections",
                value="200",
            )],
            datastore=openstack.database.ConfigurationDatastoreArgs(
                type="mysql",
                version="mysql-5.7",
            ),
            description="description")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ConfigurationConfigurationArgs']]]] configurations: An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        :param pulumi.Input[pulumi.InputType['ConfigurationDatastoreArgs']] datastore: An array of database engine type and version. The datastore
               object structure is documented below. Changing this creates resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] name: Configuration parameter name. Changing this creates a new resource.
        :param pulumi.Input[str] region: The region in which to create the db instance. Changing this
               creates a new instance.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a V1 DB configuration resource within OpenStack.

        ## Example Usage
        ### Configuration

        ```python
        import pulumi
        import pulumi_openstack as openstack

        test = openstack.database.Configuration("test",
            configurations=[openstack.database.ConfigurationConfigurationArgs(
                name="max_connections",
                value="200",
            )],
            datastore=openstack.database.ConfigurationDatastoreArgs(
                type="mysql",
                version="mysql-5.7",
            ),
            description="description")
        ```

        :param str resource_name: The name of the resource.
        :param ConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ConfigurationConfigurationArgs']]]]] = None,
                 datastore: Optional[pulumi.Input[pulumi.InputType['ConfigurationDatastoreArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 region: Optional[pulumi.Input[str]] = None,
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
            __props__ = ConfigurationArgs.__new__(ConfigurationArgs)

            __props__.__dict__["configurations"] = configurations
            if datastore is None and not opts.urn:
                raise TypeError("Missing required property 'datastore'")
            __props__.__dict__["datastore"] = datastore
            if description is None and not opts.urn:
                raise TypeError("Missing required property 'description'")
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            __props__.__dict__["region"] = region
        super(Configuration, __self__).__init__(
            'openstack:database/configuration:Configuration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            configurations: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ConfigurationConfigurationArgs']]]]] = None,
            datastore: Optional[pulumi.Input[pulumi.InputType['ConfigurationDatastoreArgs']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            region: Optional[pulumi.Input[str]] = None) -> 'Configuration':
        """
        Get an existing Configuration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ConfigurationConfigurationArgs']]]] configurations: An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        :param pulumi.Input[pulumi.InputType['ConfigurationDatastoreArgs']] datastore: An array of database engine type and version. The datastore
               object structure is documented below. Changing this creates resource.
        :param pulumi.Input[str] description: Description of the resource.
        :param pulumi.Input[str] name: Configuration parameter name. Changing this creates a new resource.
        :param pulumi.Input[str] region: The region in which to create the db instance. Changing this
               creates a new instance.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ConfigurationState.__new__(_ConfigurationState)

        __props__.__dict__["configurations"] = configurations
        __props__.__dict__["datastore"] = datastore
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["region"] = region
        return Configuration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def configurations(self) -> pulumi.Output[Optional[Sequence['outputs.ConfigurationConfiguration']]]:
        """
        An array of configuration parameter name and value. Can be specified multiple times. The configuration object structure is documented below.
        """
        return pulumi.get(self, "configurations")

    @property
    @pulumi.getter
    def datastore(self) -> pulumi.Output['outputs.ConfigurationDatastore']:
        """
        An array of database engine type and version. The datastore
        object structure is documented below. Changing this creates resource.
        """
        return pulumi.get(self, "datastore")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        Description of the resource.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Configuration parameter name. Changing this creates a new resource.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def region(self) -> pulumi.Output[str]:
        """
        The region in which to create the db instance. Changing this
        creates a new instance.
        """
        return pulumi.get(self, "region")

