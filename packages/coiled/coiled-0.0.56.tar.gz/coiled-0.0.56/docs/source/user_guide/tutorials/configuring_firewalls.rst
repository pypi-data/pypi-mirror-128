=====================================
Configuring security groups/firewalls
=====================================


While allowing incoming connections on the default Dask ports from any source
network is convenient, you might want to configure additional security measures
by restricting incoming connections. There are four arguments that can be
passed to ``set_backend_options`` or to ``backend_options`` keyword agument for the 
``coiled.Cluster`` constructor. To achieve this:

- ``enable_public_ssh``
- ``enable_public_http``
- ``disable_public_ingress``
- ``firewall``

Enable/Disable SSH
------------------

``enable_public_ssh`` will allow ingress from ``0.0.0.0/0`` to port 22 when
set to ``True``. ``enable_public_http`` will allow ingress from
``0.0.0.0/0`` to ports 8786 and 8787 when set to ``True``. If either of these
options are set to ``False``, then incoming connections to the respective ports
are only allowed from within the VPC that the Dask scheduler is
created in.

An example of the ingress rules on created security groups with ``enable_public_ssh`` set to ``False``:

.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Protocol
     - Port
     - Source
   * - tcp
     - 8787
     - ``0.0.0.0/0``
   * - tcp
     - 8786
     - ``0.0.0.0/0``


Disabling public ingress
------------------------

``disable_public_ingress`` can be used to override all other flags and
disallow incoming connections that originate from outside of your VPC or cloud
provider account. When set to ``True`` security group ingress rules we create
will look like this:


.. list-table::
   :widths: 25 25 50
   :header-rows: 1

   * - Protocol
     - Port
     - Source
   * - tcp
     - 8787
     - ``<coiled-vpc-CIDR-block>``
   * - tcp
     - 8786
     - ``<coiled-vpc-CIDR-block>``
   * - tcp
     - 22
     - ``<coiled-vpc-CIDR-block>``

In this example, ``<coiled-vpc-CIDR-block>`` represents the CIDR block
designated to the VPC that Coiled creates in your cloud provider account.
An example value would be ``10.0.0.0/24``. Note that this will vary and is
only known after the backend is initialized.

In this case, the Dask scheduler will only be accessible from within the VPC that Coiled
creates. Connections originating from outside of this VPC will be blocked.

For users to be able to use the Coiled Python client or connect to the Dask
scheduler dashboard from their laptops or VMs, you will need to configure
internal networking access and routes to this VPC at the networking
level. For example, you could use
`VPC Peering or Transit Gateways <https://docs.aws.amazon.com/whitepapers/latest/building-scalable-secure-multi-vpc-network-infrastructure/vpc-to-vpc-connectivity.html>`_
to enable network connectivity and route traffic between internal VPN clients
and Dask clusters managed by Coiled.

.. _backend_options_networking_example:

Example
^^^^^^^

You can specify networking configuration directly in Python using ``set_backend_options``:

.. code-block::

    import coiled

    coiled.set_backend_options(
        backend="aws",
        aws_access_key_id="<your-access-key-id-here>",
        aws_secret_access_key="<your-access-key-secret-here>",
        create_vpc=True,
        # Block incoming connections from 0.0.0.0/0
        disable_public_ingress=True 
    )

This configuration will be stored at the account level. It can be overridden by passing it to ``coiled.Cluster``:

.. code-block::

    import coiled

    coiled.Cluster(
        backend_options={
            "disable_public_ingress": True
        }
    )

Or save them to your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        disable_public_ingress: True

Opening ports for a specific CIDR block
----------------------------------------

If you need more control over the security groups/firewall for clusters
created by Coiled, use the ``firewall`` argument to specify ingress rules for
a ``CIDR`` block on specified list of ``ports``.
Each new security group is created with ingress rules on these ports for
the specified CIDR block.

You can also use some of the previous flags together with the ``firewall``
argument. For example:

.. code-block:: python

  import coiled

  coiled.set_backend_options(
      backend="aws",
      aws_access_key_id="<your-access-key-id-here>",
      aws_secret_access_key="<your-access-key-secret-here>",
      create_vpc=True,
      enable_public_ssh=False,
      firewall={"ports": [100, 9012, 465], "cidr": "10.1.0.2/16"},
  )

.. list-table::
    :widths: 25 25 50
    :header-rows: 1

    * - Protocol
      - Port
      - Source
    * - tcp
      - 8787
      - ``10.1.0.2/16``
    * - tcp
      - 8786
      - ``10.1.0.2/16``
    * - tcp
      - 100
      - ``10.1.0.2/16``
    * - tcp
      - 9012
      - ``10.1.0.2/16``
    * - tcp
      - 465
      - ``10.1.0.2/16``

You can also use the ``backend_options`` to achieve the same results. For
example:

.. code-block::

    import coiled

    coiled.Cluster(
        backend_options={
            "enabled_public_ssh": False,
            "firewall": {"ports": [100, 9012, 465], "cidr": "10.1.0.2/16"}
        }
    )

