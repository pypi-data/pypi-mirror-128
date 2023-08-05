# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'ContainerV1Acl',
    'ContainerV1AclRead',
    'ContainerV1Consumer',
    'ContainerV1SecretRef',
    'OrderV1Meta',
    'SecretV1Acl',
    'SecretV1AclRead',
    'GetContainerAclResult',
    'GetContainerAclReadResult',
    'GetContainerConsumerResult',
    'GetContainerSecretRefResult',
    'GetSecretAclResult',
    'GetSecretAclReadResult',
]

@pulumi.output_type
class ContainerV1Acl(dict):
    def __init__(__self__, *,
                 read: Optional['outputs.ContainerV1AclRead'] = None):
        if read is not None:
            pulumi.set(__self__, "read", read)

    @property
    @pulumi.getter
    def read(self) -> Optional['outputs.ContainerV1AclRead']:
        return pulumi.get(self, "read")


@pulumi.output_type
class ContainerV1AclRead(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "projectAccess":
            suggest = "project_access"
        elif key == "updatedAt":
            suggest = "updated_at"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerV1AclRead. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerV1AclRead.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerV1AclRead.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 project_access: Optional[bool] = None,
                 updated_at: Optional[str] = None,
                 users: Optional[Sequence[str]] = None):
        """
        :param str created_at: The date the container ACL was created.
        :param bool project_access: Whether the container is accessible project wide.
               Defaults to `true`.
        :param str updated_at: The date the container ACL was last updated.
        :param Sequence[str] users: The list of user IDs, which are allowed to access the
               container, when `project_access` is set to `false`.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if project_access is not None:
            pulumi.set(__self__, "project_access", project_access)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date the container ACL was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="projectAccess")
    def project_access(self) -> Optional[bool]:
        """
        Whether the container is accessible project wide.
        Defaults to `true`.
        """
        return pulumi.get(self, "project_access")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        The date the container ACL was last updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        """
        The list of user IDs, which are allowed to access the
        container, when `project_access` is set to `false`.
        """
        return pulumi.get(self, "users")


@pulumi.output_type
class ContainerV1Consumer(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        """
        :param str name: The name of the secret reference. The reference names must correspond the container type, more details are available [here](https://docs.openstack.org/barbican/stein/api/reference/containers.html).
        :param str url: The consumer URL.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the secret reference. The reference names must correspond the container type, more details are available [here](https://docs.openstack.org/barbican/stein/api/reference/containers.html).
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        """
        The consumer URL.
        """
        return pulumi.get(self, "url")


@pulumi.output_type
class ContainerV1SecretRef(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "secretRef":
            suggest = "secret_ref"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in ContainerV1SecretRef. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        ContainerV1SecretRef.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        ContainerV1SecretRef.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 secret_ref: str,
                 name: Optional[str] = None):
        """
        :param str secret_ref: The secret reference / where to find the secret, URL.
        :param str name: The name of the secret reference. The reference names must correspond the container type, more details are available [here](https://docs.openstack.org/barbican/stein/api/reference/containers.html).
        """
        pulumi.set(__self__, "secret_ref", secret_ref)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="secretRef")
    def secret_ref(self) -> str:
        """
        The secret reference / where to find the secret, URL.
        """
        return pulumi.get(self, "secret_ref")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the secret reference. The reference names must correspond the container type, more details are available [here](https://docs.openstack.org/barbican/stein/api/reference/containers.html).
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class OrderV1Meta(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "bitLength":
            suggest = "bit_length"
        elif key == "payloadContentType":
            suggest = "payload_content_type"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in OrderV1Meta. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        OrderV1Meta.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        OrderV1Meta.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 algorithm: str,
                 bit_length: int,
                 expiration: Optional[str] = None,
                 mode: Optional[str] = None,
                 name: Optional[str] = None,
                 payload_content_type: Optional[str] = None):
        """
        :param str algorithm: Algorithm to use for key generation.
        :param int bit_length: - Bit lenght of key to be generated.
        :param str expiration: This is a UTC timestamp in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ. If set, the secret will not be available after this time.
        :param str mode: The mode to use for key generation.
        :param str name: The name of the secret set by the user.
        :param str payload_content_type: The media type for the content of the secrets payload. Must be one of `text/plain`, `text/plain;charset=utf-8`, `text/plain; charset=utf-8`, `application/octet-stream`, `application/pkcs8`.
        """
        pulumi.set(__self__, "algorithm", algorithm)
        pulumi.set(__self__, "bit_length", bit_length)
        if expiration is not None:
            pulumi.set(__self__, "expiration", expiration)
        if mode is not None:
            pulumi.set(__self__, "mode", mode)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if payload_content_type is not None:
            pulumi.set(__self__, "payload_content_type", payload_content_type)

    @property
    @pulumi.getter
    def algorithm(self) -> str:
        """
        Algorithm to use for key generation.
        """
        return pulumi.get(self, "algorithm")

    @property
    @pulumi.getter(name="bitLength")
    def bit_length(self) -> int:
        """
        - Bit lenght of key to be generated.
        """
        return pulumi.get(self, "bit_length")

    @property
    @pulumi.getter
    def expiration(self) -> Optional[str]:
        """
        This is a UTC timestamp in ISO 8601 format YYYY-MM-DDTHH:MM:SSZ. If set, the secret will not be available after this time.
        """
        return pulumi.get(self, "expiration")

    @property
    @pulumi.getter
    def mode(self) -> Optional[str]:
        """
        The mode to use for key generation.
        """
        return pulumi.get(self, "mode")

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The name of the secret set by the user.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="payloadContentType")
    def payload_content_type(self) -> Optional[str]:
        """
        The media type for the content of the secrets payload. Must be one of `text/plain`, `text/plain;charset=utf-8`, `text/plain; charset=utf-8`, `application/octet-stream`, `application/pkcs8`.
        """
        return pulumi.get(self, "payload_content_type")


@pulumi.output_type
class SecretV1Acl(dict):
    def __init__(__self__, *,
                 read: Optional['outputs.SecretV1AclRead'] = None):
        if read is not None:
            pulumi.set(__self__, "read", read)

    @property
    @pulumi.getter
    def read(self) -> Optional['outputs.SecretV1AclRead']:
        return pulumi.get(self, "read")


@pulumi.output_type
class SecretV1AclRead(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "createdAt":
            suggest = "created_at"
        elif key == "projectAccess":
            suggest = "project_access"
        elif key == "updatedAt":
            suggest = "updated_at"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in SecretV1AclRead. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        SecretV1AclRead.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        SecretV1AclRead.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 created_at: Optional[str] = None,
                 project_access: Optional[bool] = None,
                 updated_at: Optional[str] = None,
                 users: Optional[Sequence[str]] = None):
        """
        :param str created_at: The date the secret ACL was created.
        :param bool project_access: Whether the secret is accessible project wide.
               Defaults to `true`.
        :param str updated_at: The date the secret ACL was last updated.
        :param Sequence[str] users: The list of user IDs, which are allowed to access the
               secret, when `project_access` is set to `false`.
        """
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if project_access is not None:
            pulumi.set(__self__, "project_access", project_access)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[str]:
        """
        The date the secret ACL was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="projectAccess")
    def project_access(self) -> Optional[bool]:
        """
        Whether the secret is accessible project wide.
        Defaults to `true`.
        """
        return pulumi.get(self, "project_access")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[str]:
        """
        The date the secret ACL was last updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        """
        The list of user IDs, which are allowed to access the
        secret, when `project_access` is set to `false`.
        """
        return pulumi.get(self, "users")


@pulumi.output_type
class GetContainerAclResult(dict):
    def __init__(__self__, *,
                 read: 'outputs.GetContainerAclReadResult'):
        pulumi.set(__self__, "read", read)

    @property
    @pulumi.getter
    def read(self) -> 'outputs.GetContainerAclReadResult':
        return pulumi.get(self, "read")


@pulumi.output_type
class GetContainerAclReadResult(dict):
    def __init__(__self__, *,
                 created_at: str,
                 updated_at: str,
                 project_access: Optional[bool] = None,
                 users: Optional[Sequence[str]] = None):
        """
        :param str created_at: The date the container ACL was created.
        :param str updated_at: The date the container ACL was last updated.
        :param bool project_access: Whether the container is accessible project wide.
        :param Sequence[str] users: The list of user IDs, which are allowed to access the container,
               when `project_access` is set to `false`.
        """
        pulumi.set(__self__, "created_at", created_at)
        pulumi.set(__self__, "updated_at", updated_at)
        if project_access is not None:
            pulumi.set(__self__, "project_access", project_access)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The date the container ACL was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The date the container ACL was last updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="projectAccess")
    def project_access(self) -> Optional[bool]:
        """
        Whether the container is accessible project wide.
        """
        return pulumi.get(self, "project_access")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        """
        The list of user IDs, which are allowed to access the container,
        when `project_access` is set to `false`.
        """
        return pulumi.get(self, "users")


