# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: frame.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x66rame.proto\"H\n\x08SpeFrame\x12\x0f\n\x07stokesi\x18\x01 \x03(\x02\x12\x0f\n\x07stokesv\x18\x02 \x03(\x02\x12\x0c\n\x04time\x18\x03 \x03(\x01\x12\x0c\n\x04\x66req\x18\x04 \x03(\x01\"d\n\x08ImgFrame\x12\x0f\n\x07stokesi\x18\x01 \x03(\x02\x12\x0f\n\x07stokesv\x18\x02 \x03(\x02\x12\x0c\n\x04sunx\x18\x03 \x03(\x02\x12\x0c\n\x04suny\x18\x04 \x03(\x02\x12\x0c\n\x04time\x18\x05 \x01(\x05\x12\x0c\n\x04\x66req\x18\x06 \x01(\x02\"\xf7\x01\n\x0eOpenImgFileAck\x12\x18\n\x05\x66rame\x18\x01 \x01(\x0b\x32\t.ImgFrame\x12-\n\x07header0\x18\x02 \x03(\x0b\x32\x1c.OpenImgFileAck.Header0Entry\x12-\n\x07header1\x18\x03 \x03(\x0b\x32\x1c.OpenImgFileAck.Header1Entry\x12\r\n\x05index\x18\x04 \x01(\x05\x1a.\n\x0cHeader0Entry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a.\n\x0cHeader1Entry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"4\n\tImgAppAck\x12\x18\n\x05\x66rame\x18\x01 \x01(\x0b\x32\t.ImgFrame\x12\r\n\x05index\x18\x02 \x01(\x05\"\xc2\x01\n\nFlowCalAck\x12)\n\x07stokesi\x18\x01 \x03(\x0b\x32\x18.FlowCalAck.StokesiEntry\x12)\n\x07stokesv\x18\x02 \x03(\x0b\x32\x18.FlowCalAck.StokesvEntry\x1a.\n\x0cStokesiEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x1a.\n\x0cStokesvEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x01:\x02\x38\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'frame_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OPENIMGFILEACK_HEADER0ENTRY._options = None
  _OPENIMGFILEACK_HEADER0ENTRY._serialized_options = b'8\001'
  _OPENIMGFILEACK_HEADER1ENTRY._options = None
  _OPENIMGFILEACK_HEADER1ENTRY._serialized_options = b'8\001'
  _FLOWCALACK_STOKESIENTRY._options = None
  _FLOWCALACK_STOKESIENTRY._serialized_options = b'8\001'
  _FLOWCALACK_STOKESVENTRY._options = None
  _FLOWCALACK_STOKESVENTRY._serialized_options = b'8\001'
  _globals['_SPEFRAME']._serialized_start=15
  _globals['_SPEFRAME']._serialized_end=87
  _globals['_IMGFRAME']._serialized_start=89
  _globals['_IMGFRAME']._serialized_end=189
  _globals['_OPENIMGFILEACK']._serialized_start=192
  _globals['_OPENIMGFILEACK']._serialized_end=439
  _globals['_OPENIMGFILEACK_HEADER0ENTRY']._serialized_start=345
  _globals['_OPENIMGFILEACK_HEADER0ENTRY']._serialized_end=391
  _globals['_OPENIMGFILEACK_HEADER1ENTRY']._serialized_start=393
  _globals['_OPENIMGFILEACK_HEADER1ENTRY']._serialized_end=439
  _globals['_IMGAPPACK']._serialized_start=441
  _globals['_IMGAPPACK']._serialized_end=493
  _globals['_FLOWCALACK']._serialized_start=496
  _globals['_FLOWCALACK']._serialized_end=690
  _globals['_FLOWCALACK_STOKESIENTRY']._serialized_start=596
  _globals['_FLOWCALACK_STOKESIENTRY']._serialized_end=642
  _globals['_FLOWCALACK_STOKESVENTRY']._serialized_start=644
  _globals['_FLOWCALACK_STOKESVENTRY']._serialized_end=690
# @@protoc_insertion_point(module_scope)
