#------------------------------------------------------------------------------
# Description    : Generic test functions
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import scipy.signal
import math
import os
import json
import struct
import re
import sys

from jsonschema import validate

#------------------------------------------------------------------------------
def test__invalidate_qcodes_parameter_cache(instrument):
    """
    Tests if the cache invalidation method sets the `valid` attribute on the qcodes parameter cache to `False`.

    Parameters
    ----------
    instrument
        Reference to the instrument to perform the test on.
    """
    instrument._invalidate_qcodes_parameter_cache()
    for param in instrument.parameters.values():
        assert param.cache.valid is False

#------------------------------------------------------------------------------
def test_reset_cache_invalidation(instrument):
    """
    Tests if the call to reset also invalidates the caches on the qcodes parameters.

    Parameters
    ----------
    instrument
        Reference to the instrument to perform the test on.
    """
    instrument.reset()
    for param in instrument.parameters.values():
        assert param.cache.valid is False

#------------------------------------------------------------------------------
def test_str(instrument, class_name, instrument_name):
    """
    Test string representation based in __str__

    Parameters
    ----------
    name
        instrument name

    Returns
    ----------

    Raises
    ----------
    """

    assert str(instrument) == "<{}: {}>".format(class_name, instrument_name)

#------------------------------------------------------------------------------
def test_get_scpi_commands(instrument):
    """
    Tests get SCPI commands function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    instrument
        Instrument driver object

    Returns
    ----------

    Raises
    ----------
    """

    #Get SCPI commands
    scpi_cmds = instrument._get_scpi_commands()

    #Check SCPI commands
    scpi_cmds_schema = {"title": "Command container.",
                        "description": "Contains commands.",
                        "type":        "object",
                        "required":    ["scpi_in_type", "scpi_out_type", "python_func", "python_in_type", "python_in_var", "python_out_type", "comment"],
                        "properties": {
                            "scpi_in_type": {
                                "description": "SCPI input argument types",
                                "type":        "array"
                            },
                            "scpi_out_type": {
                                "description": "SCPI output types",
                                "type":        "array"
                            },
                            "python_func": {
                                "description": "Python function name",
                                "type":        "string"
                            },
                            "python_in_type": {
                                "description": "Python function input types",
                                "type":        "array"
                            },
                            "python_in_var": {
                                "description": "Python function input variable names",
                                "type":        "array"
                            },
                            "python_out_type": {
                                "description": "Python function output types",
                                "type":        "array"
                            },
                            "comment": {
                                "description": "Python function comment",
                                "type":        "string"
                            }
                  }}

    for scpi_cmd in scpi_cmds:
        validate(scpi_cmds[scpi_cmd], scpi_cmds_schema)

#------------------------------------------------------------------------------
def test_get_idn(instrument):
    """
    Tests get IDN function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    instrument
        Instrument driver object

    Returns
    ----------

    Raises
    ----------
    """

    #Get IDN
    idn = instrument.get_idn()

    #Check IDN
    idn_schema = {"title": "Device identification container.",
                  "description": "Contains device identification.",
                  "type":        "object",
                  "required":    ["manufacturer", "model", "serial_number", "firmware"],
                  "properties": {
                       "manufacturer": {
                           "description": "Manufacturer name",
                           "type":        "string"
                       },
                       "model": {
                           "description": "Model name",
                           "type":        "string"
                       },
                       "serial_number": {
                           "description": "Serial number",
                           "type":        "string"
                       },
                       "firmware": {
                           "description": "Firmware build information",
                           "type":        "object",
                           "required":    ["fpga", "kernel_mod", "application", "driver"],
                           "properties": {
                               "fpga": {
                                   "description": "FPGA firmware build information",
                                   "type":        "object",
                               },
                               "kernel_mod": {
                                   "description": "Kernel module build information",
                                   "type":        "object",
                               },
                               "application": {
                                   "description": "Application build information",
                                   "type":        "object",
                               },
                               "driver": {
                                   "description": "Driver build information",
                                   "type":        "object",
                               }
                           }
                       }
                  }}

    build_schema = {"title":       "Build information container.",
                    "description": "Contains build information.",
                    "type":        "object",
                    "required":    ["version", "date", "hash", "dirty"],
                    "properties": {
                         "version": {
                             "description": "Version",
                             "type":        "string"
                         },
                         "date": {
                             "description": "Date",
                             "type":        "string"
                         },
                         "hash": {
                             "description": "Hash",
                             "type":        "string"
                         },
                         "dirty": {
                             "description": "Dirty bit",
                             "type":        "boolean"
                         }
                    }}

    validate(idn, idn_schema)
    validate(idn["firmware"]["fpga"],        build_schema)
    validate(idn["firmware"]["kernel_mod"],  build_schema)
    validate(idn["firmware"]["application"], build_schema)
    validate(idn["firmware"]["driver"],      build_schema)

