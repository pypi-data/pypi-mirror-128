# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: http.proto

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
  name='http.proto',
  package='',
  syntax='proto2',
  serialized_pb=_b('\n\nhttp.proto\"\xf4\x01\n\x08HTTPFlow\x12\x1d\n\x07request\x18\x01 \x01(\x0b\x32\x0c.HTTPRequest\x12\x1f\n\x08response\x18\x02 \x01(\x0b\x32\r.HTTPResponse\x12\x19\n\x05\x65rror\x18\x03 \x01(\x0b\x32\n.HTTPError\x12&\n\x0b\x63lient_conn\x18\x04 \x01(\x0b\x32\x11.ClientConnection\x12&\n\x0bserver_conn\x18\x05 \x01(\x0b\x32\x11.ServerConnection\x12\x13\n\x0bintercepted\x18\x06 \x01(\x08\x12\x0e\n\x06marked\x18\x07 \x01(\x08\x12\x0c\n\x04mode\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\t\"\xfa\x01\n\x0bHTTPRequest\x12\x19\n\x11\x66irst_line_format\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12\x0e\n\x06scheme\x18\x03 \x01(\t\x12\x0c\n\x04host\x18\x04 \x01(\t\x12\x0c\n\x04port\x18\x05 \x01(\x05\x12\x0c\n\x04path\x18\x06 \x01(\t\x12\x14\n\x0chttp_version\x18\x07 \x01(\t\x12\x1c\n\x07headers\x18\x08 \x03(\x0b\x32\x0b.HTTPHeader\x12\x0f\n\x07\x63ontent\x18\t \x01(\x0c\x12\x17\n\x0ftimestamp_start\x18\n \x01(\x01\x12\x15\n\rtimestamp_end\x18\x0b \x01(\x01\x12\x11\n\tis_replay\x18\x0c \x01(\x08\"\xbb\x01\n\x0cHTTPResponse\x12\x14\n\x0chttp_version\x18\x01 \x01(\t\x12\x13\n\x0bstatus_code\x18\x02 \x01(\x05\x12\x0e\n\x06reason\x18\x03 \x01(\t\x12\x1c\n\x07headers\x18\x04 \x03(\x0b\x32\x0b.HTTPHeader\x12\x0f\n\x07\x63ontent\x18\x05 \x01(\x0c\x12\x17\n\x0ftimestamp_start\x18\x06 \x01(\x01\x12\x15\n\rtimestamp_end\x18\x07 \x01(\x01\x12\x11\n\tis_replay\x18\x08 \x01(\x08\"+\n\tHTTPError\x12\x0b\n\x03msg\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x01\")\n\nHTTPHeader\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"%\n\x07\x41\x64\x64ress\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\"\xc2\x02\n\x10\x43lientConnection\x12\n\n\x02id\x18\x01 \x01(\t\x12\x19\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x08.Address\x12\x17\n\x0ftls_established\x18\x03 \x01(\x08\x12\x12\n\nclientcert\x18\x04 \x01(\t\x12\x10\n\x08mitmcert\x18\x05 \x01(\t\x12\x17\n\x0ftimestamp_start\x18\x06 \x01(\x01\x12\x1b\n\x13timestamp_tls_setup\x18\x07 \x01(\x01\x12\x15\n\rtimestamp_end\x18\x08 \x01(\x01\x12\x0b\n\x03sni\x18\t \x01(\t\x12\x13\n\x0b\x63ipher_name\x18\n \x01(\t\x12\x1d\n\x15\x61lpn_proto_negotiated\x18\x0b \x01(\x0c\x12\x13\n\x0btls_version\x18\x0c \x01(\t\x12%\n\x0etls_extensions\x18\r \x03(\x0b\x32\r.TLSExtension\"\xeb\x02\n\x10ServerConnection\x12\n\n\x02id\x18\x01 \x01(\t\x12\x19\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x08.Address\x12\x1c\n\nip_address\x18\x03 \x01(\x0b\x32\x08.Address\x12 \n\x0esource_address\x18\x04 \x01(\x0b\x32\x08.Address\x12\x17\n\x0ftls_established\x18\x05 \x01(\x08\x12\x0c\n\x04\x63\x65rt\x18\x06 \x01(\t\x12\x0b\n\x03sni\x18\x07 \x01(\t\x12\x1d\n\x15\x61lpn_proto_negotiated\x18\x08 \x01(\x0c\x12\x13\n\x0btls_version\x18\t \x01(\t\x12\x17\n\x0ftimestamp_start\x18\n \x01(\x01\x12\x1b\n\x13timestamp_tcp_setup\x18\x0b \x01(\x01\x12\x1b\n\x13timestamp_tls_setup\x18\x0c \x01(\x01\x12\x15\n\rtimestamp_end\x18\r \x01(\x01\x12\x1e\n\x03via\x18\x0e \x01(\x0b\x32\x11.ServerConnection\"*\n\x0cTLSExtension\x12\x0b\n\x03int\x18\x01 \x01(\x03\x12\r\n\x05\x62ytes\x18\x02 \x01(\x0c')
)




