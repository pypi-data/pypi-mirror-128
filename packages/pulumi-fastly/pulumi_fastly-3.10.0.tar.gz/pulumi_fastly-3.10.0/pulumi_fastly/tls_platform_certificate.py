# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['TlsPlatformCertificateArgs', 'TlsPlatformCertificate']

@pulumi.input_type
class TlsPlatformCertificateArgs:
    def __init__(__self__, *,
                 certificate_body: pulumi.Input[str],
                 configuration_id: pulumi.Input[str],
                 intermediates_blob: pulumi.Input[str],
                 allow_untrusted_root: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a TlsPlatformCertificate resource.
        :param pulumi.Input[str] certificate_body: PEM-formatted certificate.
        :param pulumi.Input[str] configuration_id: ID of TLS configuration to be used to terminate TLS traffic.
        :param pulumi.Input[str] intermediates_blob: PEM-formatted certificate chain from the `certificate_body` to its root.
        :param pulumi.Input[bool] allow_untrusted_root: Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        """
        pulumi.set(__self__, "certificate_body", certificate_body)
        pulumi.set(__self__, "configuration_id", configuration_id)
        pulumi.set(__self__, "intermediates_blob", intermediates_blob)
        if allow_untrusted_root is not None:
            pulumi.set(__self__, "allow_untrusted_root", allow_untrusted_root)

    @property
    @pulumi.getter(name="certificateBody")
    def certificate_body(self) -> pulumi.Input[str]:
        """
        PEM-formatted certificate.
        """
        return pulumi.get(self, "certificate_body")

    @certificate_body.setter
    def certificate_body(self, value: pulumi.Input[str]):
        pulumi.set(self, "certificate_body", value)

    @property
    @pulumi.getter(name="configurationId")
    def configuration_id(self) -> pulumi.Input[str]:
        """
        ID of TLS configuration to be used to terminate TLS traffic.
        """
        return pulumi.get(self, "configuration_id")

    @configuration_id.setter
    def configuration_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "configuration_id", value)

    @property
    @pulumi.getter(name="intermediatesBlob")
    def intermediates_blob(self) -> pulumi.Input[str]:
        """
        PEM-formatted certificate chain from the `certificate_body` to its root.
        """
        return pulumi.get(self, "intermediates_blob")

    @intermediates_blob.setter
    def intermediates_blob(self, value: pulumi.Input[str]):
        pulumi.set(self, "intermediates_blob", value)

    @property
    @pulumi.getter(name="allowUntrustedRoot")
    def allow_untrusted_root(self) -> Optional[pulumi.Input[bool]]:
        """
        Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        """
        return pulumi.get(self, "allow_untrusted_root")

    @allow_untrusted_root.setter
    def allow_untrusted_root(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_untrusted_root", value)


@pulumi.input_type
class _TlsPlatformCertificateState:
    def __init__(__self__, *,
                 allow_untrusted_root: Optional[pulumi.Input[bool]] = None,
                 certificate_body: Optional[pulumi.Input[str]] = None,
                 configuration_id: Optional[pulumi.Input[str]] = None,
                 created_at: Optional[pulumi.Input[str]] = None,
                 domains: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 intermediates_blob: Optional[pulumi.Input[str]] = None,
                 not_after: Optional[pulumi.Input[str]] = None,
                 not_before: Optional[pulumi.Input[str]] = None,
                 replace: Optional[pulumi.Input[bool]] = None,
                 updated_at: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering TlsPlatformCertificate resources.
        :param pulumi.Input[bool] allow_untrusted_root: Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        :param pulumi.Input[str] certificate_body: PEM-formatted certificate.
        :param pulumi.Input[str] configuration_id: ID of TLS configuration to be used to terminate TLS traffic.
        :param pulumi.Input[str] created_at: Timestamp (GMT) when the certificate was created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domains: All the domains (including wildcard domains) that are listed in any certificate's Subject Alternative Names (SAN) list.
        :param pulumi.Input[str] intermediates_blob: PEM-formatted certificate chain from the `certificate_body` to its root.
        :param pulumi.Input[str] not_after: Timestamp (GMT) when the certificate will expire.
        :param pulumi.Input[str] not_before: Timestamp (GMT) when the certificate will become valid.
        :param pulumi.Input[bool] replace: A recommendation from Fastly indicating the key associated with this certificate is in need of rotation.
        :param pulumi.Input[str] updated_at: Timestamp (GMT) when the certificate was last updated.
        """
        if allow_untrusted_root is not None:
            pulumi.set(__self__, "allow_untrusted_root", allow_untrusted_root)
        if certificate_body is not None:
            pulumi.set(__self__, "certificate_body", certificate_body)
        if configuration_id is not None:
            pulumi.set(__self__, "configuration_id", configuration_id)
        if created_at is not None:
            pulumi.set(__self__, "created_at", created_at)
        if domains is not None:
            pulumi.set(__self__, "domains", domains)
        if intermediates_blob is not None:
            pulumi.set(__self__, "intermediates_blob", intermediates_blob)
        if not_after is not None:
            pulumi.set(__self__, "not_after", not_after)
        if not_before is not None:
            pulumi.set(__self__, "not_before", not_before)
        if replace is not None:
            pulumi.set(__self__, "replace", replace)
        if updated_at is not None:
            pulumi.set(__self__, "updated_at", updated_at)

    @property
    @pulumi.getter(name="allowUntrustedRoot")
    def allow_untrusted_root(self) -> Optional[pulumi.Input[bool]]:
        """
        Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        """
        return pulumi.get(self, "allow_untrusted_root")

    @allow_untrusted_root.setter
    def allow_untrusted_root(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "allow_untrusted_root", value)

    @property
    @pulumi.getter(name="certificateBody")
    def certificate_body(self) -> Optional[pulumi.Input[str]]:
        """
        PEM-formatted certificate.
        """
        return pulumi.get(self, "certificate_body")

    @certificate_body.setter
    def certificate_body(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "certificate_body", value)

    @property
    @pulumi.getter(name="configurationId")
    def configuration_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of TLS configuration to be used to terminate TLS traffic.
        """
        return pulumi.get(self, "configuration_id")

    @configuration_id.setter
    def configuration_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "configuration_id", value)

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> Optional[pulumi.Input[str]]:
        """
        Timestamp (GMT) when the certificate was created.
        """
        return pulumi.get(self, "created_at")

    @created_at.setter
    def created_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "created_at", value)

    @property
    @pulumi.getter
    def domains(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        All the domains (including wildcard domains) that are listed in any certificate's Subject Alternative Names (SAN) list.
        """
        return pulumi.get(self, "domains")

    @domains.setter
    def domains(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "domains", value)

    @property
    @pulumi.getter(name="intermediatesBlob")
    def intermediates_blob(self) -> Optional[pulumi.Input[str]]:
        """
        PEM-formatted certificate chain from the `certificate_body` to its root.
        """
        return pulumi.get(self, "intermediates_blob")

    @intermediates_blob.setter
    def intermediates_blob(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "intermediates_blob", value)

    @property
    @pulumi.getter(name="notAfter")
    def not_after(self) -> Optional[pulumi.Input[str]]:
        """
        Timestamp (GMT) when the certificate will expire.
        """
        return pulumi.get(self, "not_after")

    @not_after.setter
    def not_after(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "not_after", value)

    @property
    @pulumi.getter(name="notBefore")
    def not_before(self) -> Optional[pulumi.Input[str]]:
        """
        Timestamp (GMT) when the certificate will become valid.
        """
        return pulumi.get(self, "not_before")

    @not_before.setter
    def not_before(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "not_before", value)

    @property
    @pulumi.getter
    def replace(self) -> Optional[pulumi.Input[bool]]:
        """
        A recommendation from Fastly indicating the key associated with this certificate is in need of rotation.
        """
        return pulumi.get(self, "replace")

    @replace.setter
    def replace(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "replace", value)

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> Optional[pulumi.Input[str]]:
        """
        Timestamp (GMT) when the certificate was last updated.
        """
        return pulumi.get(self, "updated_at")

    @updated_at.setter
    def updated_at(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "updated_at", value)


class TlsPlatformCertificate(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_untrusted_root: Optional[pulumi.Input[bool]] = None,
                 certificate_body: Optional[pulumi.Input[str]] = None,
                 configuration_id: Optional[pulumi.Input[str]] = None,
                 intermediates_blob: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Uploads a TLS certificate to the Fastly Platform TLS service.

        > Each TLS certificate **must** have its corresponding private key uploaded _prior_ to uploading the certificate.

        ## Example Usage

        Basic usage with self-signed CA:

        ```python
        import pulumi
        import pulumi_fastly as fastly
        import pulumi_tls as tls

        ca_key = tls.PrivateKey("caKey", algorithm="RSA")
        key_private_key = tls.PrivateKey("keyPrivateKey", algorithm="RSA")
        ca = tls.SelfSignedCert("ca",
            key_algorithm=ca_key.algorithm,
            private_key_pem=ca_key.private_key_pem,
            subjects=[tls.SelfSignedCertSubjectArgs(
                common_name="Example CA",
            )],
            is_ca_certificate=True,
            validity_period_hours=360,
            allowed_uses=[
                "cert_signing",
                "server_auth",
            ])
        example = tls.CertRequest("example",
            key_algorithm=key_private_key.algorithm,
            private_key_pem=key_private_key.private_key_pem,
            subjects=[tls.CertRequestSubjectArgs(
                common_name="example.com",
            )],
            dns_names=[
                "example.com",
                "www.example.com",
            ])
        cert_locally_signed_cert = tls.LocallySignedCert("certLocallySignedCert",
            cert_request_pem=example.cert_request_pem,
            ca_key_algorithm=ca_key.algorithm,
            ca_private_key_pem=ca_key.private_key_pem,
            ca_cert_pem=ca.cert_pem,
            validity_period_hours=360,
            allowed_uses=[
                "cert_signing",
                "server_auth",
            ])
        config = fastly.get_tls_configuration(tls_service="PLATFORM")
        key_tls_private_key = fastly.TlsPrivateKey("keyTlsPrivateKey", key_pem=key_private_key.private_key_pem)
        cert_tls_platform_certificate = fastly.TlsPlatformCertificate("certTlsPlatformCertificate",
            certificate_body=cert_locally_signed_cert.cert_pem,
            intermediates_blob=ca.cert_pem,
            configuration_id=config.id,
            allow_untrusted_root=True,
            opts=pulumi.ResourceOptions(depends_on=[key_tls_private_key]))
        ```

        ## Import

        A certificate can be imported using its Fastly certificate ID, e.g.

        ```sh
         $ pulumi import fastly:index/tlsPlatformCertificate:TlsPlatformCertificate demo xxxxxxxxxxx
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_untrusted_root: Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        :param pulumi.Input[str] certificate_body: PEM-formatted certificate.
        :param pulumi.Input[str] configuration_id: ID of TLS configuration to be used to terminate TLS traffic.
        :param pulumi.Input[str] intermediates_blob: PEM-formatted certificate chain from the `certificate_body` to its root.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: TlsPlatformCertificateArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Uploads a TLS certificate to the Fastly Platform TLS service.

        > Each TLS certificate **must** have its corresponding private key uploaded _prior_ to uploading the certificate.

        ## Example Usage

        Basic usage with self-signed CA:

        ```python
        import pulumi
        import pulumi_fastly as fastly
        import pulumi_tls as tls

        ca_key = tls.PrivateKey("caKey", algorithm="RSA")
        key_private_key = tls.PrivateKey("keyPrivateKey", algorithm="RSA")
        ca = tls.SelfSignedCert("ca",
            key_algorithm=ca_key.algorithm,
            private_key_pem=ca_key.private_key_pem,
            subjects=[tls.SelfSignedCertSubjectArgs(
                common_name="Example CA",
            )],
            is_ca_certificate=True,
            validity_period_hours=360,
            allowed_uses=[
                "cert_signing",
                "server_auth",
            ])
        example = tls.CertRequest("example",
            key_algorithm=key_private_key.algorithm,
            private_key_pem=key_private_key.private_key_pem,
            subjects=[tls.CertRequestSubjectArgs(
                common_name="example.com",
            )],
            dns_names=[
                "example.com",
                "www.example.com",
            ])
        cert_locally_signed_cert = tls.LocallySignedCert("certLocallySignedCert",
            cert_request_pem=example.cert_request_pem,
            ca_key_algorithm=ca_key.algorithm,
            ca_private_key_pem=ca_key.private_key_pem,
            ca_cert_pem=ca.cert_pem,
            validity_period_hours=360,
            allowed_uses=[
                "cert_signing",
                "server_auth",
            ])
        config = fastly.get_tls_configuration(tls_service="PLATFORM")
        key_tls_private_key = fastly.TlsPrivateKey("keyTlsPrivateKey", key_pem=key_private_key.private_key_pem)
        cert_tls_platform_certificate = fastly.TlsPlatformCertificate("certTlsPlatformCertificate",
            certificate_body=cert_locally_signed_cert.cert_pem,
            intermediates_blob=ca.cert_pem,
            configuration_id=config.id,
            allow_untrusted_root=True,
            opts=pulumi.ResourceOptions(depends_on=[key_tls_private_key]))
        ```

        ## Import

        A certificate can be imported using its Fastly certificate ID, e.g.

        ```sh
         $ pulumi import fastly:index/tlsPlatformCertificate:TlsPlatformCertificate demo xxxxxxxxxxx
        ```

        :param str resource_name: The name of the resource.
        :param TlsPlatformCertificateArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(TlsPlatformCertificateArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allow_untrusted_root: Optional[pulumi.Input[bool]] = None,
                 certificate_body: Optional[pulumi.Input[str]] = None,
                 configuration_id: Optional[pulumi.Input[str]] = None,
                 intermediates_blob: Optional[pulumi.Input[str]] = None,
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
            __props__ = TlsPlatformCertificateArgs.__new__(TlsPlatformCertificateArgs)

            __props__.__dict__["allow_untrusted_root"] = allow_untrusted_root
            if certificate_body is None and not opts.urn:
                raise TypeError("Missing required property 'certificate_body'")
            __props__.__dict__["certificate_body"] = certificate_body
            if configuration_id is None and not opts.urn:
                raise TypeError("Missing required property 'configuration_id'")
            __props__.__dict__["configuration_id"] = configuration_id
            if intermediates_blob is None and not opts.urn:
                raise TypeError("Missing required property 'intermediates_blob'")
            __props__.__dict__["intermediates_blob"] = intermediates_blob
            __props__.__dict__["created_at"] = None
            __props__.__dict__["domains"] = None
            __props__.__dict__["not_after"] = None
            __props__.__dict__["not_before"] = None
            __props__.__dict__["replace"] = None
            __props__.__dict__["updated_at"] = None
        super(TlsPlatformCertificate, __self__).__init__(
            'fastly:index/tlsPlatformCertificate:TlsPlatformCertificate',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allow_untrusted_root: Optional[pulumi.Input[bool]] = None,
            certificate_body: Optional[pulumi.Input[str]] = None,
            configuration_id: Optional[pulumi.Input[str]] = None,
            created_at: Optional[pulumi.Input[str]] = None,
            domains: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            intermediates_blob: Optional[pulumi.Input[str]] = None,
            not_after: Optional[pulumi.Input[str]] = None,
            not_before: Optional[pulumi.Input[str]] = None,
            replace: Optional[pulumi.Input[bool]] = None,
            updated_at: Optional[pulumi.Input[str]] = None) -> 'TlsPlatformCertificate':
        """
        Get an existing TlsPlatformCertificate resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_untrusted_root: Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        :param pulumi.Input[str] certificate_body: PEM-formatted certificate.
        :param pulumi.Input[str] configuration_id: ID of TLS configuration to be used to terminate TLS traffic.
        :param pulumi.Input[str] created_at: Timestamp (GMT) when the certificate was created.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] domains: All the domains (including wildcard domains) that are listed in any certificate's Subject Alternative Names (SAN) list.
        :param pulumi.Input[str] intermediates_blob: PEM-formatted certificate chain from the `certificate_body` to its root.
        :param pulumi.Input[str] not_after: Timestamp (GMT) when the certificate will expire.
        :param pulumi.Input[str] not_before: Timestamp (GMT) when the certificate will become valid.
        :param pulumi.Input[bool] replace: A recommendation from Fastly indicating the key associated with this certificate is in need of rotation.
        :param pulumi.Input[str] updated_at: Timestamp (GMT) when the certificate was last updated.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _TlsPlatformCertificateState.__new__(_TlsPlatformCertificateState)

        __props__.__dict__["allow_untrusted_root"] = allow_untrusted_root
        __props__.__dict__["certificate_body"] = certificate_body
        __props__.__dict__["configuration_id"] = configuration_id
        __props__.__dict__["created_at"] = created_at
        __props__.__dict__["domains"] = domains
        __props__.__dict__["intermediates_blob"] = intermediates_blob
        __props__.__dict__["not_after"] = not_after
        __props__.__dict__["not_before"] = not_before
        __props__.__dict__["replace"] = replace
        __props__.__dict__["updated_at"] = updated_at
        return TlsPlatformCertificate(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allowUntrustedRoot")
    def allow_untrusted_root(self) -> pulumi.Output[Optional[bool]]:
        """
        Disable checking whether the root of the certificate chain is trusted. Useful for development purposes to allow use of self-signed CAs. Defaults to false. Write-only on create.
        """
        return pulumi.get(self, "allow_untrusted_root")

    @property
    @pulumi.getter(name="certificateBody")
    def certificate_body(self) -> pulumi.Output[str]:
        """
        PEM-formatted certificate.
        """
        return pulumi.get(self, "certificate_body")

    @property
    @pulumi.getter(name="configurationId")
    def configuration_id(self) -> pulumi.Output[str]:
        """
        ID of TLS configuration to be used to terminate TLS traffic.
        """
        return pulumi.get(self, "configuration_id")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> pulumi.Output[str]:
        """
        Timestamp (GMT) when the certificate was created.
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter
    def domains(self) -> pulumi.Output[Sequence[str]]:
        """
        All the domains (including wildcard domains) that are listed in any certificate's Subject Alternative Names (SAN) list.
        """
        return pulumi.get(self, "domains")

    @property
    @pulumi.getter(name="intermediatesBlob")
    def intermediates_blob(self) -> pulumi.Output[str]:
        """
        PEM-formatted certificate chain from the `certificate_body` to its root.
        """
        return pulumi.get(self, "intermediates_blob")

    @property
    @pulumi.getter(name="notAfter")
    def not_after(self) -> pulumi.Output[str]:
        """
        Timestamp (GMT) when the certificate will expire.
        """
        return pulumi.get(self, "not_after")

    @property
    @pulumi.getter(name="notBefore")
    def not_before(self) -> pulumi.Output[str]:
        """
        Timestamp (GMT) when the certificate will become valid.
        """
        return pulumi.get(self, "not_before")

    @property
    @pulumi.getter
    def replace(self) -> pulumi.Output[bool]:
        """
        A recommendation from Fastly indicating the key associated with this certificate is in need of rotation.
        """
        return pulumi.get(self, "replace")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> pulumi.Output[str]:
        """
        Timestamp (GMT) when the certificate was last updated.
        """
        return pulumi.get(self, "updated_at")

