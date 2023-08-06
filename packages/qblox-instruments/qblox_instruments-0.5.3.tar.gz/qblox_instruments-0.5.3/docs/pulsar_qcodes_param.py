#------------------------------------------------------------------------------
# Description    : Generate Pulsar QCoDeS parameters RST
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------

#-- include -------------------------------------------------------------------

import os
import re

from pulsar_qcm.pulsar_qcm import pulsar_qcm_dummy
from pulsar_qrm.pulsar_qrm import pulsar_qrm_dummy
from cluster.cluster       import cluster_dummy
from spi_rack.spi_rack     import dummy_spi_api, spi_rack, d5a_module

#-- functions -----------------------------------------------------------------

def create_pulsar_qcodes_param_rst(instrument, filename):
    """
    Get QCoDeS instrument parameters, parse them and write them in RST format to a file.

    Parameters
    ----------
    instrument : qcodes.Instrument
        Instrument to generate file for.
    filename : str
        RST file name to generate.

    Returns
    ----------

    Raises
    ----------
    """

    #Parse all parameters
    file = open(filename, 'w')
    for call in instrument.snapshot()['parameters']:

        #Get info from doc string
        doc_str_list = getattr(instrument, call).__doc__.split('\n')
        doc_str_list = [doc_str_part.rstrip() for doc_str_part in doc_str_list]
        if doc_str_list[0] == "Parameter class:":
            param_doc_str_idx = None
            param_name_idx    = 2
            param_unit_idx    = 4
            param_val_idx     = 5
        else:
            param_doc_str_idx = 0
            param_name_idx    = 4
            param_unit_idx    = 6
            param_val_idx     = 7

        param_name = doc_str_list[param_name_idx].split('`')[2][1:]
        param_unit = doc_str_list[param_unit_idx].split('`')[2][1:]
        param_val  = doc_str_list[param_val_idx].split('`')[2][2:-1]
        if param_doc_str_idx is not None:
            param_doc_str = doc_str_list[param_doc_str_idx]
        else:
            param_doc_str = "Please see `QCoDeS <https://qcodes.github.io/Qcodes/>`_ for a description."

        #Write to file
        seq_idx_match = re.search("^sequencer([\d*]*).*", param_name)
        mod_idx_match = re.search("^module([\d*]*).*", param_name)
        if (seq_idx_match is None and mod_idx_match is None) or \
           (seq_idx_match is not None and seq_idx_match.group(1) == '0') or \
           (mod_idx_match is not None and mod_idx_match.group(1) == '1'):
            #Parameter name
            param_name = instrument.name + '.' + param_name
            file.write(".. _" + param_name + ':\n\n')
            header_line = f":code:`{param_name}`\n"
            under_line = "~" * (len(header_line) - 1) + "\n"
            file.write(header_line + under_line)

            #Doc string
            if param_doc_str != "":
                file.write("  " + param_doc_str + '\n')
            file.write('\n')

            #Properties
            file.write("  :Properties:\n")
            if param_unit != "":
                file.write("    - **unit**: " + param_unit + '\n')
            if param_val != "":
                file.write("    - **value**: " + param_val + '\n')
            file.write('\n')

    file.close()

#-- main ----------------------------------------------------------------------

#Create QCoDeS driver objects
qcm   = pulsar_qcm_dummy("pulsar_qcm")
qrm   = pulsar_qrm_dummy("pulsar_qrm")
clstr = cluster_dummy("cluster")
spi   = spi_rack("spi_rack", "COM2", is_dummy=True)

#Generate RST files
script_dir = os.path.dirname(os.path.realpath(__file__))
result_dir = os.path.join(script_dir, "_build")
if os.path.isdir(result_dir) is False:
    os.mkdir(result_dir)

create_pulsar_qcodes_param_rst(qcm,   os.path.join(result_dir, "pulsar_qcm_qcodes_param.rst"))
create_pulsar_qcodes_param_rst(qrm,   os.path.join(result_dir, "pulsar_qrm_qcodes_param.rst"))
create_pulsar_qcodes_param_rst(clstr, os.path.join(result_dir, "cluster_qcodes_param.rst"))

create_pulsar_qcodes_param_rst(spi, os.path.join(result_dir, "spi_rack_qcodes_param.rst"))
spi.add_spi_module(1, "D5a", is_dummy=True)
create_pulsar_qcodes_param_rst(spi.module1.dac0, os.path.join(result_dir, "d5a_qcodes_param.rst"))
spi.add_spi_module(2, "S4g", is_dummy=True)
create_pulsar_qcodes_param_rst(spi.module2.dac0, os.path.join(result_dir, "s4g_qcodes_param.rst"))
