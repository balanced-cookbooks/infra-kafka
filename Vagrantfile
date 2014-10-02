# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = 'precise64'
  config.hostmanager.enabled = true # Must install: vagrant plugin install vagrant-hostmanager

  # zookeeper node to manage the cluster
  config.vm.define 'zk1' do |node|
    node.vm.network :private_network, :ip => '10.20.1.10'
    config.vm.host_name = 'zk1'
    config.vm.network 'forwarded_port', guest: 2181, host: 2181
    config.vm.provision :ansible do |ansible|
      ansible.playbook = './tests/zookeeper/vagrant-ansible.yml'
      ansible.extra_vars = {
          ansible_ssh_user: 'vagrant',
          sudo: true,
      }
      ansible.groups = {
          'zookeeper' => ['zk1', 'zk2', 'zk3'],
      }

      ansible.host_key_checking = false
      #ansible.verbose = 'vvvv'
      #ansible.hosts = 'all'
    end
  end

  # kafka nodes
  [1,2,3].each do |id|
    config.vm.define "kafka#{id}" do |node|
      config.vm.network 'forwarded_port', guest: 9092, host: 9092 + id
      config.vm.provider 'virtualbox' do |vb|
        vb.customize ['modifyvm', :id, '--memory', '1536'] # Java fails to start with less memory, copy to rest of nodes if needed
      end
      node.vm.network :private_network, :ip => "10.20.1.1#{id}"
      config.vm.host_name = "kafka#{id}"
    end
  end

  # provisioning node
  config.vm.provision :ansible do |ansible|
    ansible.playbook = './vagrant-ansible.yml'
    ansible.extra_vars = {
        ansible_ssh_user: 'vagrant',
        sudo: true
    }
    ansible.host_key_checking = false
    ansible.groups = {
      'kafka-vagrant' => ['kafka1', 'kafka2', 'kafka3'],
    }
    #ansible.verbose = 'vvvv'
    #ansible.hosts = 'all'
  end


end
