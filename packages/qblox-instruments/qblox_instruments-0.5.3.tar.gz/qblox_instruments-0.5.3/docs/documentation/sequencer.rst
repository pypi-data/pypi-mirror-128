.. _sequencer:

Sequencer
==========

This section will explain how the sequencers of the Pulsar QCM and QRM are controlled. Every sequencer is controlled
using the same functions and parameters, which either take the sequencer index as a parameter or indicate which
sequencer they operate on based on the index in their name.

.. note::
    As of version 0.5.0 of the Pulsar QRM, new functionality has been added to the acquisition path (e.g. real-time demodulation, (weighed) integration, discretization, averaging, binning).
    More details about this functionality will be added to the documentation as soon as possible. For now, please have a look at the binned acquisition tutorial to get started.

Overview
--------

The sequencers are split into the sequence processor, AWG and acquisition paths as shown in the figures below. Each sequence processor controls one
AWG path and, in case of the Pulsar QRM, one acquisition path. The AWG path and acquisition path are discussed in more detail in section :ref:`documentation/pulsar:Pulsar`.
Each sequencer processor is, in turn, split into a classical and real-time pipeline. The classical pipeline is responsible for any classical instructions
related to program flow or arithmetic and the real-time pipeline is responsible for real-time instructions that are used to create the experiment timeline.

.. figure:: /figures/pulsar_qcm_sequencer.svg
    :width: 500px
    :align: center
    :alt: Pulsar QCM sequencer with AWG path.

    Pulsar QCM sequencer with AWG path.

.. figure:: /figures/pulsar_qrm_sequencer.svg
    :width: 500px
    :align: center
    :alt: Pulsar QRM sequencer.

    Pulsar QRM sequencer with AWG and acquisition paths.

The sequencers are started and stopped by calling the :meth:`!arm_sequencer`, :meth:`!start_sequencer` and
:meth:`!stop_sequencer` functions. Once started they will execute the sequence described in the next section.


Sequence
--------

The sequencers are programmed with a sequence using the :meth:`!sequencer#_waveforms_and_program` function parameter. This parameter expects
a sequence in the form of a JSON compatible file that contains the waveform, weight, acquistion and program information. The JSON file is
expected to adhere to the following format:

- **waveforms**: Indicates that the following waveforms are intended for the AWG path.

    - **waveform name**: Replace by string containing the waveform name.

        - **data**: List of floating point values to express the waveform.
        - **index**: Integer index used by the Q1ASM program to refer to the waveform.

- **weights**: Indicates that the following weight functions are intended for the integration units of the acquisition path (only used by the Pulsar QRM).

    - **weight name**: Replace by string containing the weight name.

        - **data**: List of floating point values to express the weight.
        - **index**: Integer index used by the Q1ASM program to refer to the weight.

- **acquisitions**: Indicates that the following acquisitions are available for the acquisition path to refer to (only used by the Pulsar QRM).

    - **acquisition name**: Replace by string containing the acquisition name.

        - **num_bins**: Number of bins in acquisition.
        - **index**: Integer index used by the Q1ASM program to refer to the acquisition.

- **program**: Single string containing the entire sequence processor Q1ASM program.


.. admonition:: Example of a sequence JSON file.
    :class: dropdown

        .. code-block:: json

            {
                "waveforms": {
                    "gaussian": {
                        "data": [
                            0.0075756774442599355, 0.5812730178734145, 0.5812730178734145, 0.0075756774442599355
                        ],
                        "index": 0
                    },
                    "sine": {
                        "data": [0.0, 1.0, 1.2246467991473532e-16, -1.0],
                        "index": 1
                    }
                },
                "weights": {
                    "gaussian": {
                        "data": [0.0075756774442599355, 0.5812730178734145, 0.5812730178734145, 0.0075756774442599355],
                        "index": 0
                    },
                    "sine": {
                        "data": [0.0, 1.0, 1.2246467991473532e-16, -1.0],
                        "index": 1
                    }
                },
                "acquisitions": {
                    "binned": {
                        "num_bins": 100000,
                        "index": 0
                    },
                    "averaged": {
                        "num_bins": 1,
                        "index": 1
                    }
                },
                "program": "\nplay 0,1,4 #Play waveforms and wait 4ns.\nacquire 1,0,16380 #Acquire wait for scope mode acquisition to finish.\nstop #Stop.\n"
            }



