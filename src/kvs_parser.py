from enum import Enum
from typing import List
from dataclasses import dataclass
from ebmlite import loadSchema, Document


class Mkv(Enum):
    """
    Symbolic names for select Matroska element specifications.
    https://www.matroska.org/technical/elements.html
    """
    SEGMENT = 0x18538067
    TAGS = 0x1254C367
    TAG = 0x7373
    SIMPLETAG = 0x67C8
    TAGNAME = 0x45A3
    TAGSTRING = 0x4487
    TAGBINARY = 0x4485
    CLUSTER = 0x1F43B675
    SIMPLEBLOCK = 0xA3


class Ebml(Enum):
    """
    Symbolic name for EBML Header declaration.
    https://datatracker.ietf.org/doc/html/rfc8794#section-8.1
    """
    EBML = 0x1A45DFA3


@dataclass()
class Fragment:

    bytes: bytearray
    dom: Document

    @property
    def simple_blocks(self):
        return self.__get_simple_blocks()

    def __get_simple_blocks(self):
        segment = next(s for s in self.dom if s.id == Mkv.SEGMENT.value)
        cluster = next(c for c in segment if c.id == Mkv.CLUSTER.value)
        return (b for b in cluster if b.id == Mkv.SIMPLEBLOCK.value)  # Generator


class KVSParser:

    def __init__(self, media):
        self.__stream = media['Payload']
        self.__schema = loadSchema('matroska.xml')
        self.__buffer = bytearray()

    @property
    def fragments(self) -> List[Fragment]:
        fragments = []
        for chunk in self.__stream:
            self.__buffer.extend(chunk)
            fragment = self.__parse()
            if fragment:
                fragments.append(fragment)
        return fragments

    def __parse(self) -> Fragment:
        header_elements = [e for e in self.__schema.loads(
            self.__buffer) if e.id == Ebml.EBML.value]
        if header_elements:
            offset = header_elements[0].offset
            fragment_bytes = self.__buffer[:offset]
            fragment_dom = self.__schema.loads(fragment_bytes)
            fragment = Fragment(bytes=fragment_bytes, dom=fragment_dom)
            self.__buffer = self.__buffer[offset:]
            return fragment
