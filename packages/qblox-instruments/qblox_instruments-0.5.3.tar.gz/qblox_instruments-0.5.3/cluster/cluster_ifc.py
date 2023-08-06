#------------------------------------------------------------------------------
# Description    : Cluster native interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import numpy

#Add Qblox instruments build info
from qblox_instruments import build

#Add SCPI support
from cluster.cluster_scpi_ifc import cluster_scpi_ifc

#-- class ---------------------------------------------------------------------

class cluster_ifc(cluster_scpi_ifc):
    """
    Class that provides the native API for the Cluster. It provides methods to control all
    functions and features provided by the Cluster.
    """

    #--------------------------------------------------------------------------
    def __init__(self, transport_inst, debug = 0):
        """
        Creates Cluster native interface object.

        Parameters
        ----------
        transport_inst : :class:`~ieee488_2.transport`
            Transport class responsible for the lowest level of communication (e.g. ethernet).
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------
        :class:`~cluster.cluster_ifc`
            Cluster native interface object.

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.
        """

        #Initialize parent class.
        super(cluster_ifc, self).__init__(transport_inst, debug)

    #--------------------------------------------------------------------------
    def _get_scpi_commands(self):
        """
        Get SCPI commands.

        Parameters
        ----------

        Returns
        ----------
        dict
            Dictionary containing all available SCPI commands, corresponding parameters, arguments and Python methods and finally a descriptive comment.

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Format command string
            cmds          = super()._get_scpi_commands()
            cmd_elem_list = cmds.split(';')[:-1]
            cmd_list      = numpy.reshape(cmd_elem_list, (int(len(cmd_elem_list) / 9), 9))
            cmd_dict      = {cmd[0]: {"scpi_in_type":    cmd[1].split(',') if cmd[1] != "None" and cmd[1] != "" else [],
                                      "scpi_out_type":   cmd[2].split(',') if cmd[2] != "None" and cmd[2] != "" else [],
                                      "python_func":     cmd[3],
                                      "python_in_type":  cmd[4].split(',') if cmd[4] != "None" and cmd[4] != "" else [],
                                      "python_in_var":   cmd[5].split(',') if cmd[5] != "None" and cmd[5] != "" else [],
                                      "python_out_type": cmd[6].split(',') if cmd[6] != "None" and cmd[6] != "" else [],
                                      "comment":         cmd[8]} for cmd in cmd_list}

            return cmd_dict
        except:
            raise

    #--------------------------------------------------------------------------
    def get_idn(self):
        """
        Get device identity and build information.

        Parameters
        ----------

        Returns
        ----------
        dict
            Dictionary containing manufacturer, model, serial number and build information. The build information is subdivided into FPGA firmware,
            kernel module software, application software and driver software build information. Each of those consist of the version, build date,
            build Git hash and Git build dirty indication.

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Format IDN string
            idn            = self._get_idn()
            idn_elem_list  = idn.split(',')
            idn_build_list = idn_elem_list[-1].split(' ')
            idn_dict       = {"manufacturer":  idn_elem_list[0],
                              "model":         idn_elem_list[1],
                              "serial_number": idn_elem_list[2],
                              "firmware":      {"fpga":        {"version": idn_build_list[0].split("=")[-1],
                                                                "date":    idn_build_list[1].split("=")[-1],
                                                                "hash":    idn_build_list[2].split("=")[-1],
                                                                "dirty":   int(idn_build_list[3].split("=")[-1]) > 0},
                                                "kernel_mod":  {"version": idn_build_list[4].split("=")[-1],
                                                                "date":    idn_build_list[5].split("=")[-1],
                                                                "hash":    idn_build_list[6].split("=")[-1],
                                                                "dirty":   int(idn_build_list[7].split("=")[-1]) > 0},
                                                "application": {"version": idn_build_list[8].split("=")[-1],
                                                                "date":    idn_build_list[9].split("=")[-1],
                                                                "hash":    idn_build_list[10].split("=")[-1],
                                                                "dirty":   int(idn_build_list[11].split("=")[-1]) > 0},
                                                "driver":       build.get_build_info()}}

            return idn_dict
        except:
            raise



    #--------------------------------------------------------------------------
    def get_system_status(self):
        """
        Get general system state.

        Parameters
        ----------

        Returns
        ----------
        dict
            Dictionary containing general status and corresponding flags:

            :Status:
                - OKAY: System is okay.
                - CRITICAL: An error indicated by the flags occured, but has been resolved.
                - ERROR: An error indicated by the flags is occuring.

            :Flags:
                - CARRIER_PLL_UNLOCK: Carrier board PLL is unlocked.
                - FPGA_PLL_UNLOCK: FPGA PLL is unlocked.
                - FPGA_TEMP_OR: FPGA temperature is out-of-range.
                - CARRIER_TEMP_OR: Carrier board temperature is out-of-range.

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            #Format status string
            status           = self._get_system_status()
            status_elem_list = status.split(';')
            status_flag_list = status_elem_list[-1].split(',')[:-1] if status_elem_list[-1] != '' else []
            status_dict      = {"status": status_elem_list[0],
                                "flags":  status_flag_list}
            return status_dict
        except:
            raise



#--------------------------------------------------------------------------
    def _get_modules_present(self, slot):
        """
        Get an indication of module presence for a specific slot in the Cluster.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20 to get module presence for.

        Returns
        ----------
        bool
            Module presence (False = not present, True = present).

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """

        try:
            return (int(super()._get_modules_present()) >> (slot - 1)) & 1 == 1
        except:
            raise