Program
^^^^^^^

The sequence programs are written in the custom Q1ASM assembly language described in the following sections. All sequence processor instructions are executed by
the classical pipeline and the real-time instructions are also executed by the real-time pipeline. These latter instructions are intended to control the AWG and
acquisition paths in a real-time fashion. Once processed by the classical pipeline they are queued in the real-time pipeline awaiting further execution. A total
of 32 instructions can be queued and once the queue is full, the classical part will stall on any further real-time instructions.

Once execution of the real-time instructions by the real-time pipeline is started, care must be taken to not cause an underrun of the queue. An underrun will
potentially cause undetermined real-time behaviour and desynchronize any synchronized sequencers. Therefore, when this is detected, the sequencer is completely
stopped. A likely cause of underruns is a loop with a very short (i.e. < 24ns) real-time run-time, since the jump of a loop takes some cycles to be execute by the
classical pipeline.

Finally, be aware that moving data into a register using an instruction takes a cycle to complete. This means that when an instruction reads from a register that
the previous instruction has written to, a `nop` instruction must to be placed in between these consecutively instructions for the value to be correctly read.

The state of the sequencers, including any errors, can be queried through :meth:`!get_sequencer_state`.


Instructions
""""""""""""
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| Instructions      | Argument 0   | Argument 1   | Argument 2   | Argument 3   | Argument 4   |   Description                  |
+===================+==============+==============+==============+==============+==============+================================+
| **Control**                                                                                                                   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `illegal`         | --           | --           | --           | --           | --           | | Instruction that should not  |
|                   |              |              |              |              |              | | be executed. If it is        |
|                   |              |              |              |              |              | | executed, the sequencer      |
|                   |              |              |              |              |              | | will stop with the illegal   |
|                   |              |              |              |              |              | | instruction flag set.        |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `stop`            | --           | --           | --           | --           | --           | | Instruction that stops the   |
|                   |              |              |              |              |              | | sequencer.                   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `nop`             | --           | --           | --           | --           | --           | | No operation instruction,    |
|                   |              |              |              |              |              | | that does nothing. It is     |
|                   |              |              |              |              |              | | used to pass a single cycle  |
|                   |              |              |              |              |              | | in the classic part of the   |
|                   |              |              |              |              |              | | sequencer without any        |
|                   |              |              |              |              |              | | operations.                  |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| **Jumps**                                                                                                                     |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `jmp`             | | Immediate, | --           | --           | --           | --           | | Jump to the next             |
|                   | | Register,  |              |              |              |              | | instruction indicated by     |
|                   | | Label      |              |              |              |              | | `argument 0`.                |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `jge`             | Register     | Immediate    | | Immediate, | --           | --           | | If `argument 0` is greater   |
|                   |              |              | | Register,  |              |              | | or equal to `argument 1`,    |
|                   |              |              | | Label      |              |              | | jump to the instruction      |
|                   |              |              |              |              |              | | indicated by `argument 2`.   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `jlt`             | Register     | Immediate    | | Immediate, | --           | --           | | If `argument 0` is less      |
|                   |              |              | | Register,  |              |              | | than `argument 1`, jump to   |
|                   |              |              | | Label      |              |              | | the instruction indicated    |
|                   |              |              |              |              |              | | by `argument 2`.             |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `loop`            | Register     | | Immediate, | --           | --           | --           | | Subtract `argument 0` by     |
|                   |              | | Register,  |              |              |              | | one and jump to the          |
|                   |              | | Label      |              |              |              | | instruction indicated by     |
|                   |              |              |              |              |              | | `argument 1` until           |
|                   |              |              |              |              |              | | `argument 0` reaches zero.   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| **Arithmetic**                                                                                                                |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `move`            | | Immediate, | Register     | --           | --           | --           | | `Argument 0` is moved /      |
|                   | | Register   |              |              |              |              | | copied to `argument 1`.      |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `not`             | | Immediate, | Register     | --           | --           | --           | | Bit-wise invert              |
|                   | | Register   |              |              |              |              | | `argument 0`                 |
|                   |              |              |              |              |              | | and move the result to       |
|                   |              |              |              |              |              | | `argument 1`.                |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `add`             | Register     | | Immediate, | Register     | --           | --           | | Add `argument 1` to          |
|                   |              | | Register   |              |              |              | | `argument 0` and move the    |
|                   |              |              |              |              |              | | result to `argument 2`.      |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `sub`             | Register     | | Immediate, | Register     | --           | --           | | Subtract `argument 1` from   |
|                   |              | | Register   |              |              |              | | `argument 0` and move the    |
|                   |              |              |              |              |              | | result to `argument 2`.      |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `and`             | Register     | | Immediate, | Register     | --           | --           | | Bit-wise AND `argument 0`    |
|                   |              | | Register   |              |              |              | | and `argument 1` and move    |
|                   |              |              |              |              |              | | the result to `argument 2`.  |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `or`              | Register     | | Immediate, | Register     | --           | --           | | Bit-wise OR `argument 0`     |
|                   |              | | Register   |              |              |              | | and `argument 1` and move    |
|                   |              |              |              |              |              | | the result to `argument 2`.  |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `xor`             | Register     | | Immediate, | Register     | --           | --           | | Bit-wise XOR `argument 0`    |
|                   |              | | Register   |              |              |              | | and `argument 1` and move    |
|                   |              |              |              |              |              | | the result to `argument 2`.  |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `asl`             | Register     | | Immediate, | Register     | --           | --           | | Bit-wise left-shift          |
|                   |              | | Register   |              |              |              | | `argument 0` by `argument 1` |
|                   |              |              |              |              |              | | number of  bits and move     |
|                   |              |              |              |              |              | | the result to `argument 2`.  |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `asr`             | Register     | | Immediate, | Register     | --           | --           | | Bit-wise right-shift         |
|                   |              | | Register   |              |              |              | | `argument 0` by `argument 1` |
|                   |              |              |              |              |              | | number of bits and move the  |
|                   |              |              |              |              |              | | result to `argument 2`.      |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| **Software request**                                                                                                          |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `sw_req`          | | Immediate, | --           | --           | --           | --           | | Generate software request    |
|                   | | Register   |              |              |              |              | | interrupt with `argument 0`  |
|                   |              |              |              |              |              | | value being passed as        |
|                   |              |              |              |              |              | | interrupt argument           |
|                   |              |              |              |              |              | | (currently not implemented). |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| **Real-time pipeline instructions**                                                                                           |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `set_mrk`         | | Immediate, | --           | --           | --           | --           | | Set marker output channels   |
|                   | | Register   |              |              |              |              | | to `argument 0` (bits 0-3),  |
|                   |              |              |              |              |              | | where the bit index          |
|                   |              |              |              |              |              | | corresponds to the channel   |
|                   |              |              |              |              |              | | index. The set value is      |
|                   |              |              |              |              |              | | OR´ed by that of other       |
|                   |              |              |              |              |              | | sequencers. The parameters   |
|                   |              |              |              |              |              | | are cached and only updated  |
|                   |              |              |              |              |              | | when the `upd_param`,        |
|                   |              |              |              |              |              | | `play`, `acquire` or         |
|                   |              |              |              |              |              | | `acquired_weighed`           |
|                   |              |              |              |              |              | | instructions are executed.   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `reset_ph`        | --           | --           | --           | --           | --           | | Reset the absolute phase of  |
|                   |              |              |              |              |              | | the NCO used by the AWG and  |
|                   |              |              |              |              |              | | acquisition to 0°. This also |
|                   |              |              |              |              |              | | resets any relative phase    |
|                   |              |              |              |              |              | | offsets that were already    |
|                   |              |              |              |              |              | | statically or dynamically    |
|                   |              |              |              |              |              | | set. The reset is cached and |
|                   |              |              |              |              |              | | only applied when the        |
|                   |              |              |              |              |              | | `upd_param`, `play`,         |
|                   |              |              |              |              |              | | `acquire` or                 |
|                   |              |              |              |              |              | | `acquired_weighed`           |
|                   |              |              |              |              |              | | instructions are executed.   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `set_ph`          | | Immediate, | | Immediate, | | Immediate, | --           | --           | | Set the relative phase of    |
|                   | | Register   | | Register   | | Register   |              |              | | the NCO used by the AWG and  |
|                   |              |              |              |              |              | | acquisition. The phase       |
|                   |              |              |              |              |              | | is divided into a coarse     |
|                   |              |              |              |              |              | | (`argument 0`), fine         |
|                   |              |              |              |              |              | | (`argument 1`) and           |
|                   |              |              |              |              |              | | ultra-fine (`argument 2`)    |
|                   |              |              |              |              |              | | segment. The coarse segment  |
|                   |              |              |              |              |              | | is divided into 400 steps    |
|                   |              |              |              |              |              | | of 0.9°. The fine segment    |
|                   |              |              |              |              |              | | is divided into 400 steps    |
|                   |              |              |              |              |              | | of 2.25e-3°. And the         |
|                   |              |              |              |              |              | | ultra-fine segment is        |
|                   |              |              |              |              |              | | divided into 6250 steps of   |
|                   |              |              |              |              |              | | 3.6e-7°. The parameters are  |
|                   |              |              |              |              |              | | cached and only updated      |
|                   |              |              |              |              |              | | when the `upd_param`,        |
|                   |              |              |              |              |              | | `play`, `acquire` or         |
|                   |              |              |              |              |              | | `acquired_weighed`           |
|                   |              |              |              |              |              | | instructions are executed.   |
|                   |              |              |              |              |              | | The arguments are either all |
|                   |              |              |              |              |              | | set through immediates or    |
|                   |              |              |              |              |              | | registers.                   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `set_ph_delta`    | | Immediate, | | Immediate, | | Immediate, | --           | --           | | Set an offset on top of the  |
|                   | | Register   | | Register   | | Register   |              |              | | relative phase of the NCO    |
|                   |              |              |              |              |              | | used by the AWG and          |
|                   |              |              |              |              |              | | acquisition. The offset is   |
|                   |              |              |              |              |              | | applied on top of the phase  |
|                   |              |              |              |              |              | | set using `set_ph`. See      |
|                   |              |              |              |              |              | | `set_ph` for more details    |
|                   |              |              |              |              |              | | regarding the arguments. The |
|                   |              |              |              |              |              | | parameters are cached and    |
|                   |              |              |              |              |              | | only updated when the        |
|                   |              |              |              |              |              | | `upd_param`, `play`,         |
|                   |              |              |              |              |              | | `acquire` or                 |
|                   |              |              |              |              |              | | `acquired_weighed`           |
|                   |              |              |              |              |              | | instructions are executed.   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `set_awg_gain`    | | Immediate, | | Immediate, | --           | --           | --           | | Set AWG gain for path 0      |
|                   | | Register   | | Register   |              |              |              | | using `argument 0` and path  |
|                   |              |              |              |              |              | | 1 using `argument 1`. Both   |
|                   |              |              |              |              |              | | gain values are divided in   |
|                   |              |              |              |              |              | | 2**sample path width steps.  |
|                   |              |              |              |              |              | | The parameters are cached    |
|                   |              |              |              |              |              | | and only updated when the    |
|                   |              |              |              |              |              | | `upd_param`, `play`,         |
|                   |              |              |              |              |              | | `acquire` or                 |
|                   |              |              |              |              |              | | `acquired_weighed`           |
|                   |              |              |              |              |              | | instructions are executed.   |
|                   |              |              |              |              |              | | The arguments are either     |
|                   |              |              |              |              |              | | all set through immediates   |
|                   |              |              |              |              |              | | or registers.                |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `set_awg_offs`    | | Immediate, | | Immediate, | --           | --           | --           | | Set AWG gain for path 0      |
|                   | | Register   | | Register   |              |              |              | | using `argument 0` and path  |
|                   |              |              |              |              |              | | 1 using `argument 1`. Both   |
|                   |              |              |              |              |              | | offset values are divided    |
|                   |              |              |              |              |              | | in 2**sample path width      |
|                   |              |              |              |              |              | | steps. The parameters are    |
|                   |              |              |              |              |              | | cached and only updated      |
|                   |              |              |              |              |              | | when the `upd_param`,        |
|                   |              |              |              |              |              | | `play`, `acquire` or         |
|                   |              |              |              |              |              | | `acquired_weighed`           |
|                   |              |              |              |              |              | | instructions are executed.   |
|                   |              |              |              |              |              | | The arguments are            |
|                   |              |              |              |              |              | | either all set through       |
|                   |              |              |              |              |              | | immediates or registers.     |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `upd_param`       | Immediate    | --           | --           | --           | --           | | Update the marker, phase,    |
|                   |              |              |              |              |              | | phase offset, gain and       |
|                   |              |              |              |              |              | | offset parameters set using  |
|                   |              |              |              |              |              | | their respective             |
|                   |              |              |              |              |              | | instructions and then wait   |
|                   |              |              |              |              |              | | for `argument 0` number of   |
|                   |              |              |              |              |              | | nanoseconds.                 |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `play`            | | Immediate, | | Immediate, | Immediate    | --           | --           | | Update the marker, phase,    |
|                   | | Register   | | Register   |              |              |              | | phase offset, gain and       |
|                   |              |              |              |              |              | | offset parameters set using  |
|                   |              |              |              |              |              | | their respective             |
|                   |              |              |              |              |              | | instructions, start playing  |
|                   |              |              |              |              |              | | AWG waveforms stored at      |
|                   |              |              |              |              |              | | indexes `argument 0` on      |
|                   |              |              |              |              |              | | path 0 and `argument 1` on   |
|                   |              |              |              |              |              | | path 1 and finally wait for  |
|                   |              |              |              |              |              | | `argument 2` number of       |
|                   |              |              |              |              |              | | nanoseconds. The arguments   |
|                   |              |              |              |              |              | | are either all set through   |
|                   |              |              |              |              |              | | immediates or registers.     |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `acquire`         | Immediate    | | Immediate, | Immediate    | --           | --           | | Update the marker, phase,    |
|                   |              | | Register   |              |              |              | | phase offset, gain and       |
|                   |              |              |              |              |              | | offset parameters set using  |
|                   |              |              |              |              |              | | their respective             |
|                   |              |              |              |              |              | | instruction, start the       |
|                   |              |              |              |              |              | | acquisition refered to using |
|                   |              |              |              |              |              | | index `argument 0` and       |
|                   |              |              |              |              |              | | store the bin data in bin    |
|                   |              |              |              |              |              | | index `argument 1`, finally  |
|                   |              |              |              |              |              | | wait for `argument 2` number |
|                   |              |              |              |              |              | | of nanoseconds. Integration  |
|                   |              |              |              |              |              | | is executed using a square   |
|                   |              |              |              |              |              | | weight with a preset length  |
|                   |              |              |              |              |              | | through the associated       |
|                   |              |              |              |              |              | | QCoDeS parameter. The        |
|                   |              |              |              |              |              | | arguments are either all     |
|                   |              |              |              |              |              | | set through immediates or    |
|                   |              |              |              |              |              | | registers.                   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `acquire_weighed` | Immediate    | | Immediate, | | Immediate, | | Immediate, | Immediate    | | Update the marker, phase,    |
|                   |              | | Register   | | Register   | | Register   |              | | phase offset, gain and       |
|                   |              |              |              |              |              | | offset parameters set using  |
|                   |              |              |              |              |              | | their respective             |
|                   |              |              |              |              |              | | instruction, start the       |
|                   |              |              |              |              |              | | acquisition refered to using |
|                   |              |              |              |              |              | | index `argument 0` and       |
|                   |              |              |              |              |              | | store the bin data in bin    |
|                   |              |              |              |              |              | | index `argument 1`, finally  |
|                   |              |              |              |              |              | | wait for `argument 4` number |
|                   |              |              |              |              |              | | of nanoseconds. Integration  |
|                   |              |              |              |              |              | | is executed using weights    |
|                   |              |              |              |              |              | | stored at indexes            |
|                   |              |              |              |              |              | | `argument 2` for path 0 and  |
|                   |              |              |              |              |              | | `argument 3` for path 1. The |
|                   |              |              |              |              |              | | arguments are either all     |
|                   |              |              |              |              |              | | set through immediates or    |
|                   |              |              |              |              |              | | registers.                   |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `wait`            | | Immediate, | --           | --           | --           | --           | | Wait for `argument 0`        |
|                   | | Register   |              |              |              |              | | number of nanoseconds.       |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `wait_trigger`    | | Immediate, | --           | --           | --           | --           | | Wait for external trigger    |
|                   | | Register   |              |              |              |              | | and then wait for            |
|                   |              |              |              |              |              | | `argument 0` number of       |
|                   |              |              |              |              |              | | nanoseconds.                 |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+
| `wait_sync`       | | Immediate, | --           | --           | --           | --           | | Wait for SYNQ to complete    |
|                   | | Register   |              |              |              |              | | on all connected sequencers  |
|                   |              |              |              |              |              | | over all connected           |
|                   |              |              |              |              |              | | instruments and then wait    |
|                   |              |              |              |              |              | | for `argument 0` number of   |
|                   |              |              |              |              |              | | nanoseconds.                 |
+-------------------+--------------+--------------+--------------+--------------+--------------+--------------------------------+