#------------------------------------------------------------------------------
def test_scpi_commands(instrument):
    """
    Tests remaining mandatory SCPI commands. If no exceptions occur the test passes.

    Parameters
    ----------
    instrument
        Instrument driver object

    Returns
    ----------

    Raises
    ----------
    """

    #Functions without return value
    instrument.reset()
    instrument.clear()
    instrument.set_service_request_enable(0)
    instrument.set_standard_event_status_enable(0)
    instrument.set_operation_complete()
    instrument.wait()
    instrument.preset_system_status()
    instrument.set_questionable_enable(0)
    instrument.set_operation_enable(0)

    #Functions with return value (most return values are nonsense, because of dummy instrument)
    assert instrument.get_status_byte()                  == 0
    assert instrument.get_service_request_enable()       == 0
    assert instrument.get_standard_event_status_enable() == 0
    assert instrument.get_standard_event_status()        == 0
    assert instrument.get_operation_complete()           == False
    assert instrument.test()                             == False
    assert instrument.get_system_error()                 == "No error"
    assert instrument.get_num_system_error()             == 0
    assert instrument.get_system_version()               == "0"
    assert instrument.get_questionable_condition()       == 0
    assert instrument.get_questionable_event()           == 0
    assert instrument.get_questionable_enable()          == 0
    assert instrument.get_operation_condition()          == 0
    assert instrument.get_operation_events()             == 0
    assert instrument.get_operation_enable()             == 0

#------------------------------------------------------------------------------
def test_get_temp(instrument):
    """
    Tests temperature readout function calls.

    Parameters
    ----------
    instrument
        Instrument driver object

    Returns
    ----------

    Raises
    ----------
    """

    #Return values are always 0.0, because of dummy instrument
    assert instrument.get_current_carrier_temperature() == 0.0
    assert instrument.get_maximum_carrier_temperature() == 0.0
    assert instrument.get_current_fpga_temperature()    == 0.0
    assert instrument.get_maximum_fpga_temperature()    == 0.0

#------------------------------------------------------------------------------
def test_ref_src(instrument):
    """
    Tests reference source setting and getting function calls.

    Parameters
    ----------
    instrument
        Instrument driver object

    Returns
    ----------

    Raises
    ----------
    """

    #Set all possible inputs
    instrument.reference_source("internal")
    instrument.reference_source("external")

    #Set invalid input
    try:
        instrument.reference_source("random")
        assert False
    except Exception:
        pass

    #Dummy nonsense answer always returns "external"
    assert instrument.reference_source() == "external"

