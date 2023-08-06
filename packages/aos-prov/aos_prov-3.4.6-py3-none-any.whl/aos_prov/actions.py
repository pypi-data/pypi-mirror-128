#
#  Copyright (c) 2018-2021 Renesas Inc.
#  Copyright (c) 2018-2021 EPAM Systems Inc.
#
import time

from aos_prov.command_provision import run_provision
from aos_prov.command_vm import new_vm, start_vm, delete_provisioning_ports
from aos_prov.utils.user_credentials import UserCredentials

from aos_prov.command_vm import delete_provisioning_ports
from aos_prov.communication.cloud.cloud_api import CloudAPI


def create_new_unit(vm_name):
    uc = UserCredentials(cert_file_path=None, key_file_path=None, pkcs12=args.pkcs)
    cloud_api = CloudAPI(uc)
    cloud_api.check_cloud_access()
    vm_port = new_vm(vm_name)
    start_vm(vm_name)
    time.sleep(10)
    run_provision(f'127.0.0.1:{vm_port}', cloud_api, reconnect_times=20)
    delete_provisioning_ports(vm_name)
