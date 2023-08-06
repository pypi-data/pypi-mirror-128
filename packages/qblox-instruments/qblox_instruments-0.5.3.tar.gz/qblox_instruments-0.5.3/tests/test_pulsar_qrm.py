#------------------------------------------------------------------------------
# Description    : Pulsar QRM test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import struct
import os
import json
import pytest

from tests                 import generic
from pulsar_qrm.pulsar_qrm import pulsar_qrm_dummy

#-- fixtures ------------------------------------------------------------------
@pytest.fixture(name="pulsar_dummy")
def make_dummy_qrm():
    pulsar = pulsar_qrm_dummy("pulsar")
    yield pulsar

    # clean up when done
    pulsar.close()

@pytest.fixture(name="pulsar_rf_dummy")
def make_dummy_qrm_rf():
    pulsar_rf = pulsar_qrm_dummy("pulsar", is_rf_type = True)
    yield pulsar_rf

    # clean up when done
    pulsar_rf.close()


#-- functions -----------------------------------------------------------------

#------------------------------------------------------------------------------
def test__invalidate_qcodes_parameter_cache(pulsar_dummy):
    """
    Tests if the cache invalidation method sets the `valid` attribute on the qcodes parameter cache to `False`.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test__invalidate_qcodes_parameter_cache(pulsar_dummy)

#------------------------------------------------------------------------------
def test_reset_cache_invalidation(pulsar_dummy):
    """
    Tests if the call to reset also invalidates the caches on the qcodes parameters.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_reset_cache_invalidation(pulsar_dummy)

#------------------------------------------------------------------------------
def test_str(pulsar_dummy):
    """
    Test string representation based in __str__

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_str(pulsar_dummy, "pulsar_qrm_dummy", "pulsar")

#------------------------------------------------------------------------------
def test_get_scpi_commands(pulsar_dummy):
    """
    Tests get SCPI commands function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_get_scpi_commands(pulsar_dummy)

#------------------------------------------------------------------------------
def test_get_idn(pulsar_dummy):
    """
    Tests get IDN function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_get_idn(pulsar_dummy)

#------------------------------------------------------------------------------
def test_scpi_commands(pulsar_dummy):
    """
    Tests remaining mandatory SCPI commands. If no exceptions occur the test passes.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_scpi_commands(pulsar_dummy)

#------------------------------------------------------------------------------
def test_get_system_status(pulsar_dummy):
    """
    Tests get system status function call. If no exceptions occur the test passes.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    assert pulsar_dummy.get_system_status() == {'status': '0', 'flags': []}

#------------------------------------------------------------------------------
def test_get_temp(pulsar_dummy):
    """
    Tests temperature readout function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_get_temp(pulsar_dummy)
    assert pulsar_dummy.get_current_afe_temperature() == 0.0
    assert pulsar_dummy.get_maximum_afe_temperature() == 0.0
    assert pulsar_dummy.get_current_lo_temperature()  == 0.0
    assert pulsar_dummy.get_maximum_lo_temperature()  == 0.0

#------------------------------------------------------------------------------
def test_ref_src(pulsar_dummy):
    """
    Tests reference source setting and getting function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_ref_src(pulsar_dummy)

#------------------------------------------------------------------------------
def test_lo_freq(pulsar_rf_dummy):
    """
    Tests LO frequency setting and getting function calls.

    Parameters
    ----------
    pulsar_rf_dummy: test_fixture
        Dummy RF Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    #Check LO frequency function call
    pulsar_rf_dummy.out0_in0_lo_freq(10e9)

    #Check LO frequency invalid values
    try:
        pulsar_rf_dummy.out0_in0_lo_freq(1.9e9)
        assert False
    except Exception:
        pass

    #Check LO frequency invalid values
    try:
        pulsar_rf_dummy.out0_in0_lo_freq(18.1e9)
        assert False
    except Exception:
        pass

    #Dummy nonsense answer always returns 0Hz
    assert pulsar_rf_dummy.out0_in0_lo_freq() == 0

#------------------------------------------------------------------------------
def test_in_amp_gain(pulsar_dummy):
    """
    Tests input amplifier gain setting and getting function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for idx in range(0, 2):
        #Check input amplifier gain function calls
        pulsar_dummy.set("in{}_gain".format(idx), 0)

        #Check invalid gain settings
        try:
            pulsar_dummy.set("in{}_gain".format(idx), -7)
            assert False
        except Exception:
            pass

        try:
            pulsar_dummy.set("in{}_gain".format(idx), 26)
            assert False
        except Exception:
            pass

        #Dummy nonsense answer always returns 0dB
        assert pulsar_dummy.get("in{}_gain".format(idx)) == 0

#------------------------------------------------------------------------------
def test_out_amp_offset(pulsar_rf_dummy):
    """
    Tests output amplifier offset setting and getting function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_out_amp_offset(pulsar_rf_dummy, 1)

