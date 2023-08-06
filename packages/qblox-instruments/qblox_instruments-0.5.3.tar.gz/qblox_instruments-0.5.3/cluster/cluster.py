#------------------------------------------------------------------------------
# Description    : Cluster QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
#------------------------------------------------------------------------------


#-- include -------------------------------------------------------------------

from ieee488_2.transport   import ip_transport, cluster_dummy_transport
from cluster.cluster_ifc   import cluster_ifc
from pulsar_qcm.pulsar_qcm import pulsar_qcm, pulsar_qcm_dummy
from pulsar_qrm.pulsar_qrm import pulsar_qrm, pulsar_qrm_dummy
from qcodes                import validators as vals
from qcodes                import Instrument
from functools             import partial

#-- class ---------------------------------------------------------------------

class cluster_qcodes(cluster_ifc, Instrument):
    """
    This class connects `QCoDeS <https://qcodes.github.io/Qcodes/>`_ to the Cluster native interface. Do not directly instantiate this class, but instead instantiate either the
    :class:`~.cluster` or :class:`~.cluster_dummy`.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, transport_inst, debug=0):
        """
        Creates Cluster QCoDeS class and adds all relevant instrument parameters. These instrument parameters call the associated methods provided by the native interface.

        Parameters
        ----------
        name : str
            Instrument name.
        transport_inst : :class:`~ieee488_2.transport`
            Transport class responsible for the lowest level of communication (e.g. ethernet).
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.


        .. Note::

            To get a complete of list of the QCoDeS parameters, run the following code.

        .. code-block:: Python

            from cluster.cluster import cluster_dummy

            clstr = cluster_dummy("cluster")
            for call in clstr.snapshot()['parameters']:
                print(getattr(clstr, call).__doc__)
        """

        #Initialize parent classes.
        super(cluster_qcodes, self).__init__(transport_inst, debug)
        Instrument.__init__(self, name)

        #Set instrument parameters
        self._slots = 20

        #Add QCoDeS parameters
        for slot_idx in range(1, self._slots + 1):
            self.add_parameter(
                "module{}_present".format(slot_idx),
                label       = "Module present status for slot {} in the Cluster.".format(slot_idx),
                docstring   = "Sets/gets module present status for slot {} in the Cluster.",
                unit        = '',
                vals        = vals.Bool(),
                val_mapping = {"present": True, "empty": False},
                get_parser  = bool,
                get_cmd     = partial(self._get_modules_present, slot_idx)
            )

        self.add_parameter(
            "reference_source",
            label       = "Reference source.",
            docstring   = "Sets/gets reference source ('internal' = internal 10 MHz, 'external' = external 10 MHz).",
            unit        = '',
            vals        = vals.Bool(),
            val_mapping = {"internal": True, "external": False},
            set_parser  = bool,
            get_parser  = bool,
            set_cmd     = self._set_reference_source,
            get_cmd     = self._get_reference_source
        )

    #--------------------------------------------------------------------------
    def __repr__(self) -> str:
        """
        Returns simplified representation of class giving just the class, name and connection.

        Parameters
        ----------

        Returns
        ----------
        str
            String representation of class.

        Raises
        ----------
        """

        loc_str = ""
        if hasattr(self._transport, '_socket'):
            address, port = self._transport._socket.getpeername()
            loc_str = f" at {address}:{port}"
        return f"<{type(self).__name__}: {self.name}" + loc_str + ">"

    #--------------------------------------------------------------------------
    def _invalidate_qcodes_parameter_cache(self):
        """
        Marks the cache of all qcodes parameters on this instrument as invalid.
        """
        instrument_parameters = self.parameters.values()
        for parameter in instrument_parameters:
            parameter.cache.invalidate()

    #--------------------------------------------------------------------------
    def reset(self):
        """
        Resets device, invalidates QCoDeS parameter cache and clears all status and event registers (see `SCPI <https://www.ivifoundation.org/docs/scpi-99.pdf>`_).

        Parameters
        ----------

        Returns
        ----------

        Raises
        ----------
        Exception
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        self._invalidate_qcodes_parameter_cache()
        super().reset()

#-- class ---------------------------------------------------------------------