.. note::
    The duration argument for `upd_param`, `play`, `acquire`, `acquire_weighed`, `wait`, `wait_trigger` and `wait_sync` needs to a be multiple of 4ns.
    This will be reduced to 1ns in the future.


Arguments
"""""""""

+-------------+--------+-----------------------------------------------------------------------------------------------+
| Arguments   | Format | Description                                                                                   |
+=============+========+===============================================================================================+
| `Immediate` | #      | 32-bit decimal value (e.g. :code:`1000`)                                                      |
+-------------+--------+-----------------------------------------------------------------------------------------------+
| `Register`  | R#     | Register address in range 0 to 63 (e.g. :code:`R0`)                                           |
|             |        |                                                                                               |
|             |        | pointing to a 32-bit unsigned integer                                                         |
+-------------+--------+-----------------------------------------------------------------------------------------------+
| `Label`     | @label | Label name string (e.g. :code:`@main`)                                                        |
+-------------+--------+-----------------------------------------------------------------------------------------------+


Labels
""""""

Any instruction can be preceded by a label. This label can be used as a reference to that specific instruction. In other words, it can be used as a goto-point
by any instruction that can alter program flow (i.e. `jmp`, `jge`, `jlt` and `loop`). The label must be followed by a ':' character and a whitespace before
the actual referenced instruction.


Example
"""""""

This is a simple example of a Q1ASM program. It enables each marker channel output for 1μs and then stops.

.. code-block::

          move      1,R0        # Start at marker output channel 0 (move 1 into R0)
          nop                   # Wait a cycle for R0 to be available.

    loop: set_mrk   R0          # Set marker output channels to R0
          upd_param 1000        # Update marker output channels and wait 1μs.
          asl       R0,1,R0     # Move to next marker output channel (left-shift R0).
          nop                   # Wait a cycle for R0 to be available.
          jlt       R0,16,@loop # Loop until all 4 marker output channels have been set once.

          set_mrk   0           # Reset marker output channels.
          upd_param 4           # Update marker output channels.
          stop                  # Stop sequencer.


Waveforms
^^^^^^^^^

The waveforms are expressed as a list of floating point values in the range of 1.0 to -1.0 with a resolution of one nanosecond per sample. The AWG path uses
these waveforms to parametrically generate pulses on its outputs.

Waveform playback is started by the `play` instructions. Each waveform is paired with an index, which is used by this instruction to refer to
the associated waveform. The waveform is then completely played irrespective of further sequence processor instructions, except when the sequence processor
issues the playback of another waveform, in which case the waveform will be stopped and the new waveform will start. When waveforms are not played back-to-back,
the intermediate time will be filled by samples with a value of zero.

The programmed waveforms can be retrieved using :meth:`~pulsar_qrm.pulsar_qrm_ifc.pulsar_qrm_ifc.get_waveforms`.


Weights
^^^^^^^

The weights are expressed as a list of floating point values in the range of 1.0 to -1.0 with a resolution of one nanosecond per sample. The integration
units in the acquisition path apply (i.e. multiply) these weights during the integration process when the acquisition path is triggered for weighed integration.

Weighed integration is triggered by the `acquire_weighed` instruction. Each weight is paired with an index, which is used by this instruction to refer to
the associated weight. The weight is then played, like the waveforms discussed in the previous section and determines the length of the integration.
The weighed integration process continues irrespective of further sequence processor instructions, except when the sequence processor
issues another acquisition using the `acquire` or `acquire_weighed` instructions, in which case the integration will be stopped, the result will be stored and a
new integration will start.

The programmed weights can be retrieved using :meth:`~.get_weights`.


Acquisitions
^^^^^^^^^^^^

Acquisitions are started by the `acquire` or `acquire_weighed` instructions and will trigger the capture of 16k input samples on both inputs. This mode of operation is
called `scope mode` and will store the raw input samples in a temporary buffer. Every time an acquisition is started, this temporary memory is overwritten, so it is vital
to move the samples from the temporary buffer to a more lasting location before the start of the next acquisition. This is be done by calling :meth:`~.store_scope_acquisition`,
which moves the samples into the specified acquisition in the acquisition list of the sequencer, located in the RAM of the instrument. Multiple acquisitions can be stored in
this list before being retrieved from the instrument by simply calling :meth:`~.get_acquisitions`. Acquisitions are returned as a dictionary of acquisitions. Scope mode data is
located under the `scope` key as lists of floating point values in a range of 1.0 to -1.0 with a resolution of one nanosecond per sample, as well as an indication if the ADC was
out-of-range during the measurement.

.. note::
    Before calling :meth:`~.store_scope_acquisition`, be sure to call :meth:`~pulsar_qrm.pulsar_qrm_ifc.pulsar_qrm_ifc.get_sequencer_state` and :meth:`~.get_acquisition_state` in that order.
    This ensures that both the sequencer has finished and that there is an acquisition ready.

The acquisition path also has an averaging function set through the :meth:`!scope_acq_avg_mode_en_path#` parameters. This enables the automatic
accumulation of acquisitions, where sample `N` of acquisition `M` is automatically accumulated to sample `N` of acquisition `M+1`. This happens while the acquisition is
still in the temporary buffer, so after the desired number of averaging acquisitions is completed, call :meth:`.store_scope_acquisition` to store the
accumulated result in the acquisition list. Once retrieved from the instrument, the accumulated samples will automatically be divided by the number of averages to get the actual
averaged acquisition result.

.. tip::
    For debug purposes, the acquisition path can also be triggered using a trigger level, where if the input exceeds this level, an acquisition is started. See the
    :meth:`!sequencer#_trigger_mode_acq_path#` and :meth:`!sequencer#_trigger_level_acq_path#` parameters for more information.


Continuous waveform mode
------------------------

The sequencer also supports a continuous waveform mode of operation, where the waveform playback control of sequence processor is completely bypassed and a single
waveform is just played back on a loop. This mode can be enabled using the :meth:`!sequencer#_cont_mode_en_awg_path#` parameter and the waveform can be selected
using the :meth:`!sequencer#_cont_mode_waveform_idx_awg_path#` parameter. The waveforms used in this mode must be a multiple of four samples long (i.e. 4ns).

When in continuous mode, simply program, arm, start and stop the sequencer using the regular control functions and parameters (i.e. :meth:`!sequencer#_waveforms_and_program`,
:meth:`!arm_sequencer`, :meth:`!start_sequencer` and :meth:`!stop_sequencer`). However, be aware that the sequencer processor can still
control parts of the AWG path, like phase, gain and offset, while the sequencer operates in this mode. Therefore, we advise to program the sequence processor with a single
`stop` instruction.

.. note::
    We realise that the current way of controlling this mode is not optimal, so in the near future we will be implementing additional driver support to streamline this mode.
