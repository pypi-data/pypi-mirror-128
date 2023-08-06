.. _connecting:

Connecting a Pulsar
===================

In this section we will explain how to connect a `Qblox Pulsar QCM or QRM module <https://www.qblox.com/pulsar>`_ to your host PC.
Please make sure that you have the Qblox instruments package installed before proceeding (see section :ref:`getting_started/installation:Installation`) and that your host PC has an
Ethernet port.


Connecting to a single module
-----------------------------

As an example, we will consider a setup composed of:

    - A laptop (host PC) with a USB Ethernet adapter.
    - A Pulsar QCM.

The following steps will allow you to successfully connect the module to your local network:

1. Connect the module to your host PC using an Ethernet cable.
#. Power up the module. The module is ready when all LEDs turn on (See section :ref:`documentation/general:Frontpanel LEDs`).
#. Configure the network adapter of the host PC, so that its IP address is within subnet ``192.168.0.X`` (where ``X`` is in a range from 3 to 254).
   Make sure the subnet mask is set to ``255.255.255.0``.

    .. note::
        Configuration of a network adapter varies slightly between operating systems. See section :ref:`getting_started/network_adapter_cfg:Network adapter configuration` for a Windows,
        Linux and MacOS description.

    At this point your setup will look similar to the example setup in the figure below:

    .. figure:: /figures/setup_single_module.jpg
        :width: 500px
        :align: center
        :alt: A Pulsar QCM module connected to a laptop using a USB Ethernet adapter.

    After a few seconds, the module should be present on the local network. You can verify this by executing the following command in a terminal of your choice.

    .. note::
        The default IP address of the module is ``192.168.0.2``. Replace the IP address of any following instruction accordingly if the IP address of the module was ever changed. 
        See section :ref:`getting_started/finding_ip_addr:Finding the IP address of a module` in case you do not know the IP address.

    .. code-block:: console

        $ ping 192.168.0.2 # Press Ctrl + C to terminate the program

    If successful, the output should be similar to the following example output:

    .. code-block:: console

        PING 192.168.0.2 (192.168.0.2): 56 data bytes
        64 bytes from 192.168.0.2: icmp_seq=0 ttl=64 time=0.396 ms
        64 bytes from 192.168.0.2: icmp_seq=1 ttl=64 time=0.232 ms
        64 bytes from 192.168.0.2: icmp_seq=2 ttl=64 time=0.261 ms

#. Finally, connect to the module from your host PC by running the following snippet using a `Python 3.8 <https://www.python.org/downloads/release/python-380/>`_ environment like an interactive shell 
   or a Jupyter Notebook:

    .. code-block:: python

        # Import driver
        from pulsar_qcm.pulsar_qcm import pulsar_qcm

        # Connect to module
        qcm = pulsar_qcm("qcm", "192.168.0.2")

    .. tip::
        Close the connection to the module using ``qcm.close()``.

    .. toctree::
        :hidden:

        network_adapter_cfg.rst
        finding_ip_addr.rst


Connecting to multiple modules
------------------------------

To be able to control multiple modules (e.g. a `Pulsar QCM and QRM <https://www.qblox.com/pulsar>`_) we need to follow the steps described in :ref:`getting_started/connecting_pulsar:Connecting to a single module`
except, now:

- Instead of connecting a module directly to the Ethernet adapter of the host PC, we will connect all the modules and the host PC to the same network using, for example, an Ethernet switch.
- The IP address of the modules **must** be changed to avoid IP collisions. See section :ref:`getting_started/updating:Updating` for further instructions on updating the IP address of the modules.

As an example, we will consider a setup composed of:

    - A laptop (host PC) with a USB Ethernet adapter.
    - A Pulsar QCM.
    - A Pulsar QRM.
    - A network switch.

The following figure shows the example setup:

.. figure:: /figures/setup_multiple_modules.jpg
    :width: 500px
    :align: center
    :alt: A Pulsar QCM and QRM module connected to a laptop over an Ethernet switch.

The following python code lets us connect to the modules in the example setup:

.. code-block:: python

    # Import drivers
    from pulsar_qcm.pulsar_qcm import pulsar_qcm
    from pulsar_qrm.pulsar_qrm import pulsar_qrm

    # Connect to modules
    qcm = pulsar_qcm("qcm", "192.168.0.2")  # This module uses the default IP address.
    qrm = pulsar_qrm("qrm", "192.168.0.3")  # This module's IP address was changed.

.. note::
    When using multiple modules in your setup, you might need to synchronize the in- and outputs of the various modules. See section :ref:`documentation/synchronization:Synchronization` 
    the learn how to do this.
