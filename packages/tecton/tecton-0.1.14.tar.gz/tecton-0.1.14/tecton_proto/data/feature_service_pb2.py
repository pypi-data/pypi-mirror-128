# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/feature_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tecton_proto.common import column_type_pb2 as tecton__proto_dot_common_dot_column__type__pb2
from tecton_proto.args import feature_service_pb2 as tecton__proto_dot_args_dot_feature__service__pb2
from tecton_proto.data import fco_metadata_pb2 as tecton__proto_dot_data_dot_fco__metadata__pb2
from tecton_proto.data import feature_package_pb2 as tecton__proto_dot_data_dot_feature__package__pb2
from tecton_proto.data import feature_view_pb2 as tecton__proto_dot_data_dot_feature__view__pb2
from tecton_proto.common import id_pb2 as tecton__proto_dot_common_dot_id__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tecton_proto/data/feature_service.proto',
  package='tecton_proto.data',
  syntax='proto2',
  serialized_options=b'\n\017com.tecton.dataP\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'tecton_proto/data/feature_service.proto\x12\x11tecton_proto.data\x1a%tecton_proto/common/column_type.proto\x1a\'tecton_proto/args/feature_service.proto\x1a$tecton_proto/data/fco_metadata.proto\x1a\'tecton_proto/data/feature_package.proto\x1a$tecton_proto/data/feature_view.proto\x1a\x1ctecton_proto/common/id.proto\"\x89\x03\n\x0e\x46\x65\x61tureService\x12\x45\n\x12\x66\x65\x61ture_service_id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x10\x66\x65\x61tureServiceId\x12M\n\x11\x66\x65\x61ture_set_items\x18\x02 \x03(\x0b\x32!.tecton_proto.data.FeatureSetItemR\x0f\x66\x65\x61tureSetItems\x12\x41\n\x0c\x66\x63o_metadata\x18\t \x01(\x0b\x32\x1e.tecton_proto.data.FcoMetadataR\x0b\x66\x63oMetadata\x12\x34\n\x16online_serving_enabled\x18\x0b \x01(\x08R\x14onlineServingEnabled\x12>\n\x07logging\x18\x0c \x01(\x0b\x32$.tecton_proto.args.LoggingConfigArgsR\x07loggingJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x05\x10\x06J\x04\x08\x06\x10\x07J\x04\x08\x07\x10\x08J\x04\x08\x08\x10\tJ\x04\x08\n\x10\x0b\"\xc6\x01\n\x10JoinKeyComponent\x12*\n\x11spine_column_name\x18\x01 \x01(\tR\x0fspineColumnName\x12H\n\x0c\x62inding_type\x18\x02 \x01(\x0e\x32%.tecton_proto.data.JoinKeyBindingTypeR\x0b\x62indingType\x12<\n\tdata_type\x18\x03 \x01(\x0e\x32\x1f.tecton_proto.common.ColumnTypeR\x08\x64\x61taType\"V\n\x0fJoinKeyTemplate\x12\x43\n\ncomponents\x18\x01 \x03(\x0b\x32#.tecton_proto.data.JoinKeyComponentR\ncomponents\"\x94\x03\n\x0e\x46\x65\x61tureSetItem\x12\x45\n\x12\x66\x65\x61ture_package_id\x18\x01 \x01(\x0b\x32\x17.tecton_proto.common.IdR\x10\x66\x65\x61turePackageId\x12?\n\x0f\x66\x65\x61ture_view_id\x18\x06 \x01(\x0b\x32\x17.tecton_proto.common.IdR\rfeatureViewId\x12\x62\n\x18join_configuration_items\x18\x03 \x03(\x0b\x32(.tecton_proto.data.JoinConfigurationItemR\x16joinConfigurationItems\x12\x1c\n\tnamespace\x18\x04 \x01(\tR\tnamespace\x12\'\n\x0f\x66\x65\x61ture_columns\x18\x05 \x03(\tR\x0e\x66\x65\x61tureColumns\x12O\n\x0b\x65nrichments\x18\xe8\x07 \x01(\x0b\x32,.tecton_proto.data.FeatureSetItemEnrichmentsR\x0b\x65nrichments\"s\n\x15JoinConfigurationItem\x12*\n\x11spine_column_name\x18\x01 \x01(\tR\x0fspineColumnName\x12.\n\x13package_column_name\x18\x02 \x01(\tR\x11packageColumnName\"\xc2\x01\n\x19\x46\x65\x61tureSetItemEnrichments\x12L\n\x0f\x66\x65\x61ture_package\x18\x01 \x01(\x0b\x32!.tecton_proto.data.FeaturePackageH\x00R\x0e\x66\x65\x61turePackage\x12\x43\n\x0c\x66\x65\x61ture_view\x18\x02 \x01(\x0b\x32\x1e.tecton_proto.data.FeatureViewH\x00R\x0b\x66\x65\x61tureViewB\x12\n\x10\x66\x65\x61ture_set_item*|\n\x12JoinKeyBindingType\x12!\n\x1dJOIN_KEY_BINDING_TYPE_UNKNOWN\x10\x00\x12\x1f\n\x1bJOIN_KEY_BINDING_TYPE_BOUND\x10\x01\x12\"\n\x1eJOIN_KEY_BINDING_TYPE_WILDCARD\x10\x02\x42\x13\n\x0f\x63om.tecton.dataP\x01'
  ,
  dependencies=[tecton__proto_dot_common_dot_column__type__pb2.DESCRIPTOR,tecton__proto_dot_args_dot_feature__service__pb2.DESCRIPTOR,tecton__proto_dot_data_dot_fco__metadata__pb2.DESCRIPTOR,tecton__proto_dot_data_dot_feature__package__pb2.DESCRIPTOR,tecton__proto_dot_data_dot_feature__view__pb2.DESCRIPTOR,tecton__proto_dot_common_dot_id__pb2.DESCRIPTOR,])

