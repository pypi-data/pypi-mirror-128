'''
# AWS::Wisdom Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
# Example automatically generated from non-compiling source. May contain errors.
from monocdk import aws_wisdom as wisdom
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

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAssistant(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wisdom.CfnAssistant",
):
    '''A CloudFormation ``AWS::Wisdom::Assistant``.

    :cloudformationResource: AWS::Wisdom::Assistant
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Wisdom::Assistant``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: ``AWS::Wisdom::Assistant.Name``.
        :param type: ``AWS::Wisdom::Assistant.Type``.
        :param description: ``AWS::Wisdom::Assistant.Description``.
        :param server_side_encryption_configuration: ``AWS::Wisdom::Assistant.ServerSideEncryptionConfiguration``.
        :param tags: ``AWS::Wisdom::Assistant.Tags``.
        '''
        props = CfnAssistantProps(
            name=name,
            type=type,
            description=description,
            server_side_encryption_configuration=server_side_encryption_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAssistantArn")
    def attr_assistant_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssistantArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAssistantId")
    def attr_assistant_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssistantId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Wisdom::Assistant.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Wisdom::Assistant.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''``AWS::Wisdom::Assistant.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        jsii.set(self, "type", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Wisdom::Assistant.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::Assistant.ServerSideEncryptionConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-serversideencryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Optional[typing.Union["CfnAssistant.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_wisdom.CfnAssistant.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''
            :param kms_key_id: ``CfnAssistant.ServerSideEncryptionConfigurationProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistant-serversideencryptionconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''``CfnAssistant.ServerSideEncryptionConfigurationProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistant-serversideencryptionconfiguration.html#cfn-wisdom-assistant-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnAssistantAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wisdom.CfnAssistantAssociation",
):
    '''A CloudFormation ``AWS::Wisdom::AssistantAssociation``.

    :cloudformationResource: AWS::Wisdom::AssistantAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        assistant_id: builtins.str,
        association: typing.Union["CfnAssistantAssociation.AssociationDataProperty", _IResolvable_a771d0ef],
        association_type: builtins.str,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Wisdom::AssistantAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assistant_id: ``AWS::Wisdom::AssistantAssociation.AssistantId``.
        :param association: ``AWS::Wisdom::AssistantAssociation.Association``.
        :param association_type: ``AWS::Wisdom::AssistantAssociation.AssociationType``.
        :param tags: ``AWS::Wisdom::AssistantAssociation.Tags``.
        '''
        props = CfnAssistantAssociationProps(
            assistant_id=assistant_id,
            association=association,
            association_type=association_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAssistantArn")
    def attr_assistant_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssistantArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAssistantAssociationArn")
    def attr_assistant_association_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssistantAssociationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantAssociationArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrAssistantAssociationId")
    def attr_assistant_association_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: AssistantAssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssistantAssociationId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Wisdom::AssistantAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="assistantId")
    def assistant_id(self) -> builtins.str:
        '''``AWS::Wisdom::AssistantAssociation.AssistantId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-assistantid
        '''
        return typing.cast(builtins.str, jsii.get(self, "assistantId"))

    @assistant_id.setter
    def assistant_id(self, value: builtins.str) -> None:
        jsii.set(self, "assistantId", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="association")
    def association(
        self,
    ) -> typing.Union["CfnAssistantAssociation.AssociationDataProperty", _IResolvable_a771d0ef]:
        '''``AWS::Wisdom::AssistantAssociation.Association``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-association
        '''
        return typing.cast(typing.Union["CfnAssistantAssociation.AssociationDataProperty", _IResolvable_a771d0ef], jsii.get(self, "association"))

    @association.setter
    def association(
        self,
        value: typing.Union["CfnAssistantAssociation.AssociationDataProperty", _IResolvable_a771d0ef],
    ) -> None:
        jsii.set(self, "association", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="associationType")
    def association_type(self) -> builtins.str:
        '''``AWS::Wisdom::AssistantAssociation.AssociationType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-associationtype
        '''
        return typing.cast(builtins.str, jsii.get(self, "associationType"))

    @association_type.setter
    def association_type(self, value: builtins.str) -> None:
        jsii.set(self, "associationType", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_wisdom.CfnAssistantAssociation.AssociationDataProperty",
        jsii_struct_bases=[],
        name_mapping={"knowledge_base_id": "knowledgeBaseId"},
    )
    class AssociationDataProperty:
        def __init__(self, *, knowledge_base_id: builtins.str) -> None:
            '''
            :param knowledge_base_id: ``CfnAssistantAssociation.AssociationDataProperty.KnowledgeBaseId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistantassociation-associationdata.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "knowledge_base_id": knowledge_base_id,
            }

        @builtins.property
        def knowledge_base_id(self) -> builtins.str:
            '''``CfnAssistantAssociation.AssociationDataProperty.KnowledgeBaseId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-assistantassociation-associationdata.html#cfn-wisdom-assistantassociation-associationdata-knowledgebaseid
            '''
            result = self._values.get("knowledge_base_id")
            assert result is not None, "Required property 'knowledge_base_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssociationDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_wisdom.CfnAssistantAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "assistant_id": "assistantId",
        "association": "association",
        "association_type": "associationType",
        "tags": "tags",
    },
)
class CfnAssistantAssociationProps:
    def __init__(
        self,
        *,
        assistant_id: builtins.str,
        association: typing.Union[CfnAssistantAssociation.AssociationDataProperty, _IResolvable_a771d0ef],
        association_type: builtins.str,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Wisdom::AssistantAssociation``.

        :param assistant_id: ``AWS::Wisdom::AssistantAssociation.AssistantId``.
        :param association: ``AWS::Wisdom::AssistantAssociation.Association``.
        :param association_type: ``AWS::Wisdom::AssistantAssociation.AssociationType``.
        :param tags: ``AWS::Wisdom::AssistantAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "assistant_id": assistant_id,
            "association": association,
            "association_type": association_type,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assistant_id(self) -> builtins.str:
        '''``AWS::Wisdom::AssistantAssociation.AssistantId``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-assistantid
        '''
        result = self._values.get("assistant_id")
        assert result is not None, "Required property 'assistant_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def association(
        self,
    ) -> typing.Union[CfnAssistantAssociation.AssociationDataProperty, _IResolvable_a771d0ef]:
        '''``AWS::Wisdom::AssistantAssociation.Association``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-association
        '''
        result = self._values.get("association")
        assert result is not None, "Required property 'association' is missing"
        return typing.cast(typing.Union[CfnAssistantAssociation.AssociationDataProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def association_type(self) -> builtins.str:
        '''``AWS::Wisdom::AssistantAssociation.AssociationType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-associationtype
        '''
        result = self._values.get("association_type")
        assert result is not None, "Required property 'association_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Wisdom::AssistantAssociation.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistantassociation.html#cfn-wisdom-assistantassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssistantAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_wisdom.CfnAssistantProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "type": "type",
        "description": "description",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "tags": "tags",
    },
)
class CfnAssistantProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Wisdom::Assistant``.

        :param name: ``AWS::Wisdom::Assistant.Name``.
        :param type: ``AWS::Wisdom::Assistant.Type``.
        :param description: ``AWS::Wisdom::Assistant.Description``.
        :param server_side_encryption_configuration: ``AWS::Wisdom::Assistant.ServerSideEncryptionConfiguration``.
        :param tags: ``AWS::Wisdom::Assistant.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Wisdom::Assistant.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''``AWS::Wisdom::Assistant.Type``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Wisdom::Assistant.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::Assistant.ServerSideEncryptionConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnAssistant.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Wisdom::Assistant.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-assistant.html#cfn-wisdom-assistant-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssistantProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnKnowledgeBase(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_wisdom.CfnKnowledgeBase",
):
    '''A CloudFormation ``AWS::Wisdom::KnowledgeBase``.

    :cloudformationResource: AWS::Wisdom::KnowledgeBase
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        knowledge_base_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rendering_configuration: typing.Optional[typing.Union["CfnKnowledgeBase.RenderingConfigurationProperty", _IResolvable_a771d0ef]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union["CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]] = None,
        source_configuration: typing.Optional[typing.Union["CfnKnowledgeBase.SourceConfigurationProperty", _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Create a new ``AWS::Wisdom::KnowledgeBase``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param knowledge_base_type: ``AWS::Wisdom::KnowledgeBase.KnowledgeBaseType``.
        :param name: ``AWS::Wisdom::KnowledgeBase.Name``.
        :param description: ``AWS::Wisdom::KnowledgeBase.Description``.
        :param rendering_configuration: ``AWS::Wisdom::KnowledgeBase.RenderingConfiguration``.
        :param server_side_encryption_configuration: ``AWS::Wisdom::KnowledgeBase.ServerSideEncryptionConfiguration``.
        :param source_configuration: ``AWS::Wisdom::KnowledgeBase.SourceConfiguration``.
        :param tags: ``AWS::Wisdom::KnowledgeBase.Tags``.
        '''
        props = CfnKnowledgeBaseProps(
            knowledge_base_type=knowledge_base_type,
            name=name,
            description=description,
            rendering_configuration=rendering_configuration,
            server_side_encryption_configuration=server_side_encryption_configuration,
            source_configuration=source_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty # type: ignore[misc]
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrKnowledgeBaseArn")
    def attr_knowledge_base_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: KnowledgeBaseArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKnowledgeBaseArn"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="attrKnowledgeBaseId")
    def attr_knowledge_base_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: KnowledgeBaseId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrKnowledgeBaseId"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''``AWS::Wisdom::KnowledgeBase.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="knowledgeBaseType")
    def knowledge_base_type(self) -> builtins.str:
        '''``AWS::Wisdom::KnowledgeBase.KnowledgeBaseType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-knowledgebasetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "knowledgeBaseType"))

    @knowledge_base_type.setter
    def knowledge_base_type(self, value: builtins.str) -> None:
        jsii.set(self, "knowledgeBaseType", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''``AWS::Wisdom::KnowledgeBase.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Wisdom::KnowledgeBase.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="renderingConfiguration")
    def rendering_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnKnowledgeBase.RenderingConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::KnowledgeBase.RenderingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-renderingconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnKnowledgeBase.RenderingConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "renderingConfiguration"))

    @rendering_configuration.setter
    def rendering_configuration(
        self,
        value: typing.Optional[typing.Union["CfnKnowledgeBase.RenderingConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "renderingConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="serverSideEncryptionConfiguration")
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::KnowledgeBase.ServerSideEncryptionConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "serverSideEncryptionConfiguration"))

    @server_side_encryption_configuration.setter
    def server_side_encryption_configuration(
        self,
        value: typing.Optional[typing.Union["CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "serverSideEncryptionConfiguration", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceConfiguration")
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnKnowledgeBase.SourceConfigurationProperty", _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::KnowledgeBase.SourceConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-sourceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnKnowledgeBase.SourceConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "sourceConfiguration"))

    @source_configuration.setter
    def source_configuration(
        self,
        value: typing.Optional[typing.Union["CfnKnowledgeBase.SourceConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        jsii.set(self, "sourceConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_wisdom.CfnKnowledgeBase.AppIntegrationsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "app_integration_arn": "appIntegrationArn",
            "object_fields": "objectFields",
        },
    )
    class AppIntegrationsConfigurationProperty:
        def __init__(
            self,
            *,
            app_integration_arn: builtins.str,
            object_fields: typing.Sequence[builtins.str],
        ) -> None:
            '''
            :param app_integration_arn: ``CfnKnowledgeBase.AppIntegrationsConfigurationProperty.AppIntegrationArn``.
            :param object_fields: ``CfnKnowledgeBase.AppIntegrationsConfigurationProperty.ObjectFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {
                "app_integration_arn": app_integration_arn,
                "object_fields": object_fields,
            }

        @builtins.property
        def app_integration_arn(self) -> builtins.str:
            '''``CfnKnowledgeBase.AppIntegrationsConfigurationProperty.AppIntegrationArn``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html#cfn-wisdom-knowledgebase-appintegrationsconfiguration-appintegrationarn
            '''
            result = self._values.get("app_integration_arn")
            assert result is not None, "Required property 'app_integration_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def object_fields(self) -> typing.List[builtins.str]:
            '''``CfnKnowledgeBase.AppIntegrationsConfigurationProperty.ObjectFields``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-appintegrationsconfiguration.html#cfn-wisdom-knowledgebase-appintegrationsconfiguration-objectfields
            '''
            result = self._values.get("object_fields")
            assert result is not None, "Required property 'object_fields' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AppIntegrationsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wisdom.CfnKnowledgeBase.RenderingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"template_uri": "templateUri"},
    )
    class RenderingConfigurationProperty:
        def __init__(
            self,
            *,
            template_uri: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param template_uri: ``CfnKnowledgeBase.RenderingConfigurationProperty.TemplateUri``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-renderingconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if template_uri is not None:
                self._values["template_uri"] = template_uri

        @builtins.property
        def template_uri(self) -> typing.Optional[builtins.str]:
            '''``CfnKnowledgeBase.RenderingConfigurationProperty.TemplateUri``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-renderingconfiguration.html#cfn-wisdom-knowledgebase-renderingconfiguration-templateuri
            '''
            result = self._values.get("template_uri")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RenderingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wisdom.CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"kms_key_id": "kmsKeyId"},
    )
    class ServerSideEncryptionConfigurationProperty:
        def __init__(self, *, kms_key_id: typing.Optional[builtins.str] = None) -> None:
            '''
            :param kms_key_id: ``CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-serversideencryptionconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if kms_key_id is not None:
                self._values["kms_key_id"] = kms_key_id

        @builtins.property
        def kms_key_id(self) -> typing.Optional[builtins.str]:
            '''``CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty.KmsKeyId``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-serversideencryptionconfiguration.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration-kmskeyid
            '''
            result = self._values.get("kms_key_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSideEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_wisdom.CfnKnowledgeBase.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"app_integrations": "appIntegrations"},
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            app_integrations: typing.Optional[typing.Union["CfnKnowledgeBase.AppIntegrationsConfigurationProperty", _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''
            :param app_integrations: ``CfnKnowledgeBase.SourceConfigurationProperty.AppIntegrations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html
            '''
            self._values: typing.Dict[str, typing.Any] = {}
            if app_integrations is not None:
                self._values["app_integrations"] = app_integrations

        @builtins.property
        def app_integrations(
            self,
        ) -> typing.Optional[typing.Union["CfnKnowledgeBase.AppIntegrationsConfigurationProperty", _IResolvable_a771d0ef]]:
            '''``CfnKnowledgeBase.SourceConfigurationProperty.AppIntegrations``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wisdom-knowledgebase-sourceconfiguration.html#cfn-wisdom-knowledgebase-sourceconfiguration-appintegrations
            '''
            result = self._values.get("app_integrations")
            return typing.cast(typing.Optional[typing.Union["CfnKnowledgeBase.AppIntegrationsConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_wisdom.CfnKnowledgeBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "knowledge_base_type": "knowledgeBaseType",
        "name": "name",
        "description": "description",
        "rendering_configuration": "renderingConfiguration",
        "server_side_encryption_configuration": "serverSideEncryptionConfiguration",
        "source_configuration": "sourceConfiguration",
        "tags": "tags",
    },
)
class CfnKnowledgeBaseProps:
    def __init__(
        self,
        *,
        knowledge_base_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rendering_configuration: typing.Optional[typing.Union[CfnKnowledgeBase.RenderingConfigurationProperty, _IResolvable_a771d0ef]] = None,
        server_side_encryption_configuration: typing.Optional[typing.Union[CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]] = None,
        source_configuration: typing.Optional[typing.Union[CfnKnowledgeBase.SourceConfigurationProperty, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[_CfnTag_95fbdc29]] = None,
    ) -> None:
        '''Properties for defining a ``AWS::Wisdom::KnowledgeBase``.

        :param knowledge_base_type: ``AWS::Wisdom::KnowledgeBase.KnowledgeBaseType``.
        :param name: ``AWS::Wisdom::KnowledgeBase.Name``.
        :param description: ``AWS::Wisdom::KnowledgeBase.Description``.
        :param rendering_configuration: ``AWS::Wisdom::KnowledgeBase.RenderingConfiguration``.
        :param server_side_encryption_configuration: ``AWS::Wisdom::KnowledgeBase.ServerSideEncryptionConfiguration``.
        :param source_configuration: ``AWS::Wisdom::KnowledgeBase.SourceConfiguration``.
        :param tags: ``AWS::Wisdom::KnowledgeBase.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "knowledge_base_type": knowledge_base_type,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if rendering_configuration is not None:
            self._values["rendering_configuration"] = rendering_configuration
        if server_side_encryption_configuration is not None:
            self._values["server_side_encryption_configuration"] = server_side_encryption_configuration
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def knowledge_base_type(self) -> builtins.str:
        '''``AWS::Wisdom::KnowledgeBase.KnowledgeBaseType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-knowledgebasetype
        '''
        result = self._values.get("knowledge_base_type")
        assert result is not None, "Required property 'knowledge_base_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''``AWS::Wisdom::KnowledgeBase.Name``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''``AWS::Wisdom::KnowledgeBase.Description``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rendering_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnKnowledgeBase.RenderingConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::KnowledgeBase.RenderingConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-renderingconfiguration
        '''
        result = self._values.get("rendering_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnKnowledgeBase.RenderingConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def server_side_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::KnowledgeBase.ServerSideEncryptionConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-serversideencryptionconfiguration
        '''
        result = self._values.get("server_side_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnKnowledgeBase.ServerSideEncryptionConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnKnowledgeBase.SourceConfigurationProperty, _IResolvable_a771d0ef]]:
        '''``AWS::Wisdom::KnowledgeBase.SourceConfiguration``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnKnowledgeBase.SourceConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''``AWS::Wisdom::KnowledgeBase.Tags``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wisdom-knowledgebase.html#cfn-wisdom-knowledgebase-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnKnowledgeBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssistant",
    "CfnAssistantAssociation",
    "CfnAssistantAssociationProps",
    "CfnAssistantProps",
    "CfnKnowledgeBase",
    "CfnKnowledgeBaseProps",
]

publication.publish()