class cluster(cluster_qcodes):
    """
    Cluster driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses an IP socket to communicate
    with the instrument.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, host, port=5025, debug=0):
        """
        Creates Cluster driver object.

        Parameters
        ----------
        name : str
            Instrument name.
        host : str
            Instrument IP address.
        port : int
            Instrument port.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.
        """

        #Create transport layer (socket interface)
        transport_inst = ip_transport(host=host, port=port)

        #Initialize parent classes.
        super(cluster, self).__init__(name, transport_inst, debug)

#-- class ---------------------------------------------------------------------

class cluster_dummy(cluster_qcodes):
    """
    Cluster driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses the :class:`~ieee488_2.transport.cluster_dummy_transport` layer
    to substitute an actual Cluster to allow software stack development without hardware.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, debug=1):
        """
        Creates Cluster driver object. The debug level must be set to >= 1.

        Parameters
        ----------
        name : str
            Instrument name.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        """

        #Create transport layer (socket interface)
        transport_inst = cluster_dummy_transport()

        #Initialize parent classes.
        super(cluster_dummy, self).__init__(name, transport_inst, debug)

#-- class ---------------------------------------------------------------------

class cluster_qcm(pulsar_qcm):
    """
    Cluster QCM driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses an IP socket to communicate
    with the instrument.

    .. warning::

	    This is a temporary class created for development purposes that will be removed in the future.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, host, port=5025, debug=1):
        """
        Creates Cluster QCM driver object.

        Parameters
        ----------
        name : str
            Instrument name.
        host : str
            Instrument IP address.
        port : int
            Instrument port.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.
        """

        #Initialize parent classes.
        super(cluster_qcm, self).__init__(name, host, port, debug)

#-- class ---------------------------------------------------------------------

class cluster_qcm_dummy(pulsar_qcm_dummy):
    """
    Cluster QCM driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses the :class:`~ieee488_2.transport.pulsar_dummy_transport` layer
    to substitute an actual Cluster QCM to allow software stack development without hardware.

    .. warning::

	    This is a temporary class created for development purposes that will be removed in the future.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, debug=1, is_rf_type=False):
        """
        Creates Cluster QCM driver object. The debug level must be set to >= 1.

        Parameters
        ----------
        name : str
            Instrument name.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).
        is_rf_type : bool
            Dummy module type (False = RF, True = baseband)

        Returns
        ----------

        Raises
        ----------
        """

        #Initialize parent classes.
        super(cluster_qcm_dummy, self).__init__(name, debug, is_rf_type)

#-- class ---------------------------------------------------------------------

class cluster_qrm(pulsar_qrm):
    """
    Cluster QRM driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses an IP socket to communicate
    with the instrument.

    .. warning::

	    This is a temporary class created for development purposes that will be removed in the future.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, host, port=5025, debug=1):
        """
        Creates Cluster QRM driver object.

        Parameters
        ----------
        name : str
            Instrument name.
        host : str
            Instrument IP address.
        port : int
            Instrument port.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).

        Returns
        ----------

        Raises
        ----------
        Exception
            Debug level is 0 and there is a version mismatch.
        """

        #Initialize parent classes.
        super(cluster_qrm, self).__init__(name, host, port, debug)

#-- class ---------------------------------------------------------------------

class cluster_qrm_dummy(pulsar_qrm_dummy):
    """
    Cluster QRM driver class based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_ that uses the :class:`~ieee488_2.transport.pulsar_dummy_transport` layer
    to substitute an actual Cluster QRM to allow software stack development without hardware.

    .. warning::

	    This is a temporary class created for development purposes that will be removed in the future.
    """

    #--------------------------------------------------------------------------
    def __init__(self, name, debug=1, is_rf_type=False):
        """
        Creates Cluster QRM driver object. The debug level must be set to >= 1.

        Parameters
        ----------
        name : str
            Instrument name.
        debug : int
            Debug level (0 = normal, 1 = no version check, >1 = no version or error checking).
        is_rf_type : bool
            Dummy module type (False = RF, True = baseband)

        Returns
        ----------

        Raises
        ----------
        """

        #Initialize parent classes.
        super(cluster_qrm_dummy, self).__init__(name, debug, is_rf_type)