#------------------------------------------------------------------------------
def test_out_dac_offset(pulsar_dummy):
    """
    Tests output DAC offset setting and getting function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_out_dac_offset(pulsar_dummy, 2, 1.0)

#------------------------------------------------------------------------------
def test_waveform_weight_handling(pulsar_dummy, tmpdir):
    """
    Tests waveform and weight handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_waveform_weight_handling(pulsar_dummy, tmpdir)

#------------------------------------------------------------------------------
def test_acquisition_handling(pulsar_dummy, tmpdir):
    """
    Tests waveform handling (e.g. adding, deleting) function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    #Check if acquisition list is empty
    assert pulsar_dummy.get_acquisitions(0) == {}

    #Define acquisitions
    acquisitions = {
                "acq0": {"num_bins": 10, "index": 0},
                "acq1": {"num_bins": 20, "index": 1},
                "acq2": {"num_bins": 30, "index": 2},
                "acq3": {"num_bins": 40, "index": 3}
            }

    #Add acquisitions (and program) to single dictionary and write to JSON file.
    wave_and_prog_dict = {"waveforms": {}, "weights": {}, "acquisitions": acquisitions, "program": "stop"}
    with open(os.path.join(tmpdir, "sequence.json"), 'w', encoding='utf-8') as file:
        json.dump(wave_and_prog_dict, file, indent=4)
        file.close()

    #Upload acquisitions
    pulsar_dummy.sequencer0_waveforms_and_program(os.path.join(tmpdir, "sequence.json"))

    #Store scope acquisitions
    for name in acquisitions:
        pulsar_dummy.store_scope_acquisition(0, name)

    #Get acquisitions
    acq_out = pulsar_dummy.get_acquisitions(0)

    #Check acquisition content
    sample_width     = 12
    max_sample_value = 2**(sample_width-1)-1
    size             = 2**14-1
    scope_acq0 = struct.unpack('i'*size, struct.pack('i'*size, *[int(max_sample_value/size)*i for i in range(0, size)]))
    scope_acq1 = struct.unpack('i'*size, struct.pack('i'*size, *[max_sample_value-int(max_sample_value/size)*i for i in range(0, size)]))
    for name in acq_out:
        assert acq_out[name]["index"] == acquisitions[name]["index"]
        for sample0, sample1 in zip(scope_acq0, acq_out[name]["acquisition"]["scope"]["path0"]["data"]):
            assert sample0/max_sample_value == sample1
        for sample0, sample1 in zip(scope_acq1, acq_out[name]["acquisition"]["scope"]["path1"]["data"]):
            assert sample0/max_sample_value == sample1
        assert len(acq_out[name]["acquisition"]["bins"]["integration"]["path0"]) == acquisitions[name]["num_bins"]
        assert len(acq_out[name]["acquisition"]["bins"]["integration"]["path1"]) == acquisitions[name]["num_bins"]
        assert len(acq_out[name]["acquisition"]["bins"]["threshold"])            == acquisitions[name]["num_bins"]
        assert len(acq_out[name]["acquisition"]["bins"]["avg_cnt"])              == acquisitions[name]["num_bins"]

    #Clear acquisitions
    wave_and_prog_dict = {"waveforms": {}, "weights": {}, "acquisitions": {}, "program": "stop"}
    with open(os.path.join(tmpdir, "sequence.json"), 'w', encoding='utf-8') as file:
        json.dump(wave_and_prog_dict, file, indent=4)
        file.close()

    #Upload empty acquisition list
    pulsar_dummy.sequencer0_waveforms_and_program(os.path.join(tmpdir, "sequence.json"))

    #Check acquisition list content
    assert pulsar_dummy.get_acquisitions(0) == {}

    #Get acquisition status (dummy returns nonsense)
    assert pulsar_dummy.get_acquisition_state(0) == False

#------------------------------------------------------------------------------
def test_program_handling(pulsar_dummy, tmpdir):
    """
    Tests program handling function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture
    tmpdir
        Temporary directory

    Returns
    ----------

    Raises
    ----------
    """

    #Check program handling function calls
    generic.test_program_handling(pulsar_dummy, tmpdir)

#------------------------------------------------------------------------------
def test_scope_acquisition_control(pulsar_dummy):
    """
    Tests scope acquisition control function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    pulsar_dummy.scope_acq_sequencer_select(1)
    assert pulsar_dummy.scope_acq_sequencer_select() == 1

#------------------------------------------------------------------------------
def test_sequencer_control(pulsar_dummy):
    """
    Tests program handling function calls.

    Parameters
    ----------
    pulsar_dummy: test_fixture
        Dummy Pulsar test fixture

    Returns
    ----------

    Raises
    ----------
    """

    #Check sequencer control function calls
    generic.test_sequencer_control(pulsar_dummy)
