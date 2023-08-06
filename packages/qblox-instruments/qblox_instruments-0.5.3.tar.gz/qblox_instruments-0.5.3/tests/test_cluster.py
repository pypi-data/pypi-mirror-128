#------------------------------------------------------------------------------
# Description    : Pulsar QCM test script
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

import pytest
from tests           import generic
from cluster.cluster import cluster_dummy

#-- fixtures ------------------------------------------------------------------
@pytest.fixture(name="cluster_dummy")
def make_dummy_cluster():
    clstr = cluster_dummy("cluster")
    yield clstr

    # clean up when done
    clstr.close()


#-- functions -----------------------------------------------------------------

#------------------------------------------------------------------------------
def test__invalidate_qcodes_parameter_cache(cluster_dummy):
    """
    Tests if the cache invalidation method sets the `valid` attribute on the qcodes parameter cache to `False`.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test__invalidate_qcodes_parameter_cache(cluster_dummy)

#------------------------------------------------------------------------------
def test_reset_cache_invalidation(cluster_dummy):
    """
    Tests if the call to reset also invalidates the caches on the qcodes parameters.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_reset_cache_invalidation(cluster_dummy)

#------------------------------------------------------------------------------
def test_str(cluster_dummy):
    """
    Test string representation based in __str__

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_str(cluster_dummy, "cluster_dummy", "cluster")

#------------------------------------------------------------------------------
def test_get_scpi_commands(cluster_dummy):
    """
    Tests get SCPI commands function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_get_scpi_commands(cluster_dummy)

#------------------------------------------------------------------------------
def test_get_idn(cluster_dummy):
    """
    Tests get IDN function call. If no exceptions occur and the returned object matches
    the json schema the test passes.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_get_idn(cluster_dummy)

#------------------------------------------------------------------------------
def test_scpi_commands(cluster_dummy):
    """
    Tests remaining mandatory SCPI commands. If no exceptions occur the test passes.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_scpi_commands(cluster_dummy)

#------------------------------------------------------------------------------
def test_get_system_status(cluster_dummy):
    """
    Tests get system status function call. If no exceptions occur the test passes.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    assert cluster_dummy.get_system_status() == {'status': '0', 'flags': []}

#------------------------------------------------------------------------------
def test_get_temp(cluster_dummy):
    """
    Tests temperature readout function calls.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_get_temp(cluster_dummy)
    assert cluster_dummy.get_current_bp_temperature_0() == 0.0
    assert cluster_dummy.get_maximum_bp_temperature_0() == 0.0
    assert cluster_dummy.get_current_bp_temperature_1() == 0.0
    assert cluster_dummy.get_maximum_bp_temperature_1() == 0.0
    assert cluster_dummy.get_current_bp_temperature_2() == 0.0
    assert cluster_dummy.get_maximum_bp_temperature_2() == 0.0

#------------------------------------------------------------------------------
def test_ref_src(cluster_dummy):
    """
    Tests reference source setting and getting function calls.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    generic.test_ref_src(cluster_dummy)

#------------------------------------------------------------------------------
def test_module_present(cluster_dummy):
    """
    Tests module present function calls.

    Parameters
    ----------
    cluster_dummy: test_fixture
        Dummy Cluster test fixture

    Returns
    ----------

    Raises
    ----------
    """

    for slot_idx in range(1, 21):
        assert cluster_dummy.get("module{}_present".format(slot_idx)) == "present"