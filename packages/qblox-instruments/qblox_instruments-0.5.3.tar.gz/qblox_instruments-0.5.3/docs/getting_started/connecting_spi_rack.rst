.. _connecting_spi:

Connecting an SPI Rack
======================

In this section we will explain how to setup a `Qblox SPI Rack <https://www.qblox.com/spi>`_ and connect it to your PC. Please
make sure that you have the Qblox instruments package installed before proceeding (see section
:ref:`getting_started/installation:Installation`) and that your PC has an available USB port.

Connecting to power
-------------------

.. figure:: /figures/spi_power_connection_overview.svg
        :width: 400px
        :align: center
        :alt: An SPI Rack connected to a battery and via a gyrator to mains.

The recommended way to connect the SPI Rack to power is by connecting it via a gyrator to mains in parallel to a battery.
This will ensure the system remains powered and stable, the gyrator prevents interference signals such as 50 Hz from
getting to the SPI Rack by mimicking a large (~40H) inductor.


.. figure:: /figures/gyrator_and_batt_connect_schematic.svg
        :width: 700px
        :align: center
        :alt: An SPI Rack connected to a battery and via a gyrator to mains.

.. note::

    Please ensure there is a minimum of 1 meter between the gyrator and its power supply in order to effectively prevent
    interference signals from getting to the SPI Rack. Also ensure that the SPI Rack is not mounted in the same 19 inch
    rack with line-powered equipment, this includes the gyrator power supply.

Connecting to PC
----------------

First, make sure a C1b controller module is fully inserted in the left-most slot of the SPI Rack. Then, connect the
C1b to a C2 SPI Isolator box via a display port cable. Now, connect the C2 SPI Isolator box via USB to your PC. Finally,
make sure to power switch on the back of the SPI Rack is in the `on` position, and the power supply is switched on as well.
The LED on the C1b module should now turn on.

.. figure:: /figures/c1b_to_pc_connection.svg
        :width: 600px
        :align: center
        :alt: An SPI Rack connected to a battery and via a gyrator to mains.

We can now connect to the SPI Rack via the QCoDeS driver provided through the `qblox-instruments` package (see section
:ref:`getting_started/installation:Installation`).

Communicating with the SPI Rack
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Starting the communication with the SPI Rack is done by simply instantiating an instance of the driver:

.. code-block:: python

    from spi_rack.spi_rack import spi_rack
    spi = spi_rack('SPI Rack', 'COM4')

SPI Modules
^^^^^^^^^^^

To use an SPI Rack module, simply slide the module into one of the slots of the rack and fasten the screws. You should
feel them "click" into place. The address on which to connect to the module is written on a sticker
on the side of the module itself. Each of the modules we intend to use, we should add to the driver. This is done simply
by:

.. code-block:: python

    spi.add_spi_module(2, "S4g") # example for an S4g on address 2

For more information on how to use the driver please visit the tutorial section.
