'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GLES1 import _types as _cs
# End users want this...
from OpenGL.raw.GLES1._types import *
from OpenGL.raw.GLES1 import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GLES1_OES_vertex_array_object'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GLES1,'GLES1_OES_vertex_array_object',error_checker=_errors._error_checker)
GL_VERTEX_ARRAY_BINDING_OES=_C('GL_VERTEX_ARRAY_BINDING_OES',0x85B5)
@_f
@_p.types(None,_cs.GLuint)
def glBindVertexArrayOES(array):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glDeleteVertexArraysOES(n,arrays):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glGenVertexArraysOES(n,arrays):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glIsVertexArrayOES(array):pass
