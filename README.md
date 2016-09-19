# Overview

This is the base layer for charms that wish to connect to a core
[Hadoop cluster][hadoop-core].  [Including this layer][building]
provides and manages the relation to [hadoop-plugin][], and all your reactive
charm needs to do is respond to one or more of the states listed below.

The plugin services provides the appropriate Hadoop libraries for the cluster,
and sets up the standard Hadoop config files in `/etc/hadoop/conf`.

# Usage

To create a charm layer using this base layer, you need only include it in
a `layer.yaml` file:

```yaml
includes: ['layer:hadoop-client']
```

This will fetch this layer from [interfaces.juju.solutions][] and incorporate
it into your charm layer.  You can then add handlers under the `reactive/`
directory.  Note that **any** file under `reactive/` will be expected to
contain handlers, whether as Python decorated functions or [executables][non-python]
using the [external handler protocol][].


# Reactive States

This layer, via the [hadoop-plugin][] interface, will set the following states:

  * **`hadoop.hdfs.ready`**  The Hadoop cluster has indicated that HDFS is ready
    to store data.  Handlers reacting to this state will be passed an instance
    of the [hadoop-plugin][] class, and can use the following methods to access
    information about HDFS:

    * `hadoop.namenodes()` A list of one or two NameNode addresses.
    * `hadoop.hdfs_port()` The port on which the NameNodes are listening.

  * **`hadoop.yarn.ready`**  The Hadoop cluster has indicated that Yarn is ready
    to process data.  Handlers reacting to this state will be passed an instance
    of the [hadoop-plugin][] class, and can use the following methods to access
    information about Yarn:

    * `hadoop.resourcemanagers()` A list of one or two ResourceManager addresses.
    * `hadoop.yarn_port()` The port on which the ResourceManagers are listening.
    * `hadoop.yarn_hs_ipc_port()` The IPC port for the Yarn HistoryServer.
    * `hadoop.yarn_hs_http_port()` The HTTP port for the Yarn HistoryServer.

  * **`hadoop.ready`**  The Hadoop cluster has indicated that both HDFS and Yarn
    are ready.  This is a combination of the previous two states, and also provides
    an instance upon which any of the previously mentioned methods can be called.

An example using these states would be:

```python
@when('hadoop.ready')
def configure_service(hadoop):
    update_config(
        hadoop.namenodes(), hadoop.hdfs_port(),
        hadoop.resourcemanagers(), hadoop.yarn_port())
    restart_service()
```


# Layer Configuration

This layer supports the following options, which can be set in `layer.yaml`:

  * **packages**  A list of system packages to be installed when Hadoop is
    being installed.

  * **groups**  A list of system groups to be created when Hadoop is being
    configured.

  * **users**  A list of system users to be created when Hadoop is being
    configured.

  * **dirs**  A mapping of directories to be created when Hadoop is being
    configured.  Each entry should contain the following keys:

    * **path**  Absolute directory path.
    * **perms**  Octal permissions.
    * **owner**  User name to own directory.
    * **group**  Name of group for directory.

An example `layer.yaml` using these options might be:

```yaml
includes: ['layer:hadoop-client']
options:
  hadoop-client:
    groups: [spark]
    users: [spark]
    dirs:
      spark_home:
        path: /var/lib/spark
        perms: 0755
        owner: spark
        group: spark
```


# Actions

This layer currently does not define any actions.


[hadoop-core]: https://jujucharms.com/hadoop-processing/
[building]: https://jujucharms.com/docs/devel/authors-charm-building
[interfaces.juju.solutions]: http://interfaces.juju.solutions/
[non-python]: https://pythonhosted.org/charms.reactive/#non-python-reactive-handlers
[external handler protocol]: https://pythonhosted.org/charms.reactive/charms.reactive.bus.html#charms.reactive.bus.ExternalHandler
[`data_changed`]: https://pythonhosted.org/charms.reactive/charms.reactive.helpers.html#charms.reactive.helpers.data_changed
[hadoop-plugin]: https://github.com/juju-solutions/interface-hadoop-plugin
