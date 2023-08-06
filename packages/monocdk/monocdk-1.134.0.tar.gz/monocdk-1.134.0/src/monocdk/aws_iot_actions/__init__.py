'''
# Actions for AWS IoT Rule

This library contains integration classes to send data to any number of
supported AWS Services. Instances of these classes should be passed to
`TopicRule` defined in `@aws-cdk/aws-iot`.

Currently supported are:

* Invoke a Lambda function
* Put objects to a S3 bucket
* Put logs to CloudWatch Logs
* Put records to Kinesis Data Firehose stream

## Invoke a Lambda function

The code snippet below creates an AWS IoT Rule that invoke a Lambda function
when it is triggered.

```python
# Example automatically generated from non-compiling source. May contain errors.
import monocdk.aws_iot as iot
import monocdk.aws_iot_actions as actions
import monocdk.aws_lambda as lambda_


func = lambda_.Function(self, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_14_X,
    handler="index.handler",
    code=lambda_.Code.from_inline("""
            exports.handler = (event) => {
              console.log("It is test for lambda action of AWS IoT Rule.", event);
            };""")
)

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
    actions=[actions.LambdaFunctionAction(func)]
)
```

## Put objects to a S3 bucket

The code snippet below creates an AWS IoT Rule that put objects to a S3 bucket
when it is triggered.

```python
# Example automatically generated from non-compiling source. May contain errors.
import monocdk.aws_iot as iot
import monocdk.aws_iot_actions as actions
import monocdk.aws_s3 as s3


bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[actions.S3PutObjectAction(bucket)]
)
```

The property `key` of `S3PutObjectAction` is given the value `${topic()}/${timestamp()}` by default. This `${topic()}`
and `${timestamp()}` is called Substitution templates. For more information see
[this documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html).
In above sample, `${topic()}` is replaced by a given MQTT topic as `device/001/data`. And `${timestamp()}` is replaced
by the number of the current timestamp in milliseconds as `1636289461203`. So if the MQTT broker receives an MQTT topic
`device/001/data` on `2021-11-07T00:00:00.000Z`, the S3 bucket object will be put to `device/001/data/1636243200000`.

You can also set specific `key` as following:

```python
# Example automatically generated from non-compiling source. May contain errors.
iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.S3PutObjectAction(bucket,
            key="${year}/${month}/${day}/${topic(2)}"
        )
    ]
)
```

If you wanna set access control to the S3 bucket object, you can specify `accessControl` as following:

```python
# Example automatically generated from non-compiling source. May contain errors.
iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.S3PutObjectAction(bucket,
            access_control=s3.BucketAccessControl.PUBLIC_READ
        )
    ]
)
```

## Put logs to CloudWatch Logs

The code snippet below creates an AWS IoT Rule that put logs to CloudWatch Logs
when it is triggered.

```python
import monocdk.aws_iot as iot
import monocdk.aws_iot_actions as actions
import monocdk.aws_logs as logs


log_group = logs.LogGroup(self, "MyLogGroup")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[actions.CloudWatchLogsAction(log_group)]
)
```

## Put records to Kinesis Data Firehose stream

The code snippet below creates an AWS IoT Rule that put records to Put records
to Kinesis Data Firehose stream when it is triggered.

```python
# Example automatically generated from non-compiling source. May contain errors.
import monocdk.aws_iot as iot
import monocdk.aws_iot_actions as actions
import monocdk.aws_s3 as s3
import monocdk.aws_kinesisfirehose as firehose
import monocdk.aws_kinesisfirehose_destinations as destinations


bucket = s3.Bucket(self, "MyBucket")
stream = firehose.DeliveryStream(self, "MyStream",
    destinations=[destinations.S3Bucket(bucket)]
)

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.FirehoseStreamAction(stream,
            batch_mode=True,
            record_separator=actions.FirehoseStreamRecordSeparator.NEWLINE
        )
    ]
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from .._jsii import *

from ..aws_iam import IRole as _IRole_59af6f50
from ..aws_iot import (
    ActionConfig as _ActionConfig_9dc7cb16,
    IAction as _IAction_25dbea23,
    ITopicRule as _ITopicRule_96d74f80,
)
from ..aws_kinesisfirehose import IDeliveryStream as _IDeliveryStream_2a44232c
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_logs import ILogGroup as _ILogGroup_846e17a0
from ..aws_s3 import (
    BucketAccessControl as _BucketAccessControl_a8cb5bce, IBucket as _IBucket_73486e29
)


@jsii.implements(_IAction_25dbea23)
class CloudWatchLogsAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.CloudWatchLogsAction",
):
    '''(experimental) The action to send data to Amazon CloudWatch Logs.

    :stability: experimental

    Example::

        import monocdk.aws_iot as iot
        import monocdk.aws_iot_actions as actions
        import monocdk.aws_logs as logs
        
        
        log_group = logs.LogGroup(self, "MyLogGroup")
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
            error_action=actions.CloudWatchLogsAction(log_group)
        )
    '''

    def __init__(
        self,
        log_group: _ILogGroup_846e17a0,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param log_group: The CloudWatch log group to which the action sends data.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        props = CloudWatchLogsActionProps(role=role)

        jsii.create(self.__class__, self, [log_group, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.CommonActionProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class CommonActionProps:
    def __init__(self, *, role: typing.Optional[_IRole_59af6f50] = None) -> None:
        '''(experimental) Common properties shared by Actions it access to AWS service.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_iot_actions as iot_actions
            
            # role is of type Role
            
            common_action_props = iot_actions.CommonActionProps(
                role=role
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_25dbea23)
class FirehoseStreamAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.FirehoseStreamAction",
):
    '''(experimental) The action to put the record from an MQTT message to the Kinesis Data Firehose stream.

    :stability: experimental

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk.aws_iot as iot
        import monocdk.aws_iot_actions as actions
        import monocdk.aws_s3 as s3
        import monocdk.aws_kinesisfirehose as firehose
        import monocdk.aws_kinesisfirehose_destinations as destinations
        
        
        bucket = s3.Bucket(self, "MyBucket")
        stream = firehose.DeliveryStream(self, "MyStream",
            destinations=[destinations.S3Bucket(bucket)]
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.FirehoseStreamAction(stream,
                    batch_mode=True,
                    record_separator=actions.FirehoseStreamRecordSeparator.NEWLINE
                )
            ]
        )
    '''

    def __init__(
        self,
        stream: _IDeliveryStream_2a44232c,
        *,
        batch_mode: typing.Optional[builtins.bool] = None,
        record_separator: typing.Optional["FirehoseStreamRecordSeparator"] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param stream: The Kinesis Data Firehose stream to which to put records.
        :param batch_mode: (experimental) Whether to deliver the Kinesis Data Firehose stream as a batch by using ``PutRecordBatch``. When batchMode is true and the rule's SQL statement evaluates to an Array, each Array element forms one record in the PutRecordBatch request. The resulting array can't have more than 500 records. Default: false
        :param record_separator: (experimental) A character separator that will be used to separate records written to the Kinesis Data Firehose stream. Default: - none -- the stream does not use a separator
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        props = FirehoseStreamActionProps(
            batch_mode=batch_mode, record_separator=record_separator, role=role
        )

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.FirehoseStreamActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "batch_mode": "batchMode",
        "record_separator": "recordSeparator",
    },
)
class FirehoseStreamActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        batch_mode: typing.Optional[builtins.bool] = None,
        record_separator: typing.Optional["FirehoseStreamRecordSeparator"] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for the Kinesis Data Firehose stream.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param batch_mode: (experimental) Whether to deliver the Kinesis Data Firehose stream as a batch by using ``PutRecordBatch``. When batchMode is true and the rule's SQL statement evaluates to an Array, each Array element forms one record in the PutRecordBatch request. The resulting array can't have more than 500 records. Default: false
        :param record_separator: (experimental) A character separator that will be used to separate records written to the Kinesis Data Firehose stream. Default: - none -- the stream does not use a separator

        :stability: experimental

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            import monocdk.aws_iot as iot
            import monocdk.aws_iot_actions as actions
            import monocdk.aws_s3 as s3
            import monocdk.aws_kinesisfirehose as firehose
            import monocdk.aws_kinesisfirehose_destinations as destinations
            
            
            bucket = s3.Bucket(self, "MyBucket")
            stream = firehose.DeliveryStream(self, "MyStream",
                destinations=[destinations.S3Bucket(bucket)]
            )
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
                actions=[
                    actions.FirehoseStreamAction(stream,
                        batch_mode=True,
                        record_separator=actions.FirehoseStreamRecordSeparator.NEWLINE
                    )
                ]
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if record_separator is not None:
            self._values["record_separator"] = record_separator

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def batch_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to deliver the Kinesis Data Firehose stream as a batch by using ``PutRecordBatch``.

        When batchMode is true and the rule's SQL statement evaluates to an Array, each Array
        element forms one record in the PutRecordBatch request. The resulting array can't have
        more than 500 records.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_separator(self) -> typing.Optional["FirehoseStreamRecordSeparator"]:
        '''(experimental) A character separator that will be used to separate records written to the Kinesis Data Firehose stream.

        :default: - none -- the stream does not use a separator

        :stability: experimental
        '''
        result = self._values.get("record_separator")
        return typing.cast(typing.Optional["FirehoseStreamRecordSeparator"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirehoseStreamActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_iot_actions.FirehoseStreamRecordSeparator")
class FirehoseStreamRecordSeparator(enum.Enum):
    '''(experimental) Record Separator to be used to separate records.

    :stability: experimental

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk.aws_iot as iot
        import monocdk.aws_iot_actions as actions
        import monocdk.aws_s3 as s3
        import monocdk.aws_kinesisfirehose as firehose
        import monocdk.aws_kinesisfirehose_destinations as destinations
        
        
        bucket = s3.Bucket(self, "MyBucket")
        stream = firehose.DeliveryStream(self, "MyStream",
            destinations=[destinations.S3Bucket(bucket)]
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.FirehoseStreamAction(stream,
                    batch_mode=True,
                    record_separator=actions.FirehoseStreamRecordSeparator.NEWLINE
                )
            ]
        )
    '''

    NEWLINE = "NEWLINE"
    '''(experimental) Separate by a new line.

    :stability: experimental
    '''
    TAB = "TAB"
    '''(experimental) Separate by a tab.

    :stability: experimental
    '''
    WINDOWS_NEWLINE = "WINDOWS_NEWLINE"
    '''(experimental) Separate by a windows new line.

    :stability: experimental
    '''
    COMMA = "COMMA"
    '''(experimental) Separate by a commma.

    :stability: experimental
    '''


@jsii.implements(_IAction_25dbea23)
class LambdaFunctionAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.LambdaFunctionAction",
):
    '''(experimental) The action to invoke an AWS Lambda function, passing in an MQTT message.

    :stability: experimental

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk.aws_iot as iot
        import monocdk.aws_iot_actions as actions
        import monocdk.aws_lambda as lambda_
        
        
        func = lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_inline("""
                    exports.handler = (event) => {
                      console.log("It is test for lambda action of AWS IoT Rule.", event);
                    };""")
        )
        
        iot.TopicRule(self, "TopicRule",
            topic_rule_name="MyTopicRule",  # optional
            description="invokes the lambda finction",  # optional
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
            actions=[actions.LambdaFunctionAction(func)]
        )
    '''

    def __init__(self, func: _IFunction_6e14f09e) -> None:
        '''
        :param func: The lambda function to be invoked by this action.

        :stability: experimental
        '''
        jsii.create(self.__class__, self, [func])

    @jsii.member(jsii_name="bind")
    def bind(self, topic_rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param topic_rule: -

        :stability: experimental
        '''
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [topic_rule]))


@jsii.implements(_IAction_25dbea23)
class S3PutObjectAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iot_actions.S3PutObjectAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon S3 bucket.

    :stability: experimental

    Example::

        # Example automatically generated from non-compiling source. May contain errors.
        import monocdk.aws_iot as iot
        import monocdk.aws_iot_actions as actions
        import monocdk.aws_s3 as s3
        
        
        bucket = s3.Bucket(self, "MyBucket")
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
            actions=[actions.S3PutObjectAction(bucket)]
        )
    '''

    def __init__(
        self,
        bucket: _IBucket_73486e29,
        *,
        access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
        key: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param bucket: The Amazon S3 bucket to which to write data.
        :param access_control: (experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key. Default: None
        :param key: (experimental) The path to the file where the data is written. Supports substitution templates. Default: '${topic()}/${timestamp()}'
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        props = S3PutObjectActionProps(
            access_control=access_control, key=key, role=role
        )

        jsii.create(self.__class__, self, [bucket, props])

    @jsii.member(jsii_name="bind")
    def bind(self, rule: _ITopicRule_96d74f80) -> _ActionConfig_9dc7cb16:
        '''(experimental) Returns the topic rule action specification.

        :param rule: -

        :stability: experimental
        '''
        return typing.cast(_ActionConfig_9dc7cb16, jsii.invoke(self, "bind", [rule]))


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.S3PutObjectActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "access_control": "accessControl", "key": "key"},
)
class S3PutObjectActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_IRole_59af6f50] = None,
        access_control: typing.Optional[_BucketAccessControl_a8cb5bce] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for s3.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param access_control: (experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key. Default: None
        :param key: (experimental) The path to the file where the data is written. Supports substitution templates. Default: '${topic()}/${timestamp()}'

        :stability: experimental

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_iot_actions as iot_actions
            from monocdk import aws_s3 as s3
            
            # role is of type Role
            
            s3_put_object_action_props = iot_actions.S3PutObjectActionProps(
                access_control=s3.BucketAccessControl.PRIVATE,
                key="key",
                role=role
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if access_control is not None:
            self._values["access_control"] = access_control
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def access_control(self) -> typing.Optional[_BucketAccessControl_a8cb5bce]:
        '''(experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key.

        :default: None

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_BucketAccessControl_a8cb5bce], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the file where the data is written.

        Supports substitution templates.

        :default: '${topic()}/${timestamp()}'

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3PutObjectActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iot_actions.CloudWatchLogsActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role"},
)
class CloudWatchLogsActionProps(CommonActionProps):
    def __init__(self, *, role: typing.Optional[_IRole_59af6f50] = None) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch Logs.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import aws_iot_actions as iot_actions
            
            # role is of type Role
            
            cloud_watch_logs_action_props = iot_actions.CloudWatchLogsActionProps(
                role=role
            )
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchLogsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudWatchLogsAction",
    "CloudWatchLogsActionProps",
    "CommonActionProps",
    "FirehoseStreamAction",
    "FirehoseStreamActionProps",
    "FirehoseStreamRecordSeparator",
    "LambdaFunctionAction",
    "S3PutObjectAction",
    "S3PutObjectActionProps",
]

publication.publish()
