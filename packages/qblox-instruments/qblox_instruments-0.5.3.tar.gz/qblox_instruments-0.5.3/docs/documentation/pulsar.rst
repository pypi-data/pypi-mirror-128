.. _pulsar:

Pulsar
======

In this section we will discuss the architecture of the Pulsar instruments and their rich feature set.


QCM Overview
------------

The Qubit Control Module is an instrument completely dedicated to qubit control using parametrized pulses. The pulses are stored as waveform envelopes in
memory and can be parametrized by changing gain and offset and additionally phase if also modulated. This parametrization is controlled by the AWG paths of the sequencer,
which each have two waveform paths (from here on referred to as path 0 and 1). Using parametrization, the output of these paths can either be independent
signals or modulated IQ signals. The two paths of each sequencer can, in turn, be connected to any output pair of the instrument (i.e. O\ :sup:`1/2` and O\ :sup:`3/4`)
to control one or more qubits per output. Additionally, the sequencers also control four marker output channels.

The figure below shows the architecture of the Pulsar QCM. Please see the :ref:`documentation/pulsar:Features` section for more information on the numbered
features in the figure.

.. figure:: /figures/pulsar_qcm_architecture.svg
    :width: 800px
    :align: center
    :alt: Pulsar QCM architecture.

.. note::

    This figure is outdated and will be updated soon.


QRM Overview
------------

The Qubit Readout Module is an instrument that targets qubit readout. To accomplish this, it employs a similar architecture to the QCM: besides two outputs (O\ :sup:`1/2`), the module has an acquisition path that operates on two inputs (i.e. I\ :sup:`1/2`) using two processing paths (from here on also referred to as path 0 and 1). Using
parametrization, each sequencer can target one qubit for readout, allowing multiplexed readout of qubits on the same channel. The AWG paths can generate the
readout pulses and the acquisition paths can process the returned readout data. The acquisition path supports three acquisition modes:

    - `Scope`: Returns the raw input data.
    - `Integration`: Returns the result after integrating the input data; optionally based on an integration function stored in memory.
    - `Thresholded`: Returns the binary qubit value after thresholding the integrated value.

The results of the acquisitions are returned to the user.

The figure below shows the architecture of the Pulsar QRM. Please see the :ref:`documentation/pulsar:Features` section for more information on the numbered features in the figure.

.. figure:: /figures/pulsar_qrm_architecture.svg
    :width: 800px
    :align: center
    :alt: Pulsar QCM architecture.

.. note::

    This figure is outdated and will be updated soon.

Features
--------

1. SYNQ & trigger
^^^^^^^^^^^^^^^^^

The Qblox SYNQ technology and trigger input enable simple and quick synchronization over multiple instruments. See section :ref:`documentation/synchronization:Synchronization`
for more information.


2. Sequencer
^^^^^^^^^^^^

The sequencers are the heart(s) of the Pulsar instruments. They orchestrate the experiment using a custom low-latency sequence processor specifically designed
for quantum experiments. Furthermore, they each achieve that by controlling a dedicated AWG path and, in case of a Pulsar QRM, acquisition path, which enables
parametrized pulse generation and readout. Each instrument has a 6 of these sequencers to target multiple qubits with one instrument. See section
:ref:`documentation/sequencer:Sequencer` for more information on how to program and control them.


3. Gain
^^^^^^^

Each sequencer has a dedicated gain step for both path 0 and 1, which can be statically configured using the :meth:`!sequencer#_gain_awg_path#` parameters.
However, the gain can also be dynamically controlled using the `set_awg_gain` instruction of the sequence processor which enables pulse parametrization
(see section :ref:`documentation/sequencer:Instructions`). The static and dynamic gain controls are complementary.

.. note::

    If modulated IQ signals are used for an output pair, the gain :meth:`!sequencer#_gain_awg_path#` has to be the same for both paths.


4. Offset
^^^^^^^^^

Each sequencer has a dedicated offset step for both path 0 and 1, which can be statically configured using the :meth:`!sequencer#_offs_awg_path#` parameters.
However, the offset can also be dynamically controlled using the `set_awg_offs` instruction of the sequence processor which enables pulse parametrization.
(see section :ref:`documentation/sequencer:Instructions`). The static and dynamic offset controls are complementary.

.. note::

    This offset is applied to the signals before the mixer and cannot be used for DC offset correction if the mixer is enabled.


5. NCO & IQ mixer
^^^^^^^^^^^^^^^^^

Each sequencer has a dedicated numerically controlled oscillator and IQ mixer. The NCO can be used to track the qubit phase (at a fixed frequency) and the IQ mixer can be used to modulate the output.

The frequency of the NCO and phase can be statically controlled using the :meth:`!sequencer#_nco_freq` and :meth:`!sequencer#_nco_phase_offs`
parameters. However, the phase of the NCO can also be dynamically controlled using the `reset_ph`, `set_ph` and `set_ph_delta` instructions of the sequence processor, which enables
pulse parametrization and execution of virtual Z-gates (see section :ref:`documentation/sequencer:Instructions`). The static and dynamic phase control
is complementary. The modulation is enabled using the :meth:`!sequencer#_nco_mod_en parameter`.


6. Sequencer multiplexer
^^^^^^^^^^^^^^^^^^^^^^^^

A multiplexer that allows any sequencer to be connected to any output pair. Multiple sequencers can also be connected to a single output pair. This, in combination
with the dedicated NCO and IQ mixer per sequencer, enables easy and flexible targeting of multiple qubits on a single channel. The multiplexer can be statically configured
through the :meth:`!sequencer#_channel_map_path#_out#_en` parameters.

.. note::

    The output of each sequencer is complementary. Be aware of potential output clipping when connecting multiple sequencers to a single output.


7. Mixer correction
^^^^^^^^^^^^^^^^^^^

The mixer correction is used to correct imperfections in an external mixer used for up or down conversion. Every sequencer can apply mixer corrections to the
phase and gain between path 0 and 1 to correct for frequency dependant phase and/or gain imbalance in the external mixer. On top of that, a DC offset can
be applied to each output to correct for frequency independant offset imperfections in the external mixer. The mixer correction is statically configured using
the :meth:`!sequencer#_mixer_corr_phase_offset_degree`, :meth:`!sequencer#_mixer_corr_gain_ratio` and :meth:`!out#_offset` parameters.


8. High-speed data converters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Pulsar instruments use state-of-art 1Gbps 16-bit DACs and 1Gbps 12-bit ADCs. The dynamic output range of the Pulsar QRM and QCM's DACs are 5 Vpp and 1 Vpp respectively and 50 Ω terminated.
The maximum input range of the Pulsar QRM's ADCs is 2 Vpp and 50 Ω terminated.


9. Marker output channels
^^^^^^^^^^^^^^^^^^^^^^^^^

Each sequencer has control over the four marker output channels, with the control of each sequencer being OR'ed to create the final marker outputs. The markers can
be dynamically controlled with the `set_mrk` instruction of the sequence processor (see section :ref:`documentation/sequencer:Instructions`), but can
also be overwritten with the static marker overwrite parameters :meth:`!sequencer#_marker_ovr_en` and :meth:`!sequencer#_marker_ovr_value`.
The marker output range is 0-3.3 V TTL.


10. Input gain
^^^^^^^^^^^^^^

Dedicated amplifiers to provide additional gain to the input signals. The gain can vary between -6dB and 26dB and can be set using the :meth:`!in#_amp_gain`
parameters.
