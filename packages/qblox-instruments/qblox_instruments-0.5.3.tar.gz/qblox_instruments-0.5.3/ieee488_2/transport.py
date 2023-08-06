#------------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, pulsar_dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import socket
import re
import os
import sys
import struct
import subprocess

#-- class ----------------------------------------------------------------------

class transport:
    """
    Abstract base class for data transport to instruments.
    """

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Abstract method to close instrument.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Abstract method to write command to instrument.

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Abstract method to write binary data to instrument.

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Abstract method to read binary data from instrument.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        pass

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Abstract method to read data from instrument.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        pass

#-- class ---------------------------------------------------------------------

class ip_transport(transport):
    """
    Class for data transport of IP socket.
    """

    #--------------------------------------------------------------------------
    def __init__(self, host: str, port: int = 5025, timeout : float = 60.0, snd_buf_size: int = 512 * 1024) -> None:
        """
        Create IP socket transport class.

        Parameters
        ----------
        host : str
            Instrument IP address.
        port : int
            Instrument port.
        timeout : float
            Instrument call timeout in seconds.
        snd_buf_size : int
            Instrument buffer size for transmissions to instrument.

        Returns
        ----------

        Raises
        ----------
        """

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(3)                                                 #Setup timeout (before connecting)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, snd_buf_size) #Enlarge buffer
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)         #Send immediately
        self._socket.connect((host, port))
        self._socket.settimeout(timeout)                                           #Timeout after connecting

    #--------------------------------------------------------------------------
    def __del__(self) -> None:
        """
        Delete IP socket transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self.close()

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close IP socket.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self._socket.close()

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to instrument over IP socket.

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        out_str = cmd_str + '\n'
        self.write_binary(out_str.encode('ascii'))

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to instrument over IP socket.

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        exp_len = len(data)
        act_len = 0
        while True:
            act_len += self._socket.send(data[act_len:exp_len])
            if act_len == exp_len:
                break

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from instrument over IP socket.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        data = self._socket.recv(size)
        act_len = len(data)
        exp_len = size
        while act_len != exp_len:
            data += self._socket.recv(exp_len - act_len)
            act_len = len(data)
        return data

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from instrument over IP socket.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        return self._socket.makefile().readline()

#-- class ---------------------------------------------------------------------

class file_transport(transport):
    """
    Class implementing file I/O to support driver testing.
    """

    #--------------------------------------------------------------------------
    def __init__(self, out_file_name: str, in_file_name: str = '') -> None:
        """
        Create file transport class.

        Parameters
        ----------
        out_file_name : str
            Output file name/path to write all commands to.
        in_file_name : str
            Input file name/path to read all command responses from.

        Returns
        ----------

        Raises
        ----------
        """

        self._out_file = open(out_file_name, 'wb+')
        self._in_file  = open(in_file_name, 'r')

    #--------------------------------------------------------------------------
    def __del__(self) -> None:
        """
        Delete file transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self.close()

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close file descriptors.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self._out_file.close()
        self._in_file.close()

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to file.

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        out_str = cmd_str + '\n'
        self.write_binary(out_str.encode('ascii'))

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to file.

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        self._out_file.write(data)

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from file.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        return self._in_file.read(size)

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from file.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        return self._in_file.readline()

#-- class ---------------------------------------------------------------------

