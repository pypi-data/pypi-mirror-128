Azure Backend
=============

Using Coiled with Azure
-----------------------

You can configure Coiled to launch Dask clusters and run computations on
Microsoft Azure, either within Coiled's Azure account or within your own Azure
account.

.. tip::

    In addition to the usual cluster logs, our current Azure backend support
    also includes system-level logs. This provides rich insight into any
    potential issues.


Using Coiled's Azure Account
----------------------------

You can configure Coiled to launch Dask clusters and run computations within
Coiled's Azure account. This makes it easy for you to get started quickly,
without needing to set up any additional infrastructure outside of Coiled.

.. figure:: images/backend-coiled-azure-vm.png
   :width: 100%

To use Coiled on Azure, log in to your Coiled account and access your dashboard.
Click on ``Account`` on the left navigation bar, then click the ``Edit`` button
to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

On the ``Select Your Cloud Provider`` step, select the ``Azure`` option, then
click the ``Next`` button:

.. figure:: images/cloud-backend-provider-azure.png
   :width: 100%

On the ``Configure Azure`` step, select ``Launch in Coiled's Azure Account`` and
click the ``Next`` button. Finally, select the registry you wish to use, then
click the ``Submit`` button.

Coiled is now configured to use Azure!

From now on, when you create Coiled clusters, they will be provisioned in
Coiled's Azure account.


Using your own Azure Account
----------------------------

Alternatively, you can configure Coiled to create Dask clusters and run
computations entirely within your own Azure account (within a resource group of
your choosing). This allows you to make use of security/data access controls,
compliance standards, and promotional credits that you already have in place
within your Azure account.

.. figure:: images/backend-external-azure-vm.png

Note that when running Coiled on your Azure account, Coiled Cloud is only
responsible for provisioning cloud resources for Dask clusters that you create.
Once a Dask cluster is created, all computations, data transfer, and Dask
client-to-scheduler communication occurs entirely within your Azure account.


Step 1: Obtain Azure service principal and secret
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled provisions resources on your Azure account through the use of a service
principal that is associated with a custom IAM role (which will be created in
the next step).

In this step, you can use the Azure Console to
`create a new service principal <https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#register-an-application-with-azure-ad-and-create-a-service-principal>`_
(or select an existing service principal) that will be used with Coiled.

Once you have created or identified a Azure service principal for working with
Coiled, you’ll need to create a new (or use an existing) secret. Follow the
steps in the Azure documentation to
`create and manage a service account secret <https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#option-2-create-a-new-application-secret>`_.

After you create a secret, the value of the secret will be displayed in the
Azure portal and will appear similar to ``63.E-B-moRu1IG_K2Y4.yY4s6WwcLzn4u5``.
Keep your secret handy since you’ll use it in Coiled Cloud in a later step.


Step 2: Create a custom role
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Coiled requires a limited set of permissions within a resource group to be able
to provision infrastructure and compute resources in your Azure account. You'll
need to create a new custom role in Azure and assign the appropriate set of
permissions to it. When creating a new custom role in a resource group, you can
create a new resource group for Coiled to use to provision Dask clusters, or you
can use an existing resource group.

In this step, you'll create a new custom role in your desired resource group by
following the steps in the Azure documentation on
`creating a custom role <https://docs.microsoft.com/en-us/azure/role-based-access-control/custom-roles>`_.
Specify a custom role name such as ``coiled`` that will make it easy to locate
in the next step.

When you arrive at the step to specify the necessary permissions, you can use
the following JSON code that contains all of the permissions that Coiled
requires to be able to create and manage Dask clusters in your Azure account:

