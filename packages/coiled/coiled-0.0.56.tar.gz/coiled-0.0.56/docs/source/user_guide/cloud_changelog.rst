.. cloud_changelog:

==========================
Coiled Cloud Release Notes
==========================

These release notes are related to updates for `cloud.coiled.io <https://cloud.coiled.io>`_.

10 November 2021
================

Fixes
+++++

- Dask workers will now use all CPU/Memory available for the instance type in which they have
  been created. In the past, workers would be limited by your CPU/Memory specification. 


Enhancements
++++++++++++

- Moved the **Coiled Subscription** tab up on the account settings page to make it easier
  for you to see how many credits you have used so far.
- If you are using Coiled on your cloud provider, you can now
  customize ingress rules for the firewall/security group created by Coiled
  by specifying ingress ports and a CIDR block.

Deprecated
++++++++++
- Coiled Notebooks and Coiled Jobs were an experimental feature which is being deprecated.
  After December 1, 2021, these will no longer be available.


Documentation
+++++++++++++

- Updated the list of dependencies in the documentation page :doc:`software_environment_creation`
  to include ``dask[complete]`` while creating a software environment with pip.
- Added troubleshooting article for :doc:`repeated cluster timeout errors.
  <troubleshooting/repeated_timeout_errors>`.
- Embedded tutorial videos for :ref:`cluster configuration <cluster-config>`
  and :ref:`software environments <software-envs>` documentation.

27 October 2021
===============

Fixes
+++++

- The route table for the private subnet that is created when Coiled creates a VPC
  in your AWS account, is now called ``coiled-vm-private-router`` instead of
  ``coiled-vm-public-router``.
- Mitigate Rate Limit exceptions when performing some actions like scaling clusters,
  which should improve cluster reliability.
- Software environment names must now be lowercase only.


Enhancements
++++++++++++
 
- Removed experimental warnings for GCP and Azure in the UI when choosing a
  backend option for an account.
- Removed fallback option to fetch logs from instances via SSH.


Documentation
+++++++++++++ 

- Removed experimental notes for GCP and Azure in the respective section of
  the documentation for these backends.
- Updated default ``worker_memory`` to ``8GiB`` in a few pages where it was
  saying that the default was ``16GiB``.
- Added a section about network architecture to the :doc:`security` page.
- Added a tutorial on :doc:`tutorials/select_instance_types`.
- Added a tutorial on :doc:`tutorials/select_gpu_type`.
- Added section on selecting instance types in the documentation page
  :doc:`cluster_creation`.
- Added a Networking section on the documentation page for the :doc:`backends_aws`
  that explains how you can specify your AWS security groups using the new arguments
  ``enable_public_http``, ``enable_public_ssh`` and ``disable_public_ingress``.


13 October 2021
===============

Fixes
+++++

* Environment variables sent to the Cluster with the keyword argument 
  ``environ=`` are now being converted to strings, which fixes
  occasional failures when sending non-string values to the Cluster.

Enhancements
++++++++++++

* You can now use Coiled in your own GCP account. Please refer to the
  :doc:`backends_gcp` documentation.
* You can now use Coiled in your own Azure account. Please refer to the
  :doc:`backends_azure` documentation.
* You can now select a ``region`` or ``zone`` when launching clusters in GCP.
* You can now create software environments using Docker images stored in your
  private ECR (AWS), ACR (Azure) or GAR (GCP) container registries, in addition
  to Docker Hub and other registries, by calling 
  ``coiled.create_software_environment(container="<URI>")``.
* Coiled now collects statistical profiling data from your Dask clusters.
  This data is visualized as a flame graph on the Analytics page for
  individual clusters.
* You can now hide/show columns in the Clusters Dashboard. The options are: Id,
  Cluster Name, Created By, Status, Num Workers, Software Environment,
  Cost (current), Cost(total), Last Seen, Backend, Runtime, Spot/Preemptible.
* Improve log filtering for AWS when viewing logs in the Coiled UI.


Documentation
+++++++++++++

* Added a new example on using the :doc:`Dask Snowflake <examples/snowflake>`
  connector.
* Fix link to Coiled's privacy policy in the :doc:`security` page.
* Added new section in the :doc:`gpu` documentation to demonstrate the use how
  of GPUs with the Afar library to run remote commands.


28 September 2021
=================

Fixes
+++++

* Resolve error that was throwing an "Unable to stop cluster" error message in the Clusters
  Dashboard for users using the Azure backend.
* Fix issue with workers not being created when users create a new Cluster using the AWS backend.
* Resolve error that was causing Clusters to shut down immediately upon creation for users using the AWS backend.
* Fix issue that was causing the Cluster Dashboard table to show zero workers count even though the workers were
  created and connected to the scheduler.


Enhancements
++++++++++++

* Add label containing the instance name to notification when running ``coiled.get_notifications()``.


Documentation
+++++++++++++

* Fix typo in CLI command, documentation mentioned ``coiled inspect`` but the right command is ``coiled env inspect``.
* Update :doc:`teams` page to better explain the distinction between Accounts and Teams.