#------------------------------------------------------------------------------
def test_out_amp_offset(instrument, num_out):
    """
    Tests output amplifier offset setting and getting function calls.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    for out_idx in range(0, num_out):
        for path_idx in range(0, 2):
            #Check output offset function calls
            instrument.set("out{}_offset_path{}".format(out_idx, path_idx), 0)

            #Check offset settings
            try:
                instrument.set("out{}_offset_path{}".format(out_idx, path_idx), -85.0)
                assert False
            except Exception:
                pass

            try:
                instrument.set("out{}_offset_path{}".format(out_idx, path_idx), 74.0)
                assert False
            except Exception:
                pass

            #Dummy nonsense answer always returns 0
            assert instrument.get("out{}_offset_path{}".format(out_idx, path_idx)) == 0

#------------------------------------------------------------------------------
def test_out_dac_offset(instrument, num_dacs, max_v):
    """
    Tests output DAC offset setting and getting function calls.

    Parameters
    ----------

    Returns
    ----------

    Raises
    ----------
    """

    for idx in range(0, num_dacs):
        #Check output offset function calls
        instrument.set("out{}_offset".format(idx), 0)

        #Check offset settings
        try:
            instrument.set("out{}_offset".format(idx), -1 * (max_v + 0.1))
            assert False
        except Exception:
            pass
        try:
            instrument.set("out{}_offset".format(idx), max_v + 0.1)
            assert False
        except Exception:
            pass
        #Dummy nonsense answer always returns 0
        assert instrument.get("out{}_offset".format(idx)) == 0

#------------------------------------------------------------------------------
def test_waveform_weight_handling(instrument, tmpdir):
    """
    Tests waveform handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    instrument
        Instrument driver object
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    #Check if waveform and weight lists are empty
    assert instrument.get_waveforms(0) == {}
    if hasattr(instrument, 'get_weights') and callable(getattr(instrument, 'get_weights')):
        assert instrument.get_weights(0) == {}

    #Generate waveforms and weights
    waveform_length = 100
    waveforms = {
                    "gaussian": {"data": [], "index": 0},
                    "sine":     {"data": [], "index": 1},
                    "sawtooth": {"data": [], "index": 2},
                    "block":    {"data": [], "index": 3}
                }

    waveforms["gaussian"]["data"] = scipy.signal.gaussian(waveform_length, std=0.12 * waveform_length)
    waveforms["sine"]["data"]     = [math.sin((2 * math.pi / waveform_length) * i ) for i in range(0, waveform_length)]
    waveforms["sawtooth"]["data"] = [(1.0 / (waveform_length)) * i for i in range(0, waveform_length)]
    waveforms["block"]["data"]    = [1.0 for i in range(0, waveform_length)]

    #JSON only supports lists, so reformat waveforms to lists if necessary.
    for name in waveforms:
        if str(type(waveforms[name]["data"]).__name__) == "ndarray":
            waveforms[name]["data"] = waveforms[name]["data"].tolist()

    #Add waveforms, weights (and program) to single dictionary and write to JSON file.
    wave_and_prog_dict = {"waveforms": waveforms, "weights": waveforms, "acquisitions": {}, "program": "stop"}
    with open(os.path.join(tmpdir, "sequence.json"), 'w', encoding='utf-8') as file:
        json.dump(wave_and_prog_dict, file, indent=4)
        file.close()

    #Upload waveforms and weights
    instrument.sequencer0_waveforms_and_program(os.path.join(tmpdir, "sequence.json"))

    #Get waveforms from instrument and check waveforms and indexes
    waveforms_out = instrument.get_waveforms(0)
    for name in waveforms:
        assert waveforms[name]["index"] == waveforms_out[name]["index"]
        for sample0, sample1 in zip(waveforms[name]["data"], waveforms_out[name]["data"]):
            assert struct.unpack("f", struct.pack("f", sample0))[0] == sample1

    #Get weights from instrument and check weights and indexes
    if hasattr(instrument, 'get_weights') and callable(getattr(instrument, 'get_weights')):
        weights_out = instrument.get_weights(0)
        for name in waveforms:
            assert waveforms[name]["index"] == weights_out[name]["index"]
            for sample0, sample1 in zip(waveforms[name]["data"], weights_out[name]["data"]):
                assert struct.unpack("f", struct.pack("f", sample0))[0] == sample1

    #Delete waveforms and weights from JSON file
    wave_and_prog_dict = {"waveforms": {}, "weights": {}, "acquisitions": {}, "program": "stop"}
    with open(os.path.join(tmpdir, "sequence.json"), 'w', encoding='utf-8') as file:
        json.dump(wave_and_prog_dict, file, indent=4)
        file.close()

    #Upload waveforms and weights
    instrument.sequencer0_waveforms_and_program(os.path.join(tmpdir, "sequence.json"))

    #Get waveforms from instrument and check waveforms and indexes
    assert instrument.get_waveforms(0) == {}

    #Get weights from instrument and check weights and indexes
    if hasattr(instrument, 'get_weights') and callable(getattr(instrument, 'get_weights')):
        assert instrument.get_weights(0) == {}

