# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tecton_proto/data/feature_store.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tecton_proto/data/feature_store.proto',
  package='tecton_proto.data',
  syntax='proto2',
  serialized_options=b'\n\017com.tecton.dataP\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%tecton_proto/data/feature_store.proto\x12\x11tecton_proto.data*\xa2\x01\n\x19\x46\x65\x61tureStoreFormatVersion\x12(\n$FEATURE_STORE_FORMAT_VERSION_DEFAULT\x10\x00\x12\x31\n-FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS\x10\x01\x12$\n FEATURE_STORE_FORMAT_VERSION_MAX\x10\x01\x1a\x02\x10\x01\x42\x13\n\x0f\x63om.tecton.dataP\x01'
)

_FEATURESTOREFORMATVERSION = _descriptor.EnumDescriptor(
  name='FeatureStoreFormatVersion',
  full_name='tecton_proto.data.FeatureStoreFormatVersion',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='FEATURE_STORE_FORMAT_VERSION_DEFAULT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='FEATURE_STORE_FORMAT_VERSION_MAX', index=2, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=b'\020\001',
  serialized_start=61,
  serialized_end=223,
)
_sym_db.RegisterEnumDescriptor(_FEATURESTOREFORMATVERSION)

FeatureStoreFormatVersion = enum_type_wrapper.EnumTypeWrapper(_FEATURESTOREFORMATVERSION)
FEATURE_STORE_FORMAT_VERSION_DEFAULT = 0
FEATURE_STORE_FORMAT_VERSION_TIME_NANOSECONDS = 1
FEATURE_STORE_FORMAT_VERSION_MAX = 1


DESCRIPTOR.enum_types_by_name['FeatureStoreFormatVersion'] = _FEATURESTOREFORMATVERSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None
_FEATURESTOREFORMATVERSION._options = None
# @@protoc_insertion_point(module_scope)
