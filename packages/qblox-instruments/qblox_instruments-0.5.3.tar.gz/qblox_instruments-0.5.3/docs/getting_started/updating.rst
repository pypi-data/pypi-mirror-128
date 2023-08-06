.. _updating:

Updating
========

In this section we will explain how to update the firmware and IP address of your module.
Go to `Qblox.com <https://qblox.com>`_ and download the firmware from the download section.
The firmware includes the Qblox Configuration Manager with which you can configure and update your module.

Once you have extracted the firmware, go to the directory in which it was extracted using the terminal of your choice
and execute the following commands using `Python 3.8 <https://www.python.org/downloads/release/python-380/>`_.

.. note::
    The default IP address of the module is ``192.168.0.2``. Replace the IP address of any following instruction accordingly if the module's IP address was ever changed.

To update the firmware:

.. code-block:: console

    $ python cfg_man.py -u 192.168.0.2

To update the IP address:

.. code-block:: console

    $ python cfg_man.py -i 192.168.0.<new_ip_digit(s)> 192.168.0.2

.. tip::
    When changing the IP address of the device, put a label on the instrument with its new IP address. This will help avoid connectivity issues in the future.

After executing one of the commands above, follow the instructions given by the Qblox Configuration Manager. The module will reboot, after which the update is complete.

During reboot, the LEDs will turn purple/red, which indicates the reboot is in progress. When the LEDs turn green/blue again, the reboot is finished.
If the module does not finish rebooting within 1-2 minutes, please remove power from the module and wait one minute before powering it on again. This might be required up to two times.
Once to start the internal update process and a second time to start using the updated module.

Please make sure your installed Qblox instruments package is compatible with the installed firmware.
(See `Qblox instruments PyPI <https://pypi.org/project/qblox-instruments/>`_ and section :ref:`getting_started/installation:Installation`)

.. tip::
    Executing ``$ python cfg_man.py -h`` will show you a list of additional functions, like querying the firmware version and reverting the last firmware update.
