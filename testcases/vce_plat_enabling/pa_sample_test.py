from avocado import Test
from common.test_base import BaseContent_Test
from utils.vm_utils import VM_Actions
from utils.ssh_utils import SSH
from utils.pyvmomi_library import execute_program_in_vm, upload_file_to_vm, download_file_from_vm
from pyVim.connect import SmartConnectNoSSL
import threading
import pprint
import avocado
import logging
import time
import os
import subprocess

##from avocado.utils import ssh
##import os 
##import re
##import time
##from avocado import Test
##import sys
##import subprocess
##from time import sleep
##from scp import SCPClient
##from config_vtd import config_host1_VM_name, iperf_opr_time, nic_dr_passthru, ssd_pci, ssd_pci_1, DATASTORE_PATH_1, DATASTORE_PATH_2, nic_pci, nic_passthru_dev_id, nic_pci_1, nic_passthru_dev_id_1, Config_host2_VM_name, static_ip_add, Config_iometer_VM_name, Config_windows_VM_name, Config_res_VM_name, IADX_DRIVER_PATH,DLB_SRIOV_DRIVER_PATH,KERNEL_VAR, LEGACY_MODE, SCALABLE_MODE, Config_VM_name, Config_ssd_VM_name, Config_VM2_name, Config_iperf_VM_name, REMOTE_ESXI_IP, REMOTE_ESXI_IP_1, ESXI_USERNAME, ESXI_PASSWORD, vm_username, vm_passwd, vc_name, vc_username, vc_password, Config_vmotion_VM_name, vm_win_passwd, vm_win_username
sys.path.append("/home/reddyr/TestCAPIAutomation/temp_CAPI_Automation/utils/vm_utils/")
##sys.path.append("/shared_data/drivers.io.vmware.validation.test-automation-framework/Testcases/VTD/")
##sys.path.append("/shared_data/drivers.io.vmware.validation.test-automation-framework/Testcases/DLB/")
##sys.path.append("/shared_data/drivers.io.vmware.validation.test-automation-framework/generic_utilities")
#from remote_utility import ssh_connect, ssh_cmd_execute, remote_reboot, scp_remote_to_local
#from vdev_add_lib import add_vdev_to_vm, remove_vdev_from_vm
#from upd_kernel_options import get_bootcfg, set_boot_option
##from upd_vmkernel_module_utility import module_comp_install_load, module_unload_comp_remove, get_module_name
##
##from VTD_Mode import IOMMU_Legacy_Status, IOMMU_Scalable_Status, get_VM_names
##from L3_Passthru_Lib import L3_test_exec_func, L3_test_clean_func
##sys.path.append("/shared_data/drivers.io.vmware.validation.test-automation-framework/vmware_utilities")
##from pyvmomi_library import execute_program_in_vm
##
##from L4_VM_Test_lib import L4_test_config_func, L4_test_clean_func,pci_passthru_config_func, pci_passthru_clean_func, lspci_check,get_vf_ids
###from config_vtd import Config_iometer_VM_name, Config_windows_VM_name, Config_res_VM_name, IADX_DRIVER_PATH,DLB_SRIOV_DRIVER_PATH,KERNEL_VAR, LEGACY_MODE, SCALABLE_MODE, Config_VM_name, Config_ssd_VM_name, Config_VM2_name, Config_iperf_VM_name, REMOTE_ESXI_IP, REMOTE_ESXI_IP_1, ESXI_USERNAME, ESXI_PASSWORD, vm_username, vm_passwd, vc_name, vc_username, vc_password, Config_vmotion_VM_name, vm_win_passwd, vm_win_username
##
##from Pyvmomi_lib import find_and_clone_vm, power_on_vm, power_off_vm
###from dlb_lib import get_all_vfs, get_all_pfs
##
##from vcsa_operations import vmotion, enable_vmkernel_service
##
##from pyvmomi_library import execute_program_in_vm, upload_file_to_vm, download_file_from_vm
##from vmware_sriov_utilities import check_vf_connected, add_vf_to_vm, del_vf_from_vm, sriov_enable, sriov_disable
##
##sys.path.append("/shared_data/drivers.io.vmware.validation.test-automation-framework/generic_utilities")
##from vm_operations import vmoperations
##from threading import Thread
##from pyVim.connect import SmartConnectNoSSL
##from file_io import input_output_operations_vms, prvip_input_output_operations_vms
##
##from esxi_vm_utility import vm_suspend, vm_suspend_resume, vm_resume, iperf_verifcation, get_vm_id, list_vms, update_static_ip, create_vmkernel_log, copy_vmkernel_log, copy_vm_log, copy_boot_log
##
##global vmops
##vmops = vmoperations(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD)
##vmops_1 = vmoperations(REMOTE_ESXI_IP_1, ESXI_USERNAME, ESXI_PASSWORD)