class base_dummy_transport(transport):
    """
    Class to replace device with dummy device to support software stack testing without hardware.
    The class implements all mandatory and required SCPI calls. Call reponses are
    largely artifically constructed to be inline with the call's functionality (e.g. `*IDN?` returns valid,
    but artificial IDN data.)
    """

    #--------------------------------------------------------------------------
    def __init__(self) -> None:
        """
        Create base dummy transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self._cmd_hist               = []
        self._data_out               = 0
        self._bin_out                = None
        self._system_error           = []
        self._cmds                   = {"*CMDS?":              self._get_cmds,
                                        "*IDN?":               self._get_idn,
                                        "*RST":                self._reset,
                                        "SYSTem:ERRor:NEXT?":  self._get_system_error,
                                        "SYSTem:ERRor:COUNt?": self._get_system_error_cnt
                                       }

    #--------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close and resets base dummy transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        self._cmd_hist     = []
        self._data_out     = 0
        self._bin_out      = None
        self._system_error = []

    #--------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to dummy. Stores command in command history (see :func:`ieee488_2.transport.base_dummy_transport.get_cmd_hist`).

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------

        Raises
        ----------
        """

        self._handle_cmd(cmd_str)

    #--------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to dummy. Stores command in command history (see :func:`ieee488_2.transport.base_dummy_transport.get_cmd_hist`).

        Parameters
        ----------
        data : bytes
            Binary data

        Returns
        ----------

        Raises
        ----------
        """

        cmd_parts = data.split('#'.encode())
        cmd_str   = cmd_parts[0].decode()
        bin_in    = '#'.encode() + '#'.encode().join(cmd_parts[1:])
        self._handle_cmd(cmd_str, bin_in)

    #--------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from dummy.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".

        Raises
        ----------
        """

        bin_var = self._bin_out[:size]
        self._bin_out = self._bin_out[size:]
        return bin_var

    #--------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from dummy.

        Parameters
        ----------

        Returns
        ----------
        str
            String with data.

        Raises
        ----------
        """

        return self._data_out if isinstance(self._data_out, str) else str(self._data_out)

    #--------------------------------------------------------------------------
    def _handle_cmd(self, cmd_str: str, bin_in: bytes = 0) -> None:
        """
        Parse command and split it into command, parameters and arguments. Then execute associated command method found in command dictionary.
        If the command is not in the command dictionary, respond with the default response ('0'). The command is stored in the command history
        (see :func:`ieee488_2.transport.base_dummy_transport.get_cmd_hist`).

        Parameters
        ----------
        cmd_str : str
            Command
        bin_in : bytes
            Binary data that needs to be send by the command.

        Returns
        ----------

        Raises
        ----------
        """

        cmd_parts  = cmd_str.split(' ')
        cmd_params = re.findall("[0-9]+", cmd_parts[0])
        cmd_args   = cmd_parts[1].split(',') if len(cmd_parts) > 1 else []
        cmd_args   = [arg.strip('"') for arg in cmd_args]
        cmd_str    = re.sub("[0-9]+", '#', cmd_parts[0])
        self._cmd_hist.append(cmd_str)

        if cmd_str in self._cmds:
            self._cmds[cmd_str](cmd_params, cmd_args, bin_in)
        else:
            self._data_out = 0
            self._bin_out  = self._encode_bin('0'.encode())

    #--------------------------------------------------------------------------
    @staticmethod
    def _encode_bin(data: bytes, end_of_line: bool=True) -> None:
        """
        Encode binary data to be compatible with IEEE488.2.

        Parameters
        ----------
        data : bytes
            Binary data.
        end_of_line: bool
            Indicates if end-of-line needs to be added.

        Returns
        ----------

        Raises
        ----------
        """

        header_b = str(len(data)).encode()
        header_a = ('#' + str(len(header_b))).encode()
        if end_of_line:
            out = header_a + header_b + data + '\r\n'.encode()
        else:
            out = header_a + header_b + data

        return out

    #--------------------------------------------------------------------------
    @staticmethod
    def _decode_bin(data: bytes) -> bytes:
        """
        Decode IEEE488.2 binary data.

        Parameters
        ----------
        data : bytes
            Binary data.

        Returns
        ----------

        Raises
        ----------
        RunTimeError
            Header error.
        """

        header_a = data[:2].decode() #Read '#N'
        data = data[2:]

        if header_a[0] != '#':
            raise RuntimeError('Header error: received {}'.format(header_a))
        header_b = data[:int(header_a[1])].decode()
        data = data[int(header_a[1]):]

        return data[:int(header_b)]

    #--------------------------------------------------------------------------
    def get_cmd_hist(self) -> list:
        """
        Get list of every executed command since the initialization or reset of the class.

        Parameters
        ----------

        Returns
        ----------
        list
            List of executed command strings including arguments (does not include binary data argument).

        Raises
        ----------
        """

        return self._cmd_hist

    #--------------------------------------------------------------------------
    def _get_cmds(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get SCPI commands.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = "THe:CAke:Is:A:LIe;cake;str;get_cake;lie;cake;str;0;Your trusty AI companion promised you a cake.;"

    #--------------------------------------------------------------------------
    def _get_idn(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get device identity and build information.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = "Qblox," + \
                         "Qblox Dummy," + \
                         "whatever," + \
                         "fwVersion=0.0.0 fwBuild=28/11/1967-00:00missing:00 fwHash=0xDEADBEAF fwDirty=0 " + \
                         "kmodVersion=0.0.0 kmodBuild=15/07/1943-00:00:00 kmodHash=0x0D15EA5E kmodDirty=0 " + \
                         "swVersion=0.0.0 swBuild=11/05/1924-00:00:00 swHash=0xBEEFBABE swDirty=0"

    #--------------------------------------------------------------------------
    def _reset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Reset dummy.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self.close()

    #--------------------------------------------------------------------------
    def _get_system_error(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get system error from queue (see `SCPI <https://www.ivifoundation.org/docs/scpi-99.pdf>`_).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if len(self._system_error) > 0:
            self._data_out = '0,' + self._system_error[0]
            self._system_error = self._system_error[1:]
        else:
            self._data_out = "No error"

    #--------------------------------------------------------------------------
    def _get_system_error_cnt(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of system errors (see `SCPI <https://www.ivifoundation.org/docs/scpi-99.pdf>`_).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(len(self._system_error))

#-- class ---------------------------------------------------------------------

class pulsar_dummy_transport(base_dummy_transport):
    """
    Class to replace Pulsar device with dummy device to support software stack testing without hardware.
    The class implements all mandatory, required and Pulsar specific SCPI calls. Call reponses are
    largely artifically constructed to be inline with the call's functionality (e.g. `*IDN?` returns valid,
    but artificial IDN data.) To assist development, the Q1ASM assembler has been completely implemented.
    Please have a look at the call's implentation to know what to expect from its response.
    """

    #--------------------------------------------------------------------------
    def __init__(self, acq_scope_cfg_format: str, sequencer_cfg_format: str, is_rf_type: bool = False) -> None:
        """
        Create Pulsar dummy transport class.

        Parameters
        ----------
        acq_scope_cfg_format : str
            Configuration format based on `struct.pack <https://docs.python.org/3/library/struct.html>`_ format
            used to calculate scope acquisition configuration transaction size.
        sequencer_cfg_format : str
            Configuration format based on `struct.pack <https://docs.python.org/3/library/struct.html>`_ format
            used to calculate sequencer configuration transaction size.
        is_rf_type : bool
            Dummy module type (False = RF, True = baseband)

        Returns
        ----------

        Raises
        ----------
        """

        super(pulsar_dummy_transport, self).__init__()

        self._lo_hw_present          = is_rf_type
        self._asm_status             = False
        self._asm_log                = ''
        self._acq_scope_cfg          = {}
        self._sequencer_cfg          = {}
        self._acq_scope_cfg_bin_size = struct.calcsize(acq_scope_cfg_format)
        self._sequencer_cfg_bin_size = struct.calcsize(sequencer_cfg_format)
        self._awg_waveforms          = {}
        self._acq_weights            = {}
        self._acq_acquisitions       = {}
        self._channelmap             = {}

        self._cmds["LO:PRESent?"]                                = self._get_lo_hw_present
        self._cmds["STATus:ASSEMbler:SUCCess?"]                  = self._get_assembler_status
        self._cmds["STATus:ASSEMbler:LOG?"]                      = self._get_assembler_log
        self._cmds["ACQ:SCOpe:CONFiguration"]                    = self._set_acq_scope_config
        self._cmds["ACQ:SCOpe:CONFiguration?"]                   = self._get_acq_scope_config
        self._cmds["SEQuencer#:PROGram"]                         = self._set_sequencer_program
        self._cmds["SEQuencer#:CONFiguration"]                   = self._set_sequencer_config
        self._cmds["SEQuencer#:CONFiguration?"]                  = self._get_sequencer_config
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:NEW"]          = self._add_awg_waveform
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:DELete"]       = self._del_awg_waveform
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:DATA"]         = self._set_awg_waveform_data
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:DATA?"]        = self._get_awg_waveform_data
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:INDex"]        = self._set_awg_waveform_index
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:INDex?"]       = self._get_awg_waveform_index
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:LENGth?"]      = self._get_awg_waveform_length
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:NAME?"]        = self._get_awg_waveform_name
        self._cmds["SEQuencer#:AWG:WLISt:SIZE?"]                 = self._get_num_awg_waveforms
        self._cmds["SEQuencer#:AWG:WLISt?"]                      = self._get_awg_waveforms
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:NEW"]            = self._add_acq_weight
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:DELete"]         = self._del_acq_weight
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:DATA"]           = self._set_acq_weight_data
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:DATA?"]          = self._get_acq_weight_data
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:INDex"]          = self._set_acq_weight_index
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:INDex?"]         = self._get_acq_weight_index
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:LENGth?"]        = self._get_acq_weight_length
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:NAME?"]          = self._get_acq_weight_name
        self._cmds["SEQuencer#:ACQ:WLISt:SIZE?"]                 = self._get_num_acq_weights
        self._cmds["SEQuencer#:ACQ:WLISt?"]                      = self._get_acq_weights
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:NEW"]       = self._add_acq_acquisition
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:DELete"]    = self._del_acq_acquisition
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:DATA"]      = self._set_acq_acquisition_data
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:DATA?"]     = self._get_acq_acquisition_data
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:INDex"]     = self._set_acq_acquisition_index
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:INDex?"]    = self._get_acq_acquisition_index
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:NUM_BINS?"] = self._get_acq_acquisition_num_bins
        self._cmds["SEQuencer#:ACQ:ALISt:SIZE?"]                 = self._get_num_acq_acquisitions
        self._cmds["SEQuencer#:ACQ:ALISt?"]                      = self._get_acq_acquisitions
        self._cmds["SEQuencer#:CHANnelmap"]                      = self._set_channelmap
        self._cmds["SEQuencer#:CHANnelmap?"]                     = self._get_channelmap

    #--------------------------------------------------------------------------
    def _get_lo_hw_present(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler status. Refer to the assembler log to get more information regarding the assembler result.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(int(self._lo_hw_present))

    #--------------------------------------------------------------------------
    def _get_assembler_status(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler status. Refer to the assembler log to get more information regarding the assembler result.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(int(self._asm_status))

    #--------------------------------------------------------------------------
    def _get_assembler_log(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler log.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._bin_out = self._encode_bin(self._asm_log.encode())



    #--------------------------------------------------------------------------
    def _set_acq_scope_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of scope acquisition; untouched and in binary format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._acq_scope_cfg = self._decode_bin(bin_in)

    #--------------------------------------------------------------------------
    def _get_acq_scope_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of scope acquisition. If no configuration was previously stored an array of
        zero bytes is returned. The length of the returned array is calculated based on the configuration format set during initialization
        of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if len(self._acq_scope_cfg):
            self._bin_out = self._encode_bin(self._acq_scope_cfg)
        else:
            self._bin_out = self._encode_bin(self._acq_scope_cfg_bin_size*b'\x00')



    #--------------------------------------------------------------------------
    def _set_sequencer_program(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Runs provided sequencer Q1ASM program through assembler. The assembler is a pre-compiled application, which is selected based on the platform this method
        is called on. The assembler status and log are stored and can be retrieved using corresponding methods. On a failure to assemble an error is set in
        system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        q1asm_str = self._decode_bin(bin_in).decode()
        fid = open("./tmp.q1asm", 'w')
        fid.write(q1asm_str)
        fid.close()

        if os.name == 'nt':
            assembler_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/assembler/q1asm_windows.exe")
            proc = subprocess.Popen([assembler_path, "-o", "tmp", "tmp.q1asm"], shell=True, text=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        elif sys.platform == 'darwin':
            assembler_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/assembler/q1asm_macos")
            proc = subprocess.Popen([assembler_path + " -o tmp tmp.q1asm"], shell=True, text=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        else:
            assembler_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/assembler/q1asm_linux")
            proc = subprocess.Popen([assembler_path + " -o tmp tmp.q1asm"], shell=True, text=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self._asm_log    = proc.communicate()[0]
        self._asm_status = not proc.returncode

        if not self._asm_status:
            self._system_error.append("Assembly failed.")

    #--------------------------------------------------------------------------
    def _set_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of indexed sequencer; untouched and in binary format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._sequencer_cfg[cmd_params[0]] = self._decode_bin(bin_in)

    #--------------------------------------------------------------------------
    def _get_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of the indexed sequencer. If no configuration was previously stored an array of
        zero bytes is returned. The length of the returned array is calculated based on the configuration format set during initialization
        of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._sequencer_cfg:
            self._bin_out = self._encode_bin(self._sequencer_cfg[cmd_params[0]])
        else:
            self._bin_out = self._encode_bin(self._sequencer_cfg_bin_size*b'\x00')



    #--------------------------------------------------------------------------
    def _add_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds waveform to the waveform list of the indexed sequencer's AWG path. If the waveform name is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._system_error.append("Waveform {} already in waveform list.".format(cmd_args[0]))
                return

            for index in range(0, len(self._awg_waveforms[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._awg_waveforms[cmd_params[0]]:
                    if self._awg_waveforms[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused == True:
                    break
        else:
            self._awg_waveforms[cmd_params[0]] = {}
            index = 0
        self._awg_waveforms[cmd_params[0]][cmd_args[0]] = {"wave": bytearray([]), "index": index}

    #--------------------------------------------------------------------------
    def _del_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes waveform from the waveform list of the indexed sequencer's AWG path. If the waveform name does not exist, an error is set in system error.
        The names "all" and "ALL" are reserved and those are deleted all waveforms in the waveform list of the indexed sequencer's AWG path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_args[0].lower() == 'all':
            self._awg_waveforms[cmd_params[0]] = {}
        else:
            if cmd_params[0] in self._awg_waveforms:
                if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                    del self._awg_waveforms[cmd_params[0]][cmd_args[0]]
                    return
            self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform data for the waveform in the waveform list of the indexed sequencer's AWG path.
        If the waveform name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform data of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the waveform name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._bin_out = self._encode_bin(self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"])
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform index of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the waveform name does not exist or the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                for name in self._awg_waveforms[cmd_params[0]]:
                    if self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[1] and name != cmd_args[0]:
                        self._system_error.append("Waveform index {} already in use by {}.".format(cmd_args[0], name))
                        return
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform index of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the waveform name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._data_out = self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"]
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform length of the waveform in the waveform list of the indexed sequencer's AWG path. The waveform lenght is returned as the number of samples.
        If the waveform name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._data_out = int(len(self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"])/4)
                return
        self._system_error.append("Waveform {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_awg_waveform_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform name of the waveform in the waveform list of the indexed sequencer's AWG path.
        If the waveform name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            for name in self._awg_waveforms[cmd_params[0]]:
                if self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name[1:-1]
                    return
        self._system_error.append("Waveform index {} does not exist in waveform list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_num_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Number of waveforms in the waveform list of the indexed sequencer's AWG path.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            self._data_out = len(self._awg_waveforms[cmd_params[0]])
        else:
            self._data_out = 0

    #--------------------------------------------------------------------------
    def _get_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get every waveform in the waveform list of the indexed sequencer's AWG path.
        The waveforms are returned in a binary structure.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if len(self._awg_waveforms[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True
            self._bin_out = self._encode_bin(struct.pack('I', len(self._awg_waveforms[cmd_params[0]])), end_of_line)

            for it, name in enumerate(self._awg_waveforms[cmd_params[0]]):
                if it < len(self._awg_waveforms[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(struct.pack('I', int(self._awg_waveforms[cmd_params[0]][name]["index"])), False)
                self._bin_out += self._encode_bin(self._awg_waveforms[cmd_params[0]][name]["wave"], end_of_line)
        else:
            self._bin_out = self._encode_bin(struct.pack('I', 0), True)



    #--------------------------------------------------------------------------
    def _add_acq_weight(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds weight to the weight list of the indexed sequencer's acquisition path. If the weight name is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._system_error.append("Weight {} already in weight list.".format(cmd_args[0]))
                return

            for index in range(0, len(self._acq_weights[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._acq_weights[cmd_params[0]]:
                    if self._acq_weights[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused == True:
                    break
        else:
            self._acq_weights[cmd_params[0]] = {}
            index = 0
        self._acq_weights[cmd_params[0]][cmd_args[0]] = {"wave": bytearray([]), "index": index}

    #--------------------------------------------------------------------------
    def _del_acq_weight(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes weight from the weight list of the indexed sequencer's acquisition path. If the weight name does not exist, an error is set in system error.
        The names "all" and "ALL" are reserved and those are deleted all weights in the weight list of the indexed sequencer's acquisition path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_args[0].lower() == 'all':
            self._acq_weights[cmd_params[0]] = {}
        else:
            if cmd_params[0] in self._acq_weights:
                if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                    del self._acq_weights[cmd_params[0]][cmd_args[0]]
                    return
            self._system_error.append("Weight {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_weight_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets weight data for the weight in the weight list of the indexed sequencer's acquisition path.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
                return
        self._system_error.append("Weight {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_weight_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight data of the weight in the weight list of the indexed sequencer's acquisition path.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._bin_out = self._encode_bin(self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"])
                return
        self._system_error.append("Weight {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_weight_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets weight index of the weight in the weight list of the indexed sequencer's acquisition path.
        If the weight name does not exist or the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                for name in self._acq_weights[cmd_params[0]]:
                    if self._acq_weights[cmd_params[0]][name]["index"] == cmd_args[1] and name != cmd_args[0]:
                        self._system_error.append("Weight index {} already in use by {}.".format(cmd_args[0], name))
                        return
                self._acq_weights[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        self._system_error.append("Waveform {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_weight_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight index of the weight in the weight list of the indexed sequencer's acquisition path.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._data_out = self._acq_weights[cmd_params[0]][cmd_args[0]]["index"]
                return
        self._system_error.append("Weight {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_weight_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight length of the weight in the weight list of the indexed sequencer's acquisition path. The weight lenght is returned as the number of samples.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._data_out = int(len(self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"])/4)
                return
        self._system_error.append("Weight {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_weight_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight name of the weight in the weight list of the indexed sequencer's acquisition path.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            for name in self._acq_weights[cmd_params[0]]:
                if self._acq_weights[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name[1:-1]
                    return
        self._system_error.append("Weight index {} does not exist in weight list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_num_acq_weights(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight name of the weight in the weight list of the indexed sequencer's acquistion path.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            self._data_out = len(self._acq_weights[cmd_params[0]])
        else:
            self._data_out = 0

    #--------------------------------------------------------------------------
    def _get_acq_weights(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get every weight in the weight list of the indexed sequencer's acquistition path.
        The weights are returned in a binary structure.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if len(self._acq_weights[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True
            self._bin_out = self._encode_bin(struct.pack('I', len(self._acq_weights[cmd_params[0]])), end_of_line)

            for it, name in enumerate(self._acq_weights[cmd_params[0]]):
                if it < len(self._acq_weights[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(struct.pack('I', int(self._acq_weights[cmd_params[0]][name]["index"])), False)
                self._bin_out += self._encode_bin(self._acq_weights[cmd_params[0]][name]["wave"], end_of_line)
        else:
            self._bin_out = self._encode_bin(struct.pack('I', 0), True)



    #--------------------------------------------------------------------------
    def _add_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Add acquisition to acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._system_error.append("Acquisition {} already in acquisition list.".format(cmd_args[0]))
                return

            for index in range(0, len(self._acq_acquisitions[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._acq_acquisitions[cmd_params[0]]:
                    if self._acq_acquisitions[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused == True:
                    break
        else:
            self._acq_acquisitions[cmd_params[0]] = {}
            index = 0
        self._acq_acquisitions[cmd_params[0]][cmd_args[0]] = {"acq": {"scope": {"data": [bytearray([]),bytearray([])], "or": [False, False], "avg_cnt": [0, 0]}, "bins": [{"valid": False, "int": [0, 0], "thres": 0, "avg_cnt": 0} for _ in range(0, int(cmd_args[1]))]}, "index": index}

    #--------------------------------------------------------------------------
    def _del_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes acquisition from the acquisition list of the indexed sequencer. If the acquisition name does not exist, an error is set in system error.
        The names "all" and "ALL" are reserved and those are deleted all acquisitions in the acquisition list of the indexed sequencer are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0].lower() == 'all':
                self._acq_acquisitions[cmd_params[0]] = {}
            else:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                    del self._acq_acquisitions[cmd_params[0]][cmd_args[0]]
                    return
                self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds scope acquisition data to the selected acquisition in the specified sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                sample_width     = 12
                max_sample_value = 2**(sample_width-1)-1
                size             = 2**14-1
                self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][0] = struct.pack('i'*size, *[int(max_sample_value/size)*i for i in range(0, size)])
                self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][1] = struct.pack('i'*size, *[max_sample_value-int(max_sample_value/size)*i for i in range(0, size)])
                return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get acquisition data of a single acquisition from the specified sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._bin_out = self._encode_bin(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][0], False)
                self._bin_out += self._encode_bin(struct.pack('?', self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["or"][0]), False)
                self._bin_out += self._encode_bin(struct.pack('I', self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["avg_cnt"][0]), False)
                self._bin_out += self._encode_bin(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][1], False)
                self._bin_out += self._encode_bin(struct.pack('?', self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["or"][1]), False)
                self._bin_out += self._encode_bin(struct.pack('I', self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["avg_cnt"][1]), False)

                num_bins = len(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"])
                bins = []
                for bin_it in range(0, num_bins):
                    bins.append(int(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["valid"]))
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["int"][0])
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["int"][1])
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["thres"])
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["avg_cnt"])
                self._bin_out += self._encode_bin(struct.pack('='+num_bins*'QqqLL', *bins), True)
                return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _set_acq_acquisition_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets acquisition index of the acquisition in the acquisition list of the indexed sequencer's acquisition path.
        If the acquisition name does not exist or the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                for name in self._acq_acquisitions[cmd_params[0]]:
                    if self._acq_acquisitions[cmd_params[0]][name]["index"] == cmd_args[1] and name != cmd_args[0]:
                        self._system_error.append("Weight index {} already in use by {}.".format(cmd_args[0], name))
                        return
                self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_acquisition_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets acquisition index of the acquisition in the acquisition list of the indexed sequencer's acquisition path.
        If the acquisition name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._data_out = self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["index"]
                return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_acq_acquisition_num_bins(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of bins of the acquisition in the specified sequencer's acquisition list.
        If the acquisition name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._data_out = int(len(self._acq_acquisitions[cmd_params[0]]["acq"]["bins"]))
                return
        self._system_error.append("Acquisition {} does not exist in acquisition list.".format(cmd_args[0]))

    #--------------------------------------------------------------------------
    def _get_num_acq_acquisitions(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of acquisitions in the specified sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = 0
        if cmd_params[0] in self._acq_acquisitions:
            self._data_out = len(self._acq_acquisitions[cmd_params[0]])
            return

    #--------------------------------------------------------------------------
    def _get_acq_acquisitions(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Return all acquisitions in the specied sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if len(self._acq_acquisitions[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True
            self._bin_out = self._encode_bin(struct.pack('I', len(self._acq_acquisitions[cmd_params[0]])), end_of_line)

            for it, name in enumerate(self._acq_acquisitions[cmd_params[0]]):
                if it < len(self._acq_acquisitions[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(struct.pack('I', int(self._acq_acquisitions[cmd_params[0]][name]["index"])), False)

                self._bin_out += self._encode_bin(self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["data"][0], False)
                self._bin_out += self._encode_bin(struct.pack('?', self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["or"][0]), False)
                self._bin_out += self._encode_bin(struct.pack('I', self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["avg_cnt"][0]), False)
                self._bin_out += self._encode_bin(self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["data"][1], False)
                self._bin_out += self._encode_bin(struct.pack('?', self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["or"][1]), False)
                self._bin_out += self._encode_bin(struct.pack('I', self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["avg_cnt"][1]), False)

                num_bins = len(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"])
                bins = []
                for bin_it in range(0, num_bins):
                    bins.append(int(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["valid"]))
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["int"][0])
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["int"][1])
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["thres"])
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["avg_cnt"])
                self._bin_out += self._encode_bin(struct.pack('='+num_bins*'QqqLL', *bins), end_of_line)
        else:
            self._bin_out = self._encode_bin(struct.pack('I', 0), True)

    # --------------------------------------------------------------------------
    def _set_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the channelmap list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        sequencer_idx: str = cmd_params[0]
        channel_map_bin = self._decode_bin(bin_in)
        channel_map = list(
            struct.unpack("I" * int(len(channel_map_bin) / 4), channel_map_bin)
        )
        self._channelmap[sequencer_idx] = channel_map

    # --------------------------------------------------------------------------
    def _get_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the channelmap list. If not set previously, returns an empty list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        channel_map = list()
        if cmd_params[0] in self._channelmap:
            channel_map = self._channelmap[cmd_params[0]]
        channel_map_packed = struct.pack("I" * len(channel_map), *channel_map)
        self._bin_out = self._encode_bin(channel_map_packed)

#-- class ---------------------------------------------------------------------

class cluster_dummy_transport(base_dummy_transport):
    """
    Class to replace Cluster device with dummy device to support software stack testing without hardware.
    The class implements all mandatory, required and Cluster specific SCPI calls. Call reponses are
    largely artifically constructed to be inline with the call's functionality (e.g. `*IDN?` returns valid,
    but artificial IDN data.) To assist development, the Q1ASM assembler has been completely implemented.
    Please have a look at the call's implentation to know what to expect from its response.
    """

    #--------------------------------------------------------------------------
    def __init__(self) -> None:
        """
        Create Cluster dummy transport class.

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        """

        super(cluster_dummy_transport, self).__init__()

        self._mod_present = (1<<20)-1

        self._cmds["BP:MODules?"] = self._get_modules_present

    #--------------------------------------------------------------------------
    def _get_modules_present(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get modules present in the Cluster.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = self._mod_present