#------------------------------------------------------------------------------
def test_program_handling(instrument, tmpdir):
    """
    Tests program handling function calls.

    Parameters
    ----------
    instrument
        Instrument driver object
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    #Program
    seq_prog = """
          move      1,R0        # Start at marker output channel 0 (move 1 into R0)
          nop                   # Wait a cycle for R0 to be available.

    loop: set_mrk   R0          # Set marker output channels to R0
          upd_param 1000        # Update marker output channels and wait 1us.
          asl       R0,1,R0     # Move to next marker output channel (left-shift R0).
          nop                   # Wait a cycle for R0 to be available.
          jlt       R0,16,@loop # Loop until all 4 marker output channels have been set once.

          set_mrk   0           # Reset marker output channels.
          upd_param 4           # Update marker output channels.
          stop                  # Stop sequencer.
    """

    #Add program (and waveforms) to single dictionary and write to JSON file.
    wave_and_prog_dict = {"waveforms": {}, "weights": {}, "acquisitions": {}, "program": seq_prog}
    with open(os.path.join(tmpdir, "sequence.json"), 'w', encoding='utf-8') as file:
        json.dump(wave_and_prog_dict, file, indent=4)
        file.close()

    #Upload program
    instrument.sequencer0_waveforms_and_program(os.path.join(tmpdir, "sequence.json"))

    #Get assembler status and log
    assert instrument.get_assembler_status() == True
    assert re.match(".*assembler finished successfully.*", instrument.get_assembler_log(), re.DOTALL) is not None

    #Add illegal program (and waveforms) to single dictionary and write to JSON file.
    wave_and_prog_dict = {"waveforms": {}, "weights": {}, "acquisitions": {}, "program": seq_prog + "\n random_instruction"}
    with open(os.path.join(tmpdir, "sequence.json"), 'w', encoding='utf-8') as file:
        json.dump(wave_and_prog_dict, file, indent=4)
        file.close()

    #Upload program (suppress error log printed by exception)
    try:
        old_stdout = sys.stdout
        new_stdout = open(os.devnull, 'w')
        sys.stdout = new_stdout
        instrument.sequencer0_waveforms_and_program(os.path.join(tmpdir, "sequence.json"))
        assert False
    except Exception:
        pass
    finally:
        sys.stdout = old_stdout

    #Get assembler status and log
    assert instrument.get_assembler_status() == False
    assert re.match(".*assembler failed with .* errors:.*", instrument.get_assembler_log(), re.DOTALL) is not None

#------------------------------------------------------------------------------
def test_sequencer_control(instrument):
    """
    Tests sequencer handling function calls.

    Parameters
    ----------
    instrument
        Instrument driver object

    Returns
    ----------

    Raises
    ----------
    """

    #Reading and writing to a single parameter will trigger a read and write of all sequencer settings.
    instrument.sequencer0_nco_freq(10e6)
    assert instrument.sequencer0_nco_freq() == 10e6

    #Check sequencer control
    instrument.arm_sequencer(0)
    instrument.start_sequencer(0)
    instrument.stop_sequencer(0)

    instrument.arm_sequencer()
    instrument.start_sequencer()
    instrument.stop_sequencer()

    #Get sequencer status (dummy returns nonsense status and flags)
    assert instrument.get_sequencer_state(0) == {'status': '0', 'flags': []}