_JOINKEYBINDINGTYPE = _descriptor.EnumDescriptor(
  name='JoinKeyBindingType',
  full_name='tecton_proto.data.JoinKeyBindingType',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='JOIN_KEY_BINDING_TYPE_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='JOIN_KEY_BINDING_TYPE_BOUND', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='JOIN_KEY_BINDING_TYPE_WILDCARD', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1695,
  serialized_end=1819,
)
_sym_db.RegisterEnumDescriptor(_JOINKEYBINDINGTYPE)

JoinKeyBindingType = enum_type_wrapper.EnumTypeWrapper(_JOINKEYBINDINGTYPE)
JOIN_KEY_BINDING_TYPE_UNKNOWN = 0
JOIN_KEY_BINDING_TYPE_BOUND = 1
JOIN_KEY_BINDING_TYPE_WILDCARD = 2



_FEATURESERVICE = _descriptor.Descriptor(
  name='FeatureService',
  full_name='tecton_proto.data.FeatureService',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_service_id', full_name='tecton_proto.data.FeatureService.feature_service_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featureServiceId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature_set_items', full_name='tecton_proto.data.FeatureService.feature_set_items', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featureSetItems', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fco_metadata', full_name='tecton_proto.data.FeatureService.fco_metadata', index=2,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='fcoMetadata', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='online_serving_enabled', full_name='tecton_proto.data.FeatureService.online_serving_enabled', index=3,
      number=11, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='onlineServingEnabled', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='logging', full_name='tecton_proto.data.FeatureService.logging', index=4,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='logging', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=290,
  serialized_end=683,
)


_JOINKEYCOMPONENT = _descriptor.Descriptor(
  name='JoinKeyComponent',
  full_name='tecton_proto.data.JoinKeyComponent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='spine_column_name', full_name='tecton_proto.data.JoinKeyComponent.spine_column_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='spineColumnName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='binding_type', full_name='tecton_proto.data.JoinKeyComponent.binding_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='bindingType', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data_type', full_name='tecton_proto.data.JoinKeyComponent.data_type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='dataType', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=686,
  serialized_end=884,
)


