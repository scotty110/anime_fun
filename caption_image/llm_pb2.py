# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: llm.proto
# Protobuf Python Version: 5.28.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    28,
    2,
    '',
    'llm.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tllm.proto\x12\x0ctwirp.server\"\x15\n\x05\x41Text\x12\x0c\n\x04Text\x18\x01 \x01(\t\"\x17\n\x06\x41Image\x12\r\n\x05Image\x18\x01 \x01(\x0c\"+\n\x0cImageCaption\x12\x0c\n\x04Text\x18\x01 \x01(\t\x12\r\n\x05Image\x18\x02 \x01(\x0c\x32O\n\x10\x46rierenAIService\x12;\n\x0eGenPlayingCard\x12\x13.twirp.server.AText\x1a\x14.twirp.server.AImage2C\n\rGenBioService\x12\x32\n\x06GenBio\x12\x13.twirp.server.AText\x1a\x13.twirp.server.AText2P\n\x13GenCharacterService\x12\x39\n\x0cGenCharacter\x12\x13.twirp.server.AText\x1a\x14.twirp.server.AImage2W\n\x13ImageCaptionService\x12@\n\x0c\x43\x61ptionImage\x12\x1a.twirp.server.ImageCaption\x1a\x14.twirp.server.AImageB\x0eZ\x0c./;frierenaib\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'llm_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z\014./;frierenai'
  _globals['_ATEXT']._serialized_start=27
  _globals['_ATEXT']._serialized_end=48
  _globals['_AIMAGE']._serialized_start=50
  _globals['_AIMAGE']._serialized_end=73
  _globals['_IMAGECAPTION']._serialized_start=75
  _globals['_IMAGECAPTION']._serialized_end=118
  _globals['_FRIERENAISERVICE']._serialized_start=120
  _globals['_FRIERENAISERVICE']._serialized_end=199
  _globals['_GENBIOSERVICE']._serialized_start=201
  _globals['_GENBIOSERVICE']._serialized_end=268
  _globals['_GENCHARACTERSERVICE']._serialized_start=270
  _globals['_GENCHARACTERSERVICE']._serialized_end=350
  _globals['_IMAGECAPTIONSERVICE']._serialized_start=352
  _globals['_IMAGECAPTIONSERVICE']._serialized_end=439
# @@protoc_insertion_point(module_scope)