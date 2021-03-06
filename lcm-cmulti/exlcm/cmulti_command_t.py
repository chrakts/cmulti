"""LCM type definitions
This file automatically generated by lcm.
DO NOT MODIFY BY HAND!!!!
"""

try:
    import cStringIO.StringIO as BytesIO
except ImportError:
    from io import BytesIO
import struct

class cmulti_command_t(object):
    __slots__ = ["target", "source", "command", "parameter", "informationType", "expect_answer", "timeout_ms", "crcType"]

    def __init__(self):
        self.target = ""
        self.source = ""
        self.command = ""
        self.parameter = ""
        self.informationType = 0
        self.expect_answer = False
        self.timeout_ms = 0
        self.crcType = 0

    def encode(self):
        buf = BytesIO()
        buf.write(cmulti_command_t._get_packed_fingerprint())
        self._encode_one(buf)
        return buf.getvalue()

    def _encode_one(self, buf):
        __target_encoded = self.target.encode('utf-8')
        buf.write(struct.pack('>I', len(__target_encoded)+1))
        buf.write(__target_encoded)
        buf.write(b"\0")
        __source_encoded = self.source.encode('utf-8')
        buf.write(struct.pack('>I', len(__source_encoded)+1))
        buf.write(__source_encoded)
        buf.write(b"\0")
        __command_encoded = self.command.encode('utf-8')
        buf.write(struct.pack('>I', len(__command_encoded)+1))
        buf.write(__command_encoded)
        buf.write(b"\0")
        __parameter_encoded = self.parameter.encode('utf-8')
        buf.write(struct.pack('>I', len(__parameter_encoded)+1))
        buf.write(__parameter_encoded)
        buf.write(b"\0")
        buf.write(struct.pack(">bbhb", self.informationType, self.expect_answer, self.timeout_ms, self.crcType))

    def decode(data):
        if hasattr(data, 'read'):
            buf = data
        else:
            buf = BytesIO(data)
        if buf.read(8) != cmulti_command_t._get_packed_fingerprint():
            raise ValueError("Decode error")
        return cmulti_command_t._decode_one(buf)
    decode = staticmethod(decode)

    def _decode_one(buf):
        self = cmulti_command_t()
        __target_len = struct.unpack('>I', buf.read(4))[0]
        self.target = buf.read(__target_len)[:-1].decode('utf-8', 'replace')
        __source_len = struct.unpack('>I', buf.read(4))[0]
        self.source = buf.read(__source_len)[:-1].decode('utf-8', 'replace')
        __command_len = struct.unpack('>I', buf.read(4))[0]
        self.command = buf.read(__command_len)[:-1].decode('utf-8', 'replace')
        __parameter_len = struct.unpack('>I', buf.read(4))[0]
        self.parameter = buf.read(__parameter_len)[:-1].decode('utf-8', 'replace')
        self.informationType = struct.unpack(">b", buf.read(1))[0]
        self.expect_answer = bool(struct.unpack('b', buf.read(1))[0])
        self.timeout_ms, self.crcType = struct.unpack(">hb", buf.read(3))
        return self
    _decode_one = staticmethod(_decode_one)

    _hash = None
    def _get_hash_recursive(parents):
        if cmulti_command_t in parents: return 0
        tmphash = (0x834731eed3900ad6) & 0xffffffffffffffff
        tmphash  = (((tmphash<<1)&0xffffffffffffffff)  + (tmphash>>63)) & 0xffffffffffffffff
        return tmphash
    _get_hash_recursive = staticmethod(_get_hash_recursive)
    _packed_fingerprint = None

    def _get_packed_fingerprint():
        if cmulti_command_t._packed_fingerprint is None:
            cmulti_command_t._packed_fingerprint = struct.pack(">Q", cmulti_command_t._get_hash_recursive([]))
        return cmulti_command_t._packed_fingerprint
    _get_packed_fingerprint = staticmethod(_get_packed_fingerprint)