_JOINKEYTEMPLATE = _descriptor.Descriptor(
  name='JoinKeyTemplate',
  full_name='tecton_proto.data.JoinKeyTemplate',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='components', full_name='tecton_proto.data.JoinKeyTemplate.components', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='components', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=886,
  serialized_end=972,
)


_FEATURESETITEM = _descriptor.Descriptor(
  name='FeatureSetItem',
  full_name='tecton_proto.data.FeatureSetItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_package_id', full_name='tecton_proto.data.FeatureSetItem.feature_package_id', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featurePackageId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature_view_id', full_name='tecton_proto.data.FeatureSetItem.feature_view_id', index=1,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featureViewId', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='join_configuration_items', full_name='tecton_proto.data.FeatureSetItem.join_configuration_items', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='joinConfigurationItems', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='namespace', full_name='tecton_proto.data.FeatureSetItem.namespace', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='namespace', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature_columns', full_name='tecton_proto.data.FeatureSetItem.feature_columns', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featureColumns', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='enrichments', full_name='tecton_proto.data.FeatureSetItem.enrichments', index=5,
      number=1000, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='enrichments', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=975,
  serialized_end=1379,
)


_JOINCONFIGURATIONITEM = _descriptor.Descriptor(
  name='JoinConfigurationItem',
  full_name='tecton_proto.data.JoinConfigurationItem',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='spine_column_name', full_name='tecton_proto.data.JoinConfigurationItem.spine_column_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='spineColumnName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='package_column_name', full_name='tecton_proto.data.JoinConfigurationItem.package_column_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='packageColumnName', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1381,
  serialized_end=1496,
)


_FEATURESETITEMENRICHMENTS = _descriptor.Descriptor(
  name='FeatureSetItemEnrichments',
  full_name='tecton_proto.data.FeatureSetItemEnrichments',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='feature_package', full_name='tecton_proto.data.FeatureSetItemEnrichments.feature_package', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featurePackage', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature_view', full_name='tecton_proto.data.FeatureSetItemEnrichments.feature_view', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, json_name='featureView', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='feature_set_item', full_name='tecton_proto.data.FeatureSetItemEnrichments.feature_set_item',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1499,
  serialized_end=1693,
)

_FEATURESERVICE.fields_by_name['feature_service_id'].message_type = tecton__proto_dot_common_dot_id__pb2._ID
_FEATURESERVICE.fields_by_name['feature_set_items'].message_type = _FEATURESETITEM
_FEATURESERVICE.fields_by_name['fco_metadata'].message_type = tecton__proto_dot_data_dot_fco__metadata__pb2._FCOMETADATA
_FEATURESERVICE.fields_by_name['logging'].message_type = tecton__proto_dot_args_dot_feature__service__pb2._LOGGINGCONFIGARGS
_JOINKEYCOMPONENT.fields_by_name['binding_type'].enum_type = _JOINKEYBINDINGTYPE
_JOINKEYCOMPONENT.fields_by_name['data_type'].enum_type = tecton__proto_dot_common_dot_column__type__pb2._COLUMNTYPE
_JOINKEYTEMPLATE.fields_by_name['components'].message_type = _JOINKEYCOMPONENT
_FEATURESETITEM.fields_by_name['feature_package_id'].message_type = tecton__proto_dot_common_dot_id__pb2._ID
_FEATURESETITEM.fields_by_name['feature_view_id'].message_type = tecton__proto_dot_common_dot_id__pb2._ID
_FEATURESETITEM.fields_by_name['join_configuration_items'].message_type = _JOINCONFIGURATIONITEM
_FEATURESETITEM.fields_by_name['enrichments'].message_type = _FEATURESETITEMENRICHMENTS
_FEATURESETITEMENRICHMENTS.fields_by_name['feature_package'].message_type = tecton__proto_dot_data_dot_feature__package__pb2._FEATUREPACKAGE
_FEATURESETITEMENRICHMENTS.fields_by_name['feature_view'].message_type = tecton__proto_dot_data_dot_feature__view__pb2._FEATUREVIEW
_FEATURESETITEMENRICHMENTS.oneofs_by_name['feature_set_item'].fields.append(
  _FEATURESETITEMENRICHMENTS.fields_by_name['feature_package'])
