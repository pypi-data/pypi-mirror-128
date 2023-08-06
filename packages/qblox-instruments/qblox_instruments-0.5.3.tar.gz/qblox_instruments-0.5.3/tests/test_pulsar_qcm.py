#------------------------------------------------------------------------------
# Description    : Pulsar QCM test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import pytest
from tests                 import generic
from pulsar_qcm.pulsar_qcm import pulsar_qcm_dummy

#-- fixtures ------------------------------------------------------------------
@pytest.fixture(name="pulsar_dummy")
def make_dummy_qcm():
    pulsar = pulsar_qcm_dummy("pulsar")
    yield pulsar

    # clean up when done
    pulsar.close()

@pytest.fixture(name="pulsar_rf_dummy")
def make_dummy_qcm_rf():
    pulsar_rf = pulsar_qcm_dummy("pulsar", is_rf_type = True)
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

    generic.test_str(pulsar_dummy, "pulsar_qcm_dummy", "pulsar")

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

    for lo_idx in range(0, 2):
        #Check LO frequency function call
        pulsar_rf_dummy.set("out{}_lo_freq".format(lo_idx), 10e9)

        #Check LO frequency invalid values
        try:
            pulsar_rf_dummy.set("out{}_lo_freq".format(lo_idx), 1.9e9)
            assert False
        except Exception:
            pass

        #Check LO frequency invalid values
        try:
            pulsar_rf_dummy.set("out{}_lo_freq".format(lo_idx), 18.1e9)
            assert False
        except Exception:
            pass

        #Dummy nonsense answer always returns 0Hz
        assert pulsar_rf_dummy.get("out{}_lo_freq".format(lo_idx)) == 0

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

    generic.test_out_amp_offset(pulsar_rf_dummy, 2)

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

    generic.test_out_dac_offset(pulsar_dummy, 4, 2.5)

#------------------------------------------------------------------------------
def test_waveform_handling(pulsar_dummy, tmpdir):
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

    generic.test_waveform_weight_handling(pulsar_dummy, tmpdir)

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

    generic.test_program_handling(pulsar_dummy, tmpdir)

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

    generic.test_sequencer_control(pulsar_dummy)
