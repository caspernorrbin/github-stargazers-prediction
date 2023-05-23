# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys, random, re
import inspect
from os import environ as env

from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "ssc.small"
private_net = "UPPMAX 2023/1-1 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
image_name = "Ubuntu 22.04 - 2023.01.07"

identifier = random.randint(1000,9999)

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
                                #project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print ("user authorization completed.")

image = nova.glance.find_image(image_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

#print("Path at terminal when executing this file")
#print(os.getcwd() + "\n")
cfg_file_path =  os.getcwd()+'/node-cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata_prod = open(cfg_file_path)
else:
    sys.exit("node-cloud-cfg.txt is not in current working directory")

secgroups = ['default']

print ("Creating instances ... ")
instance_node = nova.servers.create(name="grp6_node_server_with_docker_"+str(identifier), image=image, flavor=flavor>
inst_status_prod = instance_node.status

print ("waiting for 10 seconds.. ")
time.sleep(10)

while inst_status_node == 'BUILD' or inst_status_node == 'BUILD':
    print ("Instance: "+instance_node.name+" is in "+inst_status_node+" state, sleeping for 5 seconds more...")
    time.sleep(5)
    instance_node = nova.servers.get(instance_node.id)
    inst_status_node = instance_node.status

ip_address_node = None
for network in instance_node.networks[private_net]:
    if re.match('\d+\.\d+\.\d+\.\d+', network):
        ip_address_node = network
        break
if ip_address_node is None:
    raise RuntimeError('No IP address assigned!')

print ("Instance: "+ instance_node.name +" is in " + inst_status_node + " state" + " ip address: "+ ip_address_node)