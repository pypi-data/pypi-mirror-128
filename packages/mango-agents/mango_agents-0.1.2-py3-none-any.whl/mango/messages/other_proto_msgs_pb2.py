# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: other_proto_msgs.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='other_proto_msgs.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n\x16other_proto_msgs.proto\",\n\nGenericMsg\x12\x0c\n\x04text\x18\x01 \x01(\t\x12\x10\n\x08my_topic\x18\x02 \x01(\tb\x06proto3'
)




_GENERICMSG = _descriptor.Descriptor(
  name='GenericMsg',
  full_name='GenericMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='text', full_name='GenericMsg.text', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='my_topic', full_name='GenericMsg.my_topic', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=70,
)

DESCRIPTOR.message_types_by_name['GenericMsg'] = _GENERICMSG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

GenericMsg = _reflection.GeneratedProtocolMessageType('GenericMsg', (_message.Message,), {
  'DESCRIPTOR' : _GENERICMSG,
  '__module__' : 'other_proto_msgs_pb2'
  # @@protoc_insertion_point(class_scope:GenericMsg)
  })
_sym_db.RegisterMessage(GenericMsg)


# @@protoc_insertion_point(module_scope)
