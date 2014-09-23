infra-kafka
===============

Installs and configures a kafka cluster

Testing
======

```
vagrant plugin install vagrant-hostmanager
vagrant up
```
Expects a running zookeeper cluster at the following 3 nodes (zk1.vm:2181, zk2.vm:2181, zk3.vm:2181)
