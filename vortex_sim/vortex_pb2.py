# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: vortex.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='vortex.proto',
  package='',
  serialized_pb=_b('\n\x0cvortex.proto\"Y\n\x0bsensor_data\x12\x19\n\rir_data_array\x18\x01 \x03(\rB\x02\x10\x01\x12\x1c\n\x10sonar_data_array\x18\x02 \x03(\rB\x02\x10\x01\x12\x11\n\ttimestamp\x18\x03 \x01(\r\"\x7f\n\x0c\x63ommand_data\x12\x30\n\x07\x63ommand\x18\x01 \x01(\x0e\x32\x19.command_data.CommandType:\x04STOP\x12\x10\n\x04\x61rgs\x18\x02 \x03(\x05\x42\x02\x10\x01\"+\n\x0b\x43ommandType\x12\x08\n\x04MOVE\x10\x00\x12\x08\n\x04TURN\x10\x01\x12\x08\n\x04STOP\x10\x02')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_COMMAND_DATA_COMMANDTYPE = _descriptor.EnumDescriptor(
  name='CommandType',
  full_name='command_data.CommandType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='MOVE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='TURN', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOP', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=191,
  serialized_end=234,
)
_sym_db.RegisterEnumDescriptor(_COMMAND_DATA_COMMANDTYPE)


_SENSOR_DATA = _descriptor.Descriptor(
  name='sensor_data',
  full_name='sensor_data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ir_data_array', full_name='sensor_data.ir_data_array', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='sonar_data_array', full_name='sensor_data.sonar_data_array', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='sensor_data.timestamp', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=16,
  serialized_end=105,
)


_COMMAND_DATA = _descriptor.Descriptor(
  name='command_data',
  full_name='command_data',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='command_data.command', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=2,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='args', full_name='command_data.args', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=_descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMMAND_DATA_COMMANDTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=234,
)

_COMMAND_DATA.fields_by_name['command'].enum_type = _COMMAND_DATA_COMMANDTYPE
_COMMAND_DATA_COMMANDTYPE.containing_type = _COMMAND_DATA
DESCRIPTOR.message_types_by_name['sensor_data'] = _SENSOR_DATA
DESCRIPTOR.message_types_by_name['command_data'] = _COMMAND_DATA

sensor_data = _reflection.GeneratedProtocolMessageType('sensor_data', (_message.Message,), dict(
  DESCRIPTOR = _SENSOR_DATA,
  __module__ = 'vortex_pb2'
  # @@protoc_insertion_point(class_scope:sensor_data)
  ))
_sym_db.RegisterMessage(sensor_data)

command_data = _reflection.GeneratedProtocolMessageType('command_data', (_message.Message,), dict(
  DESCRIPTOR = _COMMAND_DATA,
  __module__ = 'vortex_pb2'
  # @@protoc_insertion_point(class_scope:command_data)
  ))
_sym_db.RegisterMessage(command_data)


_SENSOR_DATA.fields_by_name['ir_data_array'].has_options = True
_SENSOR_DATA.fields_by_name['ir_data_array']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_SENSOR_DATA.fields_by_name['sonar_data_array'].has_options = True
_SENSOR_DATA.fields_by_name['sonar_data_array']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
_COMMAND_DATA.fields_by_name['args'].has_options = True
_COMMAND_DATA.fields_by_name['args']._options = _descriptor._ParseOptions(descriptor_pb2.FieldOptions(), _b('\020\001'))
# @@protoc_insertion_point(module_scope)