.. dropdown:: Azure custom role (JSON)
   :title: bg-white

   .. code-block:: json

      {
        "properties": {
          "roleName": "coiled",
          "description": "",
          "assignableScopes": [],
          "permissions": [
            {
              "actions": [
                "Microsoft.Compute/disks/read",
                "Microsoft.Compute/disks/write",
                "Microsoft.Compute/disks/delete",
                "Microsoft.Compute/images/read",
                "Microsoft.Compute/images/write",
                "Microsoft.Compute/images/delete",
                "Microsoft.Compute/virtualMachines/read",
                "Microsoft.Compute/virtualMachines/write",
                "Microsoft.Compute/virtualMachines/delete",
                "Microsoft.Compute/virtualMachines/capture/action",
                "Microsoft.Compute/virtualMachines/deallocate/action",
                "Microsoft.Compute/virtualMachines/generalize/action",
                "Microsoft.ContainerRegistry/registries/read",
                "Microsoft.ContainerRegistry/registries/write",
                "Microsoft.ContainerRegistry/registries/pull/read",
                "Microsoft.ContainerRegistry/registries/push/write",
                "Microsoft.Network/networkInterfaces/read",
                "Microsoft.Network/networkInterfaces/write",
                "Microsoft.Network/networkInterfaces/delete",
                "Microsoft.Network/networkInterfaces/join/action",
                "Microsoft.Network/networkSecurityGroups/read",
                "Microsoft.Network/networkSecurityGroups/write",
                "Microsoft.Network/networkSecurityGroups/delete",
                "Microsoft.Network/networkSecurityGroups/securityRules/read",
                "Microsoft.Network/networkSecurityGroups/securityRules/write",
                "Microsoft.Network/networkSecurityGroups/securityRules/delete",
                "Microsoft.Network/networkSecurityGroups/join/action",
                "Microsoft.Network/publicIPAddresses/read",
                "Microsoft.Network/publicIPAddresses/write",
                "Microsoft.Network/publicIPAddresses/delete",
                "Microsoft.Network/routeTables/read",
                "Microsoft.Network/routeTables/write",
                "Microsoft.Network/routeTables/delete",
                "Microsoft.Network/routeTables/join/action",
                "Microsoft.Network/virtualNetworks/read",
                "Microsoft.Network/virtualNetworks/write",
                "Microsoft.Network/virtualNetworks/delete",
                "Microsoft.Network/virtualNetworks/subnets/read",
                "Microsoft.Network/virtualNetworks/subnets/write",
                "Microsoft.Network/virtualNetworks/subnets/delete",
                "Microsoft.Network/virtualNetworks/subnets/join/action",
                "Microsoft.Network/publicIPAddresses/join/action",
                "Microsoft.Resources/subscriptions/resourceGroups/read",
                "Microsoft.Storage/storageAccounts/read",
                "Microsoft.Storage/storageAccounts/write",
                "Microsoft.Storage/storageAccounts/delete",
                "Microsoft.Storage/storageAccounts/blobServices/containers/read",
                "Microsoft.Storage/storageAccounts/blobServices/containers/write",
                "Microsoft.Storage/storageAccounts/listkeys/action"
              ],
              "notActions": [],
              "dataActions": [],
              "notDataActions": []
            }
          ]
        }
      }

.. note::

   When viewing your custom role in JSON format in the Azure portal, be sure to
   copy the existing value for ``assignableScopes`` into the above JSON
   template, which will ensure that the custom role can be used within the
   resource group that you specify.

After you review and save the custom role, you are ready to assign the custom
role to a service principal in the following step.


Step 3: Assign custom role to service principal
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you’ve created a service principal and a custom role to use with Coiled,
you can assign the custom role to the service principal by following the steps
in the
`Azure documentation on assigning roles <https://docs.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal>`__.

However you choose to assign the custom role - be sure to verify that that the
Azure service principal that you configured earlier is attached to your new
custom role and resource group that will be used with Coiled.


Step 4: Configure Coiled Cloud backend
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now you're ready to configure the cloud backend in your Coiled Cloud account to
use your Azure account and Azure service principal credentials.

To configure Coiled to use your Azure account, log in to your Coiled account and
access your dashboard. Click on ``Account`` on the left navigation bar, then
click the ``Edit`` button to configure your Cloud Backend Options:

.. figure:: images/cloud-backend-options.png
   :width: 100%

.. note::

   You can configure a different cloud backend for each Coiled account (i.e.,
   your personal/default account or your :doc:`Team account <teams>`). Be sure
   that you're configuring the correct account by switching accounts at the top
   of the left navigation bar in your Coiled dashboard if needed.

On the ``Select Your Cloud Provider`` step, select the ``Azure`` option, then
click the ``Next`` button:

.. figure:: images/cloud-backend-provider-azure.png
   :width: 100%

On the ``Configure Azure`` step, select the ``Launch in my Azure account``
option, refer to the necessary values in the Azure portal and specify the values
for the ``Client ID (Application ID)``, ``Secret``, ``Subscription ID``,
``Tenant ID``, and ``Resource Group``, then click the ``Next`` button.

.. figure:: images/cloud-backend-credentials-azure.png
   :width: 100%

On the ``Container Registry`` step, select where you want to store Coiled
software environments, then click the ``Next`` button:

.. figure:: images/cloud-backend-registry-azure.png
   :width: 100%

Review the cloud backend provider options that you've configured, then click on
the ``Submit`` button:

.. figure:: images/cloud-backend-review-azure.png
   :width: 100%

Coiled is now configured to use your Azure Account!

From now on, when you create Coiled clusters, they will be provisioned in your
Azure account.


Step 5: Create a Coiled cluster
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now that you've configured Coiled to use your Azure account, you can create a
cluster to verify that everything works as expected.

To create a Coiled cluster, follow the steps listed in the quick start on your
Coiled dashboard, or follow the steps listed in the
:doc:`Getting Started <getting_started>` documentation, both of which will walk
you through installing the Coiled Python client and logging in, then running a
command such as:

.. code-block:: python

   import coiled

   cluster = coiled.Cluster(n_workers=1)

   from dask.distributed import Client

   client = Client(cluster)
   print("Dashboard:", client.dashboard_link)

.. note::

  If you're using a :doc:`Team account <teams>` in Coiled, be sure to specify
  the ``account=`` option when creating a cluster, as in:

  .. code-block:: python

     cluster = coiled.Cluster(n_workers=1, account="my-team-account-name")

  Otherwise, the cluster will be created in your personal/default account in
  Coiled, which you can access by switching accounts at the top of the left
  navigation bar in your Coiled dashboard.

Once your Coiled cluster is up and running, you can run a sample calculation on
your cluster to verify that it's functioning as expected, such as:

.. code-block:: python

   df = dd.read_csv(
       "s3://nyc-tlc/trip data/yellow_tripdata_2019-*.csv",
       dtype={
           "payment_type": "UInt8",
           "VendorID": "UInt8",
           "passenger_count": "UInt8",
           "RatecodeID": "UInt8",
       },
       storage_options={"anon": True},
       blocksize="16 MiB",
   ).persist()

   df.groupby("passenger_count").tip_amount.mean().compute()

At this point, Coiled will have created resources within your Azure account that
are used to power your Dask clusters.


Region
------

Azure support is currently only available in the ``East US`` region. If you have
data in a different region on Azure, you may be charged transfer fees.


GPU support
-----------

This backend allows you to run computations with GPU-enabled machines if your
account has access to GPUs. See the :doc:`GPU best practices <gpu>`
documentation for more information on using GPUs with this backend.

Workers currently have access to a single GPU, if you try to create a cluster
with more than one GPU, the cluster will not start, and an error will be
returned to you.

Networking
----------

When Coiled is configured to run in your own Azure account, you can customize
the firewall ingress rules for resources that Coiled creates in your Azure
account.

By default, Dask schedulers created by Coiled will be reachable via ports 22,
8787 and 8786 from any source network. This is consistent with the default
ingress rules that Coiled configures for its GCP firewalls:

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
   * - tcp
     - 22
     - ``0.0.0.0/0``

.. note::
    Ports 8787 and 8786 are used by the Dask dashboard and Dask protocol respectively.
    Port 22 optionally supports incoming SSH connections to the virtual machine.

Configuring firewall rules
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

   This feature is currently under active development and should be considered
   to be in an early experimental/testing phase.

While allowing incoming connections on the default Dask ports from any source
network is convenient, you might want to configure additional security measures
by restricting incoming connections. This can be done by using
:meth:`coiled.set_backend_options` or by using the ``backend_options``.
