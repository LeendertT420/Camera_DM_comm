#!/usr/bin/python

import os, sys
import ctypes
import numpy

import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from ctypes import cdll
from os import getcwd, path, chdir
import platform
from _ctypes import FreeLibrary

def buffer_size() :
    return 256
def actuator_count() :
    return 91
def zernikes_count() :
    return 10

def load_dll() :
    current_dir = getcwd()
    if(platform.architecture()[0] == '32bit'):
        raise Exception('Platform Error','---You only have x64 MuDM Installation, Use python x64 Interpreter and x64 OS---')
    if(platform.architecture()[0] == '64bit'):
        dlls_dir = 'C:\\Program Files\\Mu-Imagine\\MuDM_Suite_1.1.3\\bin\\x64'

    dll_name = 0
    if(platform.architecture()[0] == '64bit'):
        dll_name = 'MuDMInterface.dll'

    try:
        dll_full_file_name = path.join(dlls_dir, dll_name)
        chdir(dlls_dir)
        dll = cdll.LoadLibrary(dll_full_file_name)
        chdir(current_dir)
        return dll
    except Exception as e:
        chdir(current_dir)
        raise Exception('MuDM_Error','---CAN NOT GET DLL---')

def free_dll(handle) :
    FreeLibrary(handle)

class MuDMInterface(object):
    """Class MuDMInterface"""

    def __init__(self,  **kwargs):
        """MuDMInterface constructor
        """
        self.MuDMInterface = ctypes.c_void_p()
        self.dll= load_dll()
        self.nb_actuators = actuator_count()
        message = ctypes.create_string_buffer(buffer_size())
        self.dll.MuDMInterface_New(message,ctypes.pointer(self.MuDMInterface))
        if message.value != '' and message.value != b'' :
            raise Exception('MuDM_Error',message.value)


    def __del_obj__(self):
        """MuDMInterface Destructor
        """
        message = ctypes.create_string_buffer(buffer_size())
        self.dll.MuDMInterface_Delete(message, self.MuDMInterface)
        if message.value != '' and message.value != b'' :
            raise Exception('MuDM_Error',message.value)

    def __del__(self):
        self.__del_obj__()
        free_dll(self.dll._handle)

    def connect(self,serial_number):
        """Establish connection to the mirror and sets it to its initial position

        :param serial_number: serial number of a connected mirror
        :type serial_number: string
        """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            self.dll.MuDMInterface_Connect(message,self.MuDMInterface,ctypes.c_char_p(serial_number.encode('utf-8')))
            if message.value != '' and message.value != b'' :
                raise Exception('MuDM_Error',message.value)
        except Exception as exception:
            raise Exception(__name__+' : connect',exception)

    def disconnect(self):
        """Close connection to the device """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            self.dll.MuDMInterface_Disconnect(message,self.MuDMInterface)
            if message.value != '' and message.value != b'' :
                raise Exception('MuDM_Error',message.value)
        except Exception as exception:
            raise Exception(__name__+' : disconnect',exception)

    def get_temperature(
        self
        ):
        """Get current MuDMInterface Temperature

        :return: Temperature (Celcius)
        :rtype: float
        """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            temp_out = ctypes.c_float()
            self.dll.MuDMInterface_GetTemperature(message,self.MuDMInterface,ctypes.byref(temp_out))
            if message.value != '' and message.value != b'' : raise Exception('MuDM_Error',message.value)
            return temp_out.value
        except Exception as exception:
            raise Exception(__name__+' : get_temperature',exception)

    def get_overheat_status(
        self
        ):
        """Get current MuDMInterface OverheatStatus : true if mirror stopped working

        :return: Status
        :rtype: bool
        """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            status = ctypes.c_int()
            self.dll.MuDMInterface_GetOverHeatStatus(message,self.MuDMInterface,ctypes.byref(status))
            if message.value != '' and message.value != b'' : raise Exception('MuDM_Error',message.value)
            return bool(status.value)
        except Exception as exception:
            raise Exception(__name__+' : get_overheat_status',exception)


    def get_current_positions(
        self
        ):
        """Get current actuators positions

        :return: Array containing the actuators positions
        :rtype: float list[]
        """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            value_out_positions = numpy.zeros(self.nb_actuators, dtype = numpy.single)
            self.dll.MuDMInterface_GetCurrentPositions.argtypes = [ctypes.c_char_p, ctypes.c_void_p, numpy.ctypeslib.ndpointer(numpy.single, flags="C_CONTIGUOUS")]
            self.dll.MuDMInterface_GetCurrentPositions( message,self.MuDMInterface,value_out_positions )
            if message.value != '' and message.value != b'' : raise Exception('MuDM_Error',message.value)
            return value_out_positions.tolist()
        except Exception as exception:
            raise Exception(__name__+' : get_current_positions',exception)

    def move_to_absolute_positions(
        self,
        positions_array
        ):
        """Move to requested absolute positions, clip according to aplitude limits

        :param positions_array: Requested absolutes positions
        :type positions_array: float list[] (size = number of actuators)
        """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            self.dll.MuDMInterface_MoveToAbsolutePositions.argtypes = [ctypes.c_char_p, ctypes.c_void_p,numpy.ctypeslib.ndpointer(numpy.float32, flags="C_CONTIGUOUS")]
            self.dll.MuDMInterface_MoveToAbsolutePositions(message, self.MuDMInterface, numpy.array(positions_array, dtype = numpy.float32) )
            if message.value != '' and message.value != b'' : raise Exception('MuDM_Error',message.value)
        except Exception as exception:
            raise Exception(__name__+' : move_to_absolute_positions',exception)


    def move_to_zernike_surface(
        self,
        positions_array,
        focus_correction
        ):
        """Move to requested absolute positions, clip according to aplitude limits

        :param positions_array: Requested absolutes positions
        :type positions_array: float list[] (size = Zernike Count)
        """
        try:
            message = ctypes.create_string_buffer(buffer_size())
            self.dll.MuDMInterface_MoveToZernikeSurface.argtypes = [ctypes.c_char_p,ctypes.c_void_p, numpy.ctypeslib.ndpointer(numpy.float32, flags="C_CONTIGUOUS"), ctypes.c_int]
            self.dll.MuDMInterface_MoveToZernikeSurface( message,self.MuDMInterface,numpy.array(positions_array, dtype = numpy.float32), ctypes.c_int(int(focus_correction)))
            if message.value != '' and message.value != b'' : raise Exception('MuDM_Error',message.value)
        except Exception as exception:
            raise Exception(__name__+' : move_to_zernike_surface',exception)