@pulumi.output_type
class GetContainerConsumerResult(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 url: Optional[str] = None):
        """
        :param str name: The Container name.
        :param str url: The consumer URL.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if url is not None:
            pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The Container name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def url(self) -> Optional[str]:
        """
        The consumer URL.
        """
        return pulumi.get(self, "url")


@pulumi.output_type
class GetContainerSecretRefResult(dict):
    def __init__(__self__, *,
                 name: Optional[str] = None,
                 secret_ref: Optional[str] = None):
        """
        :param str name: The Container name.
        :param str secret_ref: The secret reference / where to find the secret, URL.
        """
        if name is not None:
            pulumi.set(__self__, "name", name)
        if secret_ref is not None:
            pulumi.set(__self__, "secret_ref", secret_ref)

    @property
    @pulumi.getter
    def name(self) -> Optional[str]:
        """
        The Container name.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="secretRef")
    def secret_ref(self) -> Optional[str]:
        """
        The secret reference / where to find the secret, URL.
        """
        return pulumi.get(self, "secret_ref")


@pulumi.output_type
class GetSecretAclResult(dict):
    def __init__(__self__, *,
                 read: 'outputs.GetSecretAclReadResult'):
        pulumi.set(__self__, "read", read)

    @property
    @pulumi.getter
    def read(self) -> 'outputs.GetSecretAclReadResult':
        return pulumi.get(self, "read")


@pulumi.output_type
class GetSecretAclReadResult(dict):
    def __init__(__self__, *,
                 created_at: str,
                 updated_at: str,
                 project_access: Optional[bool] = None,
                 users: Optional[Sequence[str]] = None):
        """
        :param str created_at: The date the secret ACL was created.
        :param str updated_at: The date the secret ACL was last updated.
        :param bool project_access: Whether the secret is accessible project wide.
        :param Sequence[str] users: The list of user IDs, which are allowed to access the secret, when
               `project_access` is set to `false`.
        """
        pulumi.set(__self__, "created_at", created_at)
        pulumi.set(__self__, "updated_at", updated_at)
        if project_access is not None:
            pulumi.set(__self__, "project_access", project_access)
        if users is not None:
            pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The date the secret ACL was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        The date the secret ACL was last updated.
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="projectAccess")
    def project_access(self) -> Optional[bool]:
        """
        Whether the secret is accessible project wide.
        """
        return pulumi.get(self, "project_access")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence[str]]:
        """
        The list of user IDs, which are allowed to access the secret, when
        `project_access` is set to `false`.
        """
        return pulumi.get(self, "users")


