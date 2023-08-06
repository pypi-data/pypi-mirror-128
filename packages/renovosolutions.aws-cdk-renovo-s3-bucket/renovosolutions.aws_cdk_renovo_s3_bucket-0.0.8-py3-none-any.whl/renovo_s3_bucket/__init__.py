'''
# cdk-library-renovo-s3-bucket

An AWS CDK construct library to create S3 buckets with some desirable defaults. Also provides some other helpers to make it easier to apply certain common rules we use.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_s3
import aws_cdk.core


@jsii.interface(
    jsii_type="@renovosolutions/cdk-library-renovo-s3-bucket.IRenovoS3BucketProps"
)
class IRenovoS3BucketProps(typing_extensions.Protocol):
    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lifecycleRules")
    def lifecycle_rules(self) -> typing.List[aws_cdk.aws_s3.LifecycleRule]:
        '''Rules that define how Amazon S3 manages objects during their lifetime.'''
        ...

    @lifecycle_rules.setter
    def lifecycle_rules(self, value: typing.List[aws_cdk.aws_s3.LifecycleRule]) -> None:
        ...

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket.'''
        ...

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IRenovoS3BucketPropsProxy:
    __jsii_type__: typing.ClassVar[str] = "@renovosolutions/cdk-library-renovo-s3-bucket.IRenovoS3BucketProps"

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="lifecycleRules")
    def lifecycle_rules(self) -> typing.List[aws_cdk.aws_s3.LifecycleRule]:
        '''Rules that define how Amazon S3 manages objects during their lifetime.'''
        return typing.cast(typing.List[aws_cdk.aws_s3.LifecycleRule], jsii.get(self, "lifecycleRules"))

    @lifecycle_rules.setter
    def lifecycle_rules(self, value: typing.List[aws_cdk.aws_s3.LifecycleRule]) -> None:
        jsii.set(self, "lifecycleRules", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the bucket.'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "name", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRenovoS3BucketProps).__jsii_proxy_class__ = lambda : _IRenovoS3BucketPropsProxy


class RenovoS3Bucket(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@renovosolutions/cdk-library-renovo-s3-bucket.RenovoS3Bucket",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        props: IRenovoS3BucketProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.Bucket:
        return typing.cast(aws_cdk.aws_s3.Bucket, jsii.get(self, "bucket"))


__all__ = [
    "IRenovoS3BucketProps",
    "RenovoS3Bucket",
]

publication.publish()