_HTTPFLOW = _descriptor.Descriptor(
  name='HTTPFlow',
  full_name='HTTPFlow',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request', full_name='HTTPFlow.request', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='response', full_name='HTTPFlow.response', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='HTTPFlow.error', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='client_conn', full_name='HTTPFlow.client_conn', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='server_conn', full_name='HTTPFlow.server_conn', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='intercepted', full_name='HTTPFlow.intercepted', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='marked', full_name='HTTPFlow.marked', index=6,
      number=7, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mode', full_name='HTTPFlow.mode', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='HTTPFlow.id', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=15,
  serialized_end=259,
)


_HTTPREQUEST = _descriptor.Descriptor(
  name='HTTPRequest',
  full_name='HTTPRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='first_line_format', full_name='HTTPRequest.first_line_format', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='method', full_name='HTTPRequest.method', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='scheme', full_name='HTTPRequest.scheme', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='host', full_name='HTTPRequest.host', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='HTTPRequest.port', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='path', full_name='HTTPRequest.path', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='http_version', full_name='HTTPRequest.http_version', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='headers', full_name='HTTPRequest.headers', index=7,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='HTTPRequest.content', index=8,
      number=9, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_start', full_name='HTTPRequest.timestamp_start', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_end', full_name='HTTPRequest.timestamp_end', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_replay', full_name='HTTPRequest.is_replay', index=11,
      number=12, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=262,
  serialized_end=512,
)


_HTTPRESPONSE = _descriptor.Descriptor(
  name='HTTPResponse',
  full_name='HTTPResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='http_version', full_name='HTTPResponse.http_version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status_code', full_name='HTTPResponse.status_code', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='reason', full_name='HTTPResponse.reason', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='headers', full_name='HTTPResponse.headers', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='content', full_name='HTTPResponse.content', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_start', full_name='HTTPResponse.timestamp_start', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_end', full_name='HTTPResponse.timestamp_end', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='is_replay', full_name='HTTPResponse.is_replay', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=515,
  serialized_end=702,
)


_HTTPERROR = _descriptor.Descriptor(
  name='HTTPError',
  full_name='HTTPError',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='HTTPError.msg', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='HTTPError.timestamp', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=704,
  serialized_end=747,
)


_HTTPHEADER = _descriptor.Descriptor(
  name='HTTPHeader',
  full_name='HTTPHeader',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='HTTPHeader.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='HTTPHeader.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=749,
  serialized_end=790,
)


_ADDRESS = _descriptor.Descriptor(
  name='Address',
  full_name='Address',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host', full_name='Address.host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='port', full_name='Address.port', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=792,
  serialized_end=829,
)


_CLIENTCONNECTION = _descriptor.Descriptor(
  name='ClientConnection',
  full_name='ClientConnection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ClientConnection.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='ClientConnection.address', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tls_established', full_name='ClientConnection.tls_established', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='clientcert', full_name='ClientConnection.clientcert', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='mitmcert', full_name='ClientConnection.mitmcert', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_start', full_name='ClientConnection.timestamp_start', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_tls_setup', full_name='ClientConnection.timestamp_tls_setup', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_end', full_name='ClientConnection.timestamp_end', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sni', full_name='ClientConnection.sni', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cipher_name', full_name='ClientConnection.cipher_name', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alpn_proto_negotiated', full_name='ClientConnection.alpn_proto_negotiated', index=10,
      number=11, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tls_version', full_name='ClientConnection.tls_version', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tls_extensions', full_name='ClientConnection.tls_extensions', index=12,
      number=13, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=832,
  serialized_end=1154,
)


_SERVERCONNECTION = _descriptor.Descriptor(
  name='ServerConnection',
  full_name='ServerConnection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='ServerConnection.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='ServerConnection.address', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ip_address', full_name='ServerConnection.ip_address', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='source_address', full_name='ServerConnection.source_address', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tls_established', full_name='ServerConnection.tls_established', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cert', full_name='ServerConnection.cert', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sni', full_name='ServerConnection.sni', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='alpn_proto_negotiated', full_name='ServerConnection.alpn_proto_negotiated', index=7,
      number=8, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tls_version', full_name='ServerConnection.tls_version', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_start', full_name='ServerConnection.timestamp_start', index=9,
      number=10, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_tcp_setup', full_name='ServerConnection.timestamp_tcp_setup', index=10,
      number=11, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_tls_setup', full_name='ServerConnection.timestamp_tls_setup', index=11,
      number=12, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='timestamp_end', full_name='ServerConnection.timestamp_end', index=12,
      number=13, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='via', full_name='ServerConnection.via', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1157,
  serialized_end=1520,
)


