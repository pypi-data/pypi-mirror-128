.. _ip_addr:

Finding the IP address of a module
----------------------------------

Here we provide some tips to help find the IP address of a device (e.g. a Pulsar Series QCM or QRM). We will show how to scan a range of IP addresses on the :code:`192.168.0.X` subnet.

.. tip::
    When changing the IP address of the device, put a label on the instrument with its new IP address. This will help avoid connectivity issues in the future.

1. Follow steps 1-3 described in :ref:`getting_started/connecting_pulsar:Connecting to multiple modules`.
2. If possible, disconnect all other devices that share the same network, such that only the host PC and the device with the an unknown IP are on the same subnetwork.
3. Scan the IP address within the subnet:


MacOS/Linux
^^^^^^^^^^^^
Open a terminal of your choice and run:

.. code-block:: console

    $ sudo nmap -sn 192.168.0.*

The output should look similar to:

.. code-block:: console

    Starting Nmap 7.91 ( https://nmap.org ) at 2021-01-02 20:16 CET
    Nmap scan report for 192.168.0.3
    Host is up (0.00029s latency).
    MAC Address: 04:91:62:BF:DE:57 (Microchip Technology)
    Nmap scan report for 192.168.0.200
    Host is up.
    Nmap done: 256 IP addresses (2 hosts up) scanned in 13.05 seconds

In this case our device has the IP :code:`192.168.0.3` while the network adapter of our host PC has been configured at :code:`192.168.0.200`.


Windows
^^^^^^^
On Windows we recommend installing the latest version of *nmap* that comes with a graphical interface (Zenmap).

1. Visit `download section at nmap.org <https://nmap.org/download.html>`_ and download the *Latest stable release self-installer* under the *Microsoft Windows binaries* section.
2. Run the installer with default options.
3. Execute **as administrator** the *Nmap - Zenmap GIU* that should appear on your Desktop (or in the start menu)
4. Type in the *Command* field :code:`nmap -sn 192.168.0.*` and hit *Enter* on your keyboard. After a few seconds the output should look similar to:

.. figure:: /figures/zenmap_windows.png
    :width: 800px
    :align: center
    :alt: Nmap - Zenmap GUI on windows

In this case our device has the IP :code:`192.168.0.3` while the network adapter of our host PC has been configured at :code:`192.168.0.240`.