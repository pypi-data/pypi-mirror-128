.. _general:

General
=======

In this section we explain general concepts of the Qblox instruments, like general instrument control and status.


Control
-------

All Qblox instruments, excluding the `SPI Rack <https://www.qblox.com/spi>`_, are controlled over Ethernet using a Python driver based on `QCoDeS <https://qcodes.github.io/Qcodes/>`_.
We recommend using this driver as it provides easy and clear access to all functionality of the instrument; even if you use a different lab-framework as the overhead of QCoDeS is minimal.

Underneath the QCoDeS driver layer, the control software is built upon the `SCPI <https://www.ivifoundation.org/docs/scpi-99.pdf>`_ standard, as also reflected by the :ref:`api_reference`.
This means that all communication with the instrument happens using the master/slave paradigm, where the host PC is the master and **always** responsible for initiating communication by
issuing SCPI commands to the instrument. Of course, all of this is abstracted away at the driver level, so you don't have to have in-depth knowledge of the standard. However, if you are familiar
with it, you will have access to all the default SCPI functionality that you are used to, like :meth:`!get_idn` (`*IDN?`), :meth:`!reset` (`*RST`) and
:meth:`!clear` (`*CLS`), albeit with a slightly more readable name.


Reset
^^^^^

We advise resetting the instrument before executing any experiment to get the instrument into a well-defined state, thereby improving reproducibility of the experiment. Resetting the
instrument is easily achieved by calling :meth:`!reset`. This will reset the instrument status and configuration to the default values. It will reset all SCPI registers, including
any reported error. It will also clear all stored Q1ASM programs, waveforms and acquisitions.

There are many use cases where you want to store the instrument's settings before resetting, for instance to be able to easily reproduce an experiment. For this, we advise to use the
`snapshot <https://qcodes.github.io/Qcodes/examples/DataSet/Working%20with%20snapshots.html>`_ feature of QCoDeS.


Errors
^^^^^^

Instrument errors are reported using SCPI's system error registers, which can be read using :meth:`!get_num_system_error` (`SYSTem:ERRor:COUNt?`) and
:meth:`!get_system_error` (`SYSTem:ERRor:NEXT?`). However, like mentioned before, this is all abstracted away at the driver level. This means that the errors are automatically read
and reported to you using exceptions. Any driver function can throw these exceptions and you need to make sure these are handled appropriately, for instance by using
`try statements <https://docs.python.org/3/tutorial/errors.html>`_.


Clocking
--------

The instruments need a 10 MHz reference clock to operate. It is used to derive clocks for the instrument's internal logic and data converters. Each instrument can either generate this 10 MHz
reference clock internally or it can be generated externally and provided through the REF\ :sup:`in` SMA connector (10 MHz, 1 Vpp nominal @ 50 Ω) [see section :ref:`getting_started/overview:Overview`].
Using the external reference source can be useful for synchronizing the instrument with other instruments in you setup, Qblox's or others. The
:meth:`!reference_source` parameter can be used to select which reference clock is used to clock the instrument. We recommend to set the reference right after resetting the instrument with :meth:`!reset`.
Whichever reference clock is selected, the reference clock is also output using the REF\ :sup:`out` SMA connector (10 MHz, 0-3.3 V @ 50 Ω). This output can be used as reference clock for other instruments.
Be aware that the input and output reference clocks are purposely not phase aligned to aid synchronization of Qblox instruments (see section :ref:`documentation/synchronization:Synchronization`).


Status
------

The status of the instrument conveys the general operational condition of the instrument.
This is derived from multiple internal components, like PLLs and temperature sensors.
The instrument's status is updated every millisecond and stored in the standard SCPI registers.
It can be queried through these registers [e.g. through
:meth:`!get_status_byte` (`*STB?`)],
but a more convenient way of reading out the general instrument status is calling
:meth:`!get_system_status`.
This returns the following status and accompanying flags that elaborate on the status:

- **Status**:

    - **Okay**: Instrument is operational.
    - **Critical**: Instrument has encountered an error (see flags below), but it has been corrected.
    - **Error**: Instrument has encountered an error (see flags below), which needs to be fixed urgently.

- **Flags**:

    - **Carrier board PLL unlocked**: No reference clock found.
    - **FPGA PLL unlocked**: No reference clock found.
    - **FPGA temperature out-of-range**: FPGA temperature has surpassed 80°C.
    - **Carrier board temperature out-of-range**: Carrier board temperature has surpassed 100°C.
    - **Analog frontend temperature out-of-range**: Analog frontend board temperature has surpassed 100°C.

The instrument status is persistent through the state `critical`, so a way to reset it is required. This can be simply done by calling the :meth:`!clear` to clear the state or by
completely resetting the instrument by calling :meth:`!reset`.


Frontpanel LEDs
^^^^^^^^^^^^^^^

The LEDs on the frontpanel of the Qblox instruments are used as a visual indication of the status of the instrument. The LED colors indicate the following status:

+---------+------------+--------------------------------------------+
| **S**   | **Green**  | Okay.                                      |
|         +------------+--------------------------------------------+
|         | **Orange** | Critical.                                  |
|         +------------+--------------------------------------------+
|         | **Red**    | Error.                                     |
+---------+------------+--------------------------------------------+
| **R**   | **Green**  | External reference clock selected.         |
|         +------------+--------------------------------------------+
|         | **Blue**   | Internal reference clock selected          |
|         +------------+--------------------------------------------+
|         | **Red**    | No reference clock found.                  |
+---------+------------+--------------------------------------------+
| **I/O** | **Green**  | Channel idle.                              |
|         +------------+--------------------------------------------+
|         | **Purple** | Sequencer connected to channel is armed.   |
|         +------------+--------------------------------------------+
|         | **Blue**   | Sequencer connected to channel is running. |
|         +------------+--------------------------------------------+
|         | **Red**    | Sequencer connected to channel failed.     |
|         +------------+--------------------------------------------+
|         | **Orange** | Output values are clipping.                |
+---------+------------+--------------------------------------------+
