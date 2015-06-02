# -*- mode: ruby -*-
# vi: set ft=ruby sw=2 :

# This requires Vagrant 1.6.2 or newer (earlier versions can't reliably
# configure the Fedora 20 network stack).
Vagrant.require_version ">= 1.6.2"

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

ENV['VAGRANT_DEFAULT_PROVIDER'] = 'virtualbox'

$runner_vms = 2
vms = (1..$runner_vms).map{ |a| "runner-#{a}" } << 'master'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = ENV['BOX_URL'] || "ubuntu/trusty64"

  if Vagrant.has_plugin?("vagrant-cachier")
    config.cache.scope = :box
  end

  vms = (1..$runner_vms).map{ |a| "runner-#{a}" } << 'master'

  vms.each_with_index do |i, x|
    config.vm.define vm_name = i do |config|
      config.vm.network :private_network, :ip => "172.16.160.#{x+10}"
      config.vm.hostname = vm_name
      config.vm.provider "virtualbox" do |v|
        v.memory = 2048
      end
      # allow root to SSH into the machines the same as ubuntu
      config.vm.provision :shell, inline: 'cat /vagrant/insecure_private_key.pub >> /root/.ssh/authorized_keys'
      config.vm.provision :shell, inline: 'cp /vagrant/insecure_private_key /root/.ssh/id_rsa'
      config.vm.provision :shell, inline: 'chmod 600 /root/.ssh/id_rsa'
      config.vm.provision :shell, inline: 'cp /vagrant/insecure_private_key.pub /root/.ssh/id_rsa.pub'
      config.vm.provision :shell, inline: 'chmod 600 /root/.ssh/id_rsa.pub'
    end
  end
end