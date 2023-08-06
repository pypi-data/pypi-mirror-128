.. _troubleshooting:

Troubleshooting
===============

"Have you tried turning it off and on again?" - The IT Crowd

Below you will find a table with common problems and potential solutions for Qblox `Pulsar series instruments <https://www.qblox.com/pulsar>`_.
If your problem is not listed or you are not able to fix your problem, please contact `support@qblox.com <support@qblox.com>`_ for help.

+----------------------------------------------------+------------------------------------------------------+
| Problem                                            | Solutions                                            |
+====================================================+======================================================+
| | `The status (S) LED is not green.`               | | If the LED is red, it indicates a serious error    |
|                                                    | | that needs to be resolved.                         |
|                                                    | | Query :meth:`!get_system_status` to see            |
|                                                    | | what the problem is.                               |
|                                                    +------------------------------------------------------+
|                                                    | | If the LED is orange, the LED indicates a critical |
|                                                    | | warning, that an error has occurred but has been   |
|                                                    | | resolved.                                          |
|                                                    | | Query :meth:`!get_system_status` see               |
|                                                    | | what the problem is.                               |
+----------------------------------------------------+------------------------------------------------------+
| | `The reference clock (R) LED is not green.`      | | If the LED is red, no reference clock is found.    |
|                                                    | | Most likely you have selected the external input   |
|                                                    | | as reference source, but have not connected the    |
|                                                    | | reference.                                         |
|                                                    +------------------------------------------------------+
|                                                    | | If the LED is blue, the internal reference clock   |
|                                                    | | is selected. Use the parameter                     |
|                                                    | | :meth:`!reference_source` to change                |
|                                                    | | this if necessary.                                 |
+----------------------------------------------------+------------------------------------------------------+
| | `The channel (I/O) LEDs are not green.`          | | If the LED is red, an error has occurred in one or |
|                                                    | | more of the connected sequencers.                  |
|                                                    | | Query :meth:`!get_sequencer_state` to              |
|                                                    | | see what the problem is.                           |
|                                                    +------------------------------------------------------+
|                                                    | | If the LED is purple or blue, one or more of the   |
|                                                    | | connected sequencers is armed or running.          |
|                                                    | | Query :meth:`!get_sequencer_state` to              |
|                                                    | | see what the sequencers are doing.                 |
|                                                    +------------------------------------------------------+
|                                                    | | If the LED is orange, one or more of the           |
|                                                    | | connected sequencers is causing the output to      |
|                                                    | | clip. Query :meth:`!get_sequencer_state` to        |
|                                                    | | see what the sequencers are doing.                 |
+----------------------------------------------------+------------------------------------------------------+
| | `I cannot connect to the instrument.`            | | Make sure that the Ethernet cables are firmly      |
|                                                    | | inserted into the instrument and host PC (see      |
|                                                    | | section :ref:`connecting`).                        |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that the instrument and host PC are      |
|                                                    | | within the same subnet of the same network         |
|                                                    | | (see section :ref:`connecting`).                   |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that you are using the IP address of the |
|                                                    | | instrument. If you you do not know the IP address  |
|                                                    | | or are not sure you are using the correct one, see |
|                                                    | | section :ref:`ip_addr`.                            |
+----------------------------------------------------+------------------------------------------------------+
| | `When I connect to the instrument, I get an`     | | This indicates that the version of your installed  |
| | `error that the driver and firmware are`         | | Qblox instruments package and the firmware of the  |
| | `incompatible.`                                  | | instrument you  are trying to connect to are not   |
|                                                    | | compatible (see sections :ref:`installation` and   |
|                                                    | | :ref:`updating`).                                  |
|                                                    +------------------------------------------------------+
|                                                    | | If all else fails, the instrument can be           |
|                                                    | | instantiated in debug mode where this error is     |
|                                                    | | bypassed. However, this is highly discouraged and  |
|                                                    | | no guarantees can be given that the instruments    |
|                                                    | | will function properly. Nor can further support be |
|                                                    | | provided. Please see                               |
|                                                    | | :class:`~pulsar_qcm.pulsar_qcm` and                |
|                                                    | | :class:`~pulsar_qrm.pulsar_qrm`.                   |
+----------------------------------------------------+------------------------------------------------------+
| | `When I connect a reference clock to`            | | Make sure that the reference clock source is       |
| | `REF`\ :sup:`in` `and configure the instrument`  | | outputting the clock as a 10 MHz, 1 Vpp signal.    |
| | `to use an external reference clock, the`        | | The REF\ :sup:`out` from another Qblox instrument  |
| | `reference clock LED (R) turns red.`             | | can be used for this (see section                  |
|                                                    | | :ref:`synchronization`).                           |
+----------------------------------------------------+------------------------------------------------------+
| | `I cannot get the SYNQ to work.`                 | | Make sure that you are using a USB-C compliant     |
|                                                    | | cable to connect the instruments using the SYNQ    |
|                                                    | | connectors (see section :ref:`overview`).          |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that the SYNQ cables are firmly inserted |
|                                                    | | into the instrument. A distinct click should be    |
|                                                    | | felt when inserting them into the instruments.     |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that the SYNQ is enabled by setting the  |
|                                                    | | :meth:`!sequencer#_sync_en` parameter.             |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that the sequencers are used to play     |
|                                                    | | waveforms and start acquisitions and that these    |
|                                                    | | sequencers are running the `wait_sync` instruction |
|                                                    | | (see section :ref:`sequencer`).                    |
+----------------------------------------------------+------------------------------------------------------+
| | `I cannot get the trigger to work.`              | | Make sure the trigger source is connected to the   |
|                                                    | | TRIG\ :sup:`in` SMA connector (see section         |
|                                                    | | :ref:`Overview`).                                  |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that the trigger source is outputting a  |
|                                                    | | trigger. This can be easily verified using an      |
|                                                    | | oscilloscope.                                      |
|                                                    +------------------------------------------------------+
|                                                    | | Make sure that the sequencers are used to play     |
|                                                    | | waveforms and start acquisitions and that these    |
|                                                    | | sequencers are running the `wait_trigger`          |
|                                                    | | instruction (see section :ref:`sequencer`).        |
+----------------------------------------------------+------------------------------------------------------+
| | `The output voltage of the instrument is twice`  | | Make sure that you terminate the output signal     |
| | `as high as expected.`                           | | with 50 Ω.                                         |
+----------------------------------------------------+------------------------------------------------------+
| | `I updated the firmware or IP address using the` | | No, this is normal behaviour and indicates that    |
| | `Qblox Configuration Manager and the LEDs`       | | the instrument has stopped its internal processes  |
| | `turned purple and/or red. Did something go`     | | and is trying to reboot. Though, some are not able |
| | `wrong?`                                         | | to and need a manual power cycle                   |
|                                                    | | (see :ref:`updating`).                             |
+----------------------------------------------------+------------------------------------------------------+
| | `I updated the firmware or IP address using the` | | Unfortunately, some instruments do not have the    |
| | `Qblox Configuration Manager, but the`           | | the capability to reboot and have to be manually   |
| | `instrument won't automatically reboot.`         | | power cycled. Some up to two times to complete an  |
|                                                    | | update (see :ref:`updating`).                      |
+----------------------------------------------------+------------------------------------------------------+
