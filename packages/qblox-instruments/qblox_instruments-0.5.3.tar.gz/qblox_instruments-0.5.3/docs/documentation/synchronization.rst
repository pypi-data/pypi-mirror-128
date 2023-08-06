.. _synchronization:

Synchronization
===============

In this section we explain how to synchronize multiple instruments in your setup including Qblox `Pulsar series <https://www.qblox.com/pulsar>`_ instruments.
Synchronization is based on two aspects:

    1. A shared reference clock, preferably phase aligned, so that all instruments use the same reference to base their operations on.
    2. A synchronized start event, so that all instruments start their operations simultaneously.

The following subsections will go into more detail on how to achieve both aspects.


Reference clock
---------------

Like most instruments the Qblox instruments use a 10 MHz clock as a time reference. To synchronize multiple instruments in your setup you will need to connect such a reference clock to
the REF\ :sup:`in` SMA connector of the instruments (10 MHz, 1 Vpp nominal @ 50 Ω) (see section :ref:`getting_started/overview:Overview`) and set the :meth:`!reference_source` parameter to external. Connecting the reference can
be done in two ways:

    1. Through a clock distribution module that distributes a reference clock provided by a reference clock source to all instruments in the setup as shown in the figure below.
       Care has to be taken that all distributed reference clocks are length matched to keep the clocks phase aligned.

    .. figure:: /figures/synchronization_clk_dist_module.svg
        :width: 400px
        :align: center
        :alt: Clock synchronization through clock distribution module.

    |

    2. Through daisy-chaining the reference clock from one Qblox instrument to the next as shown in the figure below. The Qblox instruments have been configured so that when a 50 cm coaxial cable is used
       to connect the REF\ :sup:`out` SMA connector of one instrument to the REF\ :sup:`in` SMA connector of the next, the instrument's reference clocks are phase align to one another. This removes the need
       of an additional clock distribution module. The first instrument in the daisy-chain can either use an internal reference source or an external reference if you wish to connect additional non-Qblox
       instruments. All other Qblox instruments need to be configured to use external reference sources.

    .. figure:: /figures/synchronization_clk_dist_chain.svg
        :width: 400px
        :align: center
        :alt: Clock synchronization through clock daisy-chain.


SYNQ
----

To synchronize the start event of the instruments, Qblox SYNQ technology can be used to greatly simply the process. To use this SYNQ technology, the Qblox instruments need to be daisy-chained using the two SYNC ports
(see section :ref:`getting_started/overview:Overview`) as shown in the figure below. Additionally, the :meth:`!sequencer#_sync_en` parameter needs to be set for every sequencer in the instrument participating in the
experiment and these same sequencers need to execute the `wait_sync` instruction (see section :ref:`documentation/sequencer:Instructions`). Note, these last two steps also need to done when only using
a single Qblox instrument. The Qblox SYNQ technology will then automatically align the timing of every participating sequencer in all Qblox instruments to within 300 ps of one another.

.. figure:: /figures/synchronization_sync.svg
    :width: 400px
    :align: center
    :alt: SYNQ daisy-chain.

Additionally, the marker output channels can be controlled by the sequencers to trigger other non-Qblox instruments, thereby synchronizing them with the Qblox instruments. However, care needs to be taken to compensate
for any trigger delay caused by the connection or the triggered instrument itself.


Trigger
-------

If desired, the Qblox instruments can also be triggered by other non-Qblox instruments. To achieve this, simply connect the trigger signal to the TRIG\ :sup:`in` SMA connector (0-3.3 V, high-Z) (see section :ref:`getting_started/overview:Overview`)
as shown in the figure below and have any sequencer in the Qblox instrument participating in the experiment execute the `wait_trigger` instruction (see section :ref:`documentation/sequencer:Instructions`).

.. figure:: /figures/synchronization_trigger.svg
    :width: 400px
    :align: center
    :alt: External trigger.