_FEATURESETITEMENRICHMENTS.fields_by_name['feature_package'].containing_oneof = _FEATURESETITEMENRICHMENTS.oneofs_by_name['feature_set_item']
_FEATURESETITEMENRICHMENTS.oneofs_by_name['feature_set_item'].fields.append(
  _FEATURESETITEMENRICHMENTS.fields_by_name['feature_view'])
_FEATURESETITEMENRICHMENTS.fields_by_name['feature_view'].containing_oneof = _FEATURESETITEMENRICHMENTS.oneofs_by_name['feature_set_item']
DESCRIPTOR.message_types_by_name['FeatureService'] = _FEATURESERVICE
DESCRIPTOR.message_types_by_name['JoinKeyComponent'] = _JOINKEYCOMPONENT
DESCRIPTOR.message_types_by_name['JoinKeyTemplate'] = _JOINKEYTEMPLATE
DESCRIPTOR.message_types_by_name['FeatureSetItem'] = _FEATURESETITEM
DESCRIPTOR.message_types_by_name['JoinConfigurationItem'] = _JOINCONFIGURATIONITEM
DESCRIPTOR.message_types_by_name['FeatureSetItemEnrichments'] = _FEATURESETITEMENRICHMENTS
DESCRIPTOR.enum_types_by_name['JoinKeyBindingType'] = _JOINKEYBINDINGTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeatureService = _reflection.GeneratedProtocolMessageType('FeatureService', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESERVICE,
  '__module__' : 'tecton_proto.data.feature_service_pb2'
  # @@protoc_insertion_point(class_scope:tecton_proto.data.FeatureService)
  })
_sym_db.RegisterMessage(FeatureService)

JoinKeyComponent = _reflection.GeneratedProtocolMessageType('JoinKeyComponent', (_message.Message,), {
  'DESCRIPTOR' : _JOINKEYCOMPONENT,
  '__module__' : 'tecton_proto.data.feature_service_pb2'
  # @@protoc_insertion_point(class_scope:tecton_proto.data.JoinKeyComponent)
  })
_sym_db.RegisterMessage(JoinKeyComponent)

JoinKeyTemplate = _reflection.GeneratedProtocolMessageType('JoinKeyTemplate', (_message.Message,), {
  'DESCRIPTOR' : _JOINKEYTEMPLATE,
  '__module__' : 'tecton_proto.data.feature_service_pb2'
  # @@protoc_insertion_point(class_scope:tecton_proto.data.JoinKeyTemplate)
  })
_sym_db.RegisterMessage(JoinKeyTemplate)

FeatureSetItem = _reflection.GeneratedProtocolMessageType('FeatureSetItem', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESETITEM,
  '__module__' : 'tecton_proto.data.feature_service_pb2'
  # @@protoc_insertion_point(class_scope:tecton_proto.data.FeatureSetItem)
  })
_sym_db.RegisterMessage(FeatureSetItem)

JoinConfigurationItem = _reflection.GeneratedProtocolMessageType('JoinConfigurationItem', (_message.Message,), {
  'DESCRIPTOR' : _JOINCONFIGURATIONITEM,
  '__module__' : 'tecton_proto.data.feature_service_pb2'
  # @@protoc_insertion_point(class_scope:tecton_proto.data.JoinConfigurationItem)
  })
_sym_db.RegisterMessage(JoinConfigurationItem)

FeatureSetItemEnrichments = _reflection.GeneratedProtocolMessageType('FeatureSetItemEnrichments', (_message.Message,), {
  'DESCRIPTOR' : _FEATURESETITEMENRICHMENTS,
  '__module__' : 'tecton_proto.data.feature_service_pb2'
  # @@protoc_insertion_point(class_scope:tecton_proto.data.FeatureSetItemEnrichments)
  })
_sym_db.RegisterMessage(FeatureSetItemEnrichments)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