class sample(Test):
    
    def test_getVM_powercli(self):
        """
        Test to execute 18014072501 Virtualization - VMware - Cores per Socket
        VMware multicore virtual CPU support lets you control the number of cores per virtual CPU in a virtual machine. This capability lets operating systems with socket restrictions use more of the host CPU's cores.
        Precondition: VM should be installed with any OS like Fedora, Rockylinux and it should be in powered OFF state.
        Navigate Hardware tab and change number VCPUs and coresperSockets for VM
        Power ON VM and capture the VCPUs and CoresperSocket and compare with intial set values
        repeat this step for mulitple values.
        Capture vmkernel, boot and vmware logs when test fails
        If there is failure in any of the above operations, test fails
        """   
		
		###vm_actions = VM_Actions(esxi_ip, esxi_user, esxi_password)
		###
        ###VMs = vm_actions.get_VM_names(Config_VM_name, 1, 1)       
        ###list_value=['4','16', '2', '12']
        ###l=len(list_value)
        ###for i in range(0,l,2):
        ###    for VM in VMs:
        ###        if power_off_vm([VM],REMOTE_ESXI_IP) != 0:
        ###            copy_vmkernel_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
        ###            copy_boot_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
        ###            copy_vm_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD,VM, DATASTORE_PATH_1,'18014072501')
        ###            self.fail('powering off VM failed')
        ###    sleep(10)
        ###    
        ###    p = subprocess.Popen(['pwsh', './get_vm_deatails.ps1', REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, Config_VM_name, list_value[i], list_value[i+1]])
        ###    p.wait()  

		vms_list = vm_actions.get_VM_names(vm_name, 4, 2)#name, vm starting id, number of VMs
        vms_list.append(vm_name)
        list_value=['4','16', '2', '12']
        l=len(list_value)
        for i in range(0,l,2):
                for VM in vms_list:
                    p = subprocess.Popen(['pwsh', './get_vm_deatails.ps1', REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, vm_name, list_value[i], list_value[i+1]])
                    p.wait()
        sleep(30);


        ###    for VM in VMs:
        ###        if power_on_vm([VM],REMOTE_ESXI_IP) != 0:
        ###            copy_vmkernel_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
        ###            copy_boot_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
        ###            copy_vm_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD,VM, DATASTORE_PATH_1,'18014072501')
        ###            self.fail('powering on VM failed')   
        ###    sleep(60)

            vm_ip = vmops.get_ip(vms_list[0])
            print("IP address of the virtual machine", vm_ip)
            #esxi_session = ssh_connect(vm_ip, vm_username, vm_passwd)
            cmd1 = "| grep 'socket' > /root/cpus_info.txt"
            cmd2 = '/proc/cpuinfo | grep processor | wc -l >> /root/cpus_info.txt'
            #cmd3 = 'cat /proc/cpuinfo | grep "physical id" | sort -u | wc -l
            sleep(60)
            si = SmartConnectNoSSL(host=REMOTE_ESXI_IP, user=ESXI_USERNAME, pwd=ESXI_PASSWORD, port=443)
                   
            ###execute_program_in_vm(si, Config_VM_name, vm_username, vm_passwd, "/bin/lscpu", cmd1)
            ###execute_program_in_vm(si, Config_VM_name, vm_username, vm_passwd, "/bin/cat", cmd2)
            ###download_file_from_vm(si, REMOTE_ESXI_IP, Config_VM_name, vm_username, vm_passwd, '/root/cpus_info.txt', "/shared_data/drivers.io.vmware.validation.test-automation-framework/Testcases/Platform/cpus_info.txt", port_no=443)
            ####corespersock_info=ssh_cmd_execute(esxi_session, cmd1, '', 30)
            ###sleep(10)

            with open(r'/home/reddyr/TestCAPIAutomation/temp_CAPI_Automation/testcases/vce_plat_enabling/cpus_info.txt', 'r') as fo:
                readline=fo.readlines()
                for linenumber in range(len(readline)):
                    if('socket' in readline[linenumber]):
                        socket_list = readline[linenumber].split()
                        coresper_sock=socket_list[-1]
                        print(coresper_sock)
                        process_info=readline[linenumber+1]
                        print(process_info)
                fo.close()

            # corespersock_info=corespersock_info.strip()
            # corespersock_info = corespersock_info.split(' ')
            # coresper_sock = corespersock_info[-1]
            # print("*****cores per socket infor after****", coresper_sock )         
            # process_info=ssh_cmd_execute(esxi_session, cmd2, '', 30)
            # sleep(10)
            # process_info=process_info.rstrip()
            # print("*******processors infor********", process_info)
            # print(process_info.rstrip())
            # print("cores per scoket value ", coresper_sock)
            # print("no of cpus", process_info) 
                        
            ###if(coresper_sock != list_value[i]) :
            ###    copy_vmkernel_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
            ###    copy_boot_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
            ###    copy_vm_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD,VMs[0], DATASTORE_PATH_1,'18014072501')
            ###    self.fail('corespersockets are not matching')
            ###            
            ###if(int(process_info) != int(list_value[i+1])) :
            ###    copy_vmkernel_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
            ###    copy_boot_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD, DATASTORE_PATH_1, '18014072501')
            ###    copy_vm_log(REMOTE_ESXI_IP, ESXI_USERNAME, ESXI_PASSWORD,VMs[0], DATASTORE_PATH_1,'18014072501')
            ###    self.fail('cpus are not matching')        
            ###else:
            ###    print("both are matching completed")
            
        self.log.info('cores per scoket test completed successfully') 