_TLSEXTENSION = _descriptor.Descriptor(
  name='TLSExtension',
  full_name='TLSExtension',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='int', full_name='TLSExtension.int', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bytes', full_name='TLSExtension.bytes', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=_b(""),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1522,
  serialized_end=1564,
)

_HTTPFLOW.fields_by_name['request'].message_type = _HTTPREQUEST
_HTTPFLOW.fields_by_name['response'].message_type = _HTTPRESPONSE
_HTTPFLOW.fields_by_name['error'].message_type = _HTTPERROR
_HTTPFLOW.fields_by_name['client_conn'].message_type = _CLIENTCONNECTION
_HTTPFLOW.fields_by_name['server_conn'].message_type = _SERVERCONNECTION
_HTTPREQUEST.fields_by_name['headers'].message_type = _HTTPHEADER
_HTTPRESPONSE.fields_by_name['headers'].message_type = _HTTPHEADER
_CLIENTCONNECTION.fields_by_name['address'].message_type = _ADDRESS
_CLIENTCONNECTION.fields_by_name['tls_extensions'].message_type = _TLSEXTENSION
_SERVERCONNECTION.fields_by_name['address'].message_type = _ADDRESS
_SERVERCONNECTION.fields_by_name['ip_address'].message_type = _ADDRESS
_SERVERCONNECTION.fields_by_name['source_address'].message_type = _ADDRESS
_SERVERCONNECTION.fields_by_name['via'].message_type = _SERVERCONNECTION
DESCRIPTOR.message_types_by_name['HTTPFlow'] = _HTTPFLOW
DESCRIPTOR.message_types_by_name['HTTPRequest'] = _HTTPREQUEST
DESCRIPTOR.message_types_by_name['HTTPResponse'] = _HTTPRESPONSE
DESCRIPTOR.message_types_by_name['HTTPError'] = _HTTPERROR
DESCRIPTOR.message_types_by_name['HTTPHeader'] = _HTTPHEADER
DESCRIPTOR.message_types_by_name['Address'] = _ADDRESS
DESCRIPTOR.message_types_by_name['ClientConnection'] = _CLIENTCONNECTION
DESCRIPTOR.message_types_by_name['ServerConnection'] = _SERVERCONNECTION
DESCRIPTOR.message_types_by_name['TLSExtension'] = _TLSEXTENSION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HTTPFlow = _reflection.GeneratedProtocolMessageType('HTTPFlow', (_message.Message,), dict(
  DESCRIPTOR = _HTTPFLOW,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:HTTPFlow)
  ))
_sym_db.RegisterMessage(HTTPFlow)

HTTPRequest = _reflection.GeneratedProtocolMessageType('HTTPRequest', (_message.Message,), dict(
  DESCRIPTOR = _HTTPREQUEST,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:HTTPRequest)
  ))
_sym_db.RegisterMessage(HTTPRequest)

HTTPResponse = _reflection.GeneratedProtocolMessageType('HTTPResponse', (_message.Message,), dict(
  DESCRIPTOR = _HTTPRESPONSE,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:HTTPResponse)
  ))
_sym_db.RegisterMessage(HTTPResponse)

HTTPError = _reflection.GeneratedProtocolMessageType('HTTPError', (_message.Message,), dict(
  DESCRIPTOR = _HTTPERROR,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:HTTPError)
  ))
_sym_db.RegisterMessage(HTTPError)

HTTPHeader = _reflection.GeneratedProtocolMessageType('HTTPHeader', (_message.Message,), dict(
  DESCRIPTOR = _HTTPHEADER,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:HTTPHeader)
  ))
_sym_db.RegisterMessage(HTTPHeader)

Address = _reflection.GeneratedProtocolMessageType('Address', (_message.Message,), dict(
  DESCRIPTOR = _ADDRESS,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:Address)
  ))
_sym_db.RegisterMessage(Address)

ClientConnection = _reflection.GeneratedProtocolMessageType('ClientConnection', (_message.Message,), dict(
  DESCRIPTOR = _CLIENTCONNECTION,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:ClientConnection)
  ))
_sym_db.RegisterMessage(ClientConnection)

ServerConnection = _reflection.GeneratedProtocolMessageType('ServerConnection', (_message.Message,), dict(
  DESCRIPTOR = _SERVERCONNECTION,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:ServerConnection)
  ))
_sym_db.RegisterMessage(ServerConnection)

TLSExtension = _reflection.GeneratedProtocolMessageType('TLSExtension', (_message.Message,), dict(
  DESCRIPTOR = _TLSEXTENSION,
  __module__ = 'http_pb2'
  # @@protoc_insertion_point(class_scope:TLSExtension)
  ))
_sym_db.RegisterMessage(TLSExtension)


# @@protoc_insertion_point(module_scope)
