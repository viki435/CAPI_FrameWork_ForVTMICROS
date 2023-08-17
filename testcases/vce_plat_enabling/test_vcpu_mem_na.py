import yaml
import pprint
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

_logger = logging.getLogger(__name__)

class thread(threading.Thread):
    """Thread class customised for executing workload in VM.
       Also, it returns the result of execution in join method
    """
    def __init__(self, si, vm_name, vm_user_name, vm_passwd, path_to_program, program_arguments):
        threading.Thread.__init__(self)
        #self.content=content
        self.si=si
        self.vm_name = vm_name
        self.vm_user_name = vm_user_name
        self.vm_passwd = vm_passwd
        self.path_to_program = path_to_program
        self.program_arguments = program_arguments
        self._return = None

    def run(self):
        self._return = execute_program_in_vm(self.si, self.vm_name, self.vm_user_name, self.vm_passwd, self.path_to_program, '')

    def join(self):
        threading.Thread.join(self)
        return self._return

class VtCode_Test(BaseContent_Test):
    """
    :avocado: enable
    """

    def setUp(self):
        """
        TODO
        """        
        super(VtCode_Test, self).setUp()

        self.list_esxi_hosts = [
            {
            "platname": self.yaml_configuration['sut']['platform_name'],
            "esxi_host": self.yaml_configuration['sut']['esxi']['ip'],
            "esxi_user": self.yaml_configuration['sut']['esxi']['user'],
            "esxi_password": self.yaml_configuration['sut']['esxi']['password'],
            "vcen_ip": self.yaml_configuration['sut']['vcenter']['ip'],
            "vcen_user": self.yaml_configuration['sut']['vcenter']['user'],
            "vcen_password": self.yaml_configuration['sut']['vcenter']['password'],
            "nfs_datastore_name": self.yaml_configuration['sut']['esxi']['datastores']['nfs']['name'],
            "nfs_share_path": self.yaml_configuration['sut']['esxi']['datastores']['nfs']['nfs_share_path'],
            "vms_names":[                    
                    self.yaml_configuration['sut']['esxi']['vms']['vm1']['vm_name'],
                    #self.yaml_configuration['sut']['esxi']['vms']['vm2']['vm_name'],
                    # self.yaml_configuration['sut']['esxi']['vms']['vm3']['vm_name'],
                ],
            },           
        ]

        self.platforms_checkup(self.list_esxi_hosts)
        time.sleep(10)
        
    def test_vtmicros(self):
        """
        Test Cases: Include description

        :avocado: tags=demo
        """
        fileReadFlag=2
        vm_name = self.yaml_configuration['sut']['esxi']['vms']['vm1']['vm_name']
        print("base vm name is ", vm_name)

        esxi_ip = self.yaml_configuration['sut']['esxi']['ip']
        esxi_user = self.yaml_configuration['sut']['esxi']['user']
        esxi_password = self.yaml_configuration['sut']['esxi']['password']
        esxi_session = SSH(esxi_ip, esxi_user, esxi_password)
        esxi_session.connect()

        vc_ip = self.yaml_configuration['sut']['vcenter']['ip']
        print(vc_ip)
        _logger.info("Vcenter IP address is = %s" % vc_ip)
        vc_user = self.yaml_configuration['sut']['vcenter']['user']
        print(vc_user)
        _logger.info("Vcenter IP address is = %s" % vc_user)
        vc_password =  self.yaml_configuration['sut']['vcenter']['password']
        print(vc_password)
        _logger.info("Vcenter IP address is = %s" % vc_password)


        vm_actions = VM_Actions(esxi_ip, esxi_user, esxi_password)

        DS_path = "/vmfs/volumes/19df80f7-f7c725d3"
        vmx_name = vm_name+".vmx"
        config_file_path = DS_path + '/' + vm_name + '/' + vmx_name
        print("******ViKi******Config File Path is: ", config_file_path)

        esxi_session.scp_remote_to_local(config_file_path)
        location = os.getcwd()
        cmd = 'cp  ' + vmx_name + ' ' +  vmx_name + '.bkp'
        os.system(cmd)

        self.NUM_VCPUS = self.params.get("numvcpus", default = None)
        self.MEM_SIZE = self.params.get("memSize", default = None)
        self.NODE_AFFINITY = self.params.get("nodeAffinity", default = None)
        self.READ_FROM_FILE = self.params.get("readFromFile", default = None)
        self.NUM_OF_VMS = self.params.get("vmCount", default = None)
 
        if (self.READ_FROM_FILE == '0'):
            print("***ViKi***In test_diff_config, NUM_VCPUS = ", self.NUM_VCPUS)
            print("***ViKi***In test_diff_config, MEM_SIZE = ", self.MEM_SIZE)
            print("***ViKi***In test_diff_config, NODE_AFFINITY = ", self.NODE_AFFINITY)
            print("Powering Off Base VM to make sure the cloning happens correctly")
            _logger.info("TestCase.test_demo: init")
            time.sleep(10)
           
            if vm_actions.power_off_vm(vm_name) != 0:
                print("VM powering OFF failed")
                time.sleep(10)
            with open(vmx_name, 'r', encoding='utf-8') as fp_Params:
                data = fp_Params.readlines()
                
            print("***ViKi***Number of VCPUs before updating: ", data[6])
            print("***ViKi***Memory Size before updating", data[7])
            
            lineNumber=0
            affinityFlag=0
            lineNumVCPU=300#Setting the value of line number beyond the size of file
            lineNumMemSize=300
            lineNumNodeAffinity=300
            
            for lineNumber in range(len(data)):
                if ('numvcpus' in data[lineNumber]):
                    print ("Line number matching with numvcpus is: ", lineNumber)
                    lineNumVCPU=lineNumber
                if ('memSize' in data[lineNumber]):
                    print ("Line number matching with memSize is: ", lineNumber)
                    lineNumMemSize=lineNumber
                if ('numa.nodeAffinity' in data[lineNumber]):
                    print("Matching Node Affinity line is found")
                    lineNumNodeAffinity=lineNumber
                    affinityFlag=1
           
            if (affinityFlag == 1):
                print("Matching Affinity line is found, so just replace the value as per command line")
                tempLine_NA=self.NODE_AFFINITY
                data[lineNumNodeAffinity] = "numa.nodeAffinity ="+" "+'"'+tempLine_NA+'"'+"\n"
                print("Setting the Node Affinity to this in the vmx file: ", data[lineNumNodeAffinity])
           
            time.sleep(15)
            tempLine6 = self.NUM_VCPUS
            data[6] = "numvcpus ="+" "+'"'+tempLine6+'"'+"\n"
            
            tempLine7 = self.MEM_SIZE
            data[7] = "memSize ="+" "+'"'+tempLine7+'"'+"\n"#"numvcpus ="+" "+"tempLine7"+"\n"
           
            print("***ViKi***After Updating: ", data[6])
            print("***ViKi***After Updating: ", data[7])
            with open(vmx_name, 'w', encoding='utf-8') as fp_Params:
                fp_Params.writelines(data)
            
            if affinityFlag == 0:
                print ("Node Affinity parameter is not present in the VMX file, so add it at the end")
                with open(vmx_name, 'a') as fp_nodeAffinity:
                    fp_nodeAffinity.write('numa.nodeAffinity = "0"')
                    print("Check if Node Affinity parameter is added by manually opening the local VMX file now")
            
            print("CHECK IF THE VARIABLES ARE UPDATED PROPERLY")
            time.sleep(30)

        if (self.READ_FROM_FILE == '1'):
            print("THE DATA INDICATING TO READ FROM FILE IS: ", self.READ_FROM_FILE)
            print("Read the parameters from file")
            with open("paramsFile.txt", 'r') as fileData:
                onceFlag = 0
                for line in fileData:
                    data = line.split()
                    print(data)
                    print("self.NUM_OF_VMS and data[0] are: ", self.NUM_OF_VMS, data[0])
                    if (self.NUM_OF_VMS == data[0] and onceFlag == 0):
                        self.NUM_VCPUS = data[1]
                        self.MEM_SIZE = data[2]
                        self.NODE_AFFINITY = data[3]
                        print("VCPUs: ", self.NUM_VCPUS)
                        print("MemSize: ", self.MEM_SIZE)
                        print("NodeAffinity: ", self.NODE_AFFINITY)
                        onceFlag = 1
                    if (onceFlag == 1):
                        break
            with open(vmx_name, 'r', encoding='utf-8') as fp_Params_f1:
                data = fp_Params_f1.readlines()
            
            lineNumber_f1=0
            affinityFlag_f1=0
            lineNumVCPU_f1=300#Setting the value of line number beyond the size of file
            lineNumMemSize_f1=300
            lineNumNodeAffinity_f1=300
            
            for lineNumber_f1 in range(len(data)):
                if ('numvcpus' in data[lineNumber_f1]):
                    print ("Line number matching with numvcpus is: ", lineNumber_f1)
                    lineNumVCPU_f1=lineNumber_f1
                if ('memSize' in data[lineNumber_f1]):
                    print ("Line number matching with memSize is: ", lineNumber_f1)
                    lineNumMemSize_f1=lineNumber_f1
                if ('numa.nodeAffinity' in data[lineNumber_f1]):
                    print("Matching Node Affinity line is found")
                    lineNumNodeAffinity_f1=lineNumber_f1
                    affinityFlag_f1=1
           
            if (affinityFlag_f1 == 1):
                print("Matching Affinity line is found, so just replace the value as per command line")
                tempLine_NA_f1=self.NODE_AFFINITY
                data[lineNumNodeAffinity_f1] = "numa.nodeAffinity ="+" "+'"'+tempLine_NA_f1+'"'+"\n"
                print("Setting the Node Affinity to this in the vmx file: ", data[lineNumNodeAffinity_f1])
           
            tempLine6_f1 = self.NUM_VCPUS
            data[6] = "numvcpus ="+" "+'"'+tempLine6_f1+'"'+"\n"
            
            tempLine7_f1 = self.MEM_SIZE
            data[7] = "memSize ="+" "+'"'+tempLine7_f1+'"'+"\n"#"numvcpus ="+" "+"tempLine7_f1"+"\n"
           
            print("***ViKi***After Updating: ", data[6])
            print("***ViKi***After Updating: ", data[7])
            with open(vmx_name, 'w', encoding='utf-8') as fp_Params_f1:
                fp_Params_f1.writelines(data)
            
            if affinityFlag_f1 == 0:
                print ("Node Affinity parameter is not present in the VMX file, so add it at the end")
                with open(vmx_name, 'a') as fp_nodeAffinity_f1:
                    fp_nodeAffinity_f1.write('numa.nodeAffinity = "0"')
                    print("Check if Node Affinity parameter is added by manually opening the local VMX file now")

        time.sleep(10)
        self.log.debug('completed updating vmx file')
        path = os.getcwd() + "/" + vmx_name
        print("path is: ", path)
        esxi_session.scp_local_to_remote(path, config_file_path)
        self.log.debug('completed scp_local_to_remote')
            
        print("Powering Off the VM after configuring the VMX file of template VM")
        if vm_actions.power_off_vm(vm_name) != 0:
            print("VM powering OFF failed")
        time.sleep(10)
        
        if vm_actions.power_on_vm(vm_name) != 0:
            print("VM powering on failed")
        time.sleep(10)
        
        if vm_actions.power_off_vm(vm_name) != 0:
            print("VM powering OFF failed")
        time.sleep(10)
        seqVMs = int(self.NUM_OF_VMS)
        seqVMs = seqVMs-1
        print("The value of seqVMs is: ", seqVMs)
        vms_list = vm_actions.get_VM_names(vm_name, 4, seqVMs)
        print("VMs list before cloning is: ", vms_list)
        
        ymlSeq = int(self.NUM_OF_VMS)
        ymlSeq = ymlSeq + 2
        print("The value of ymlSeq is: ", ymlSeq)
        with open('/root/CAPI_FrameWork_ForVTMICROS/testcases/vce_plat_enabling/create_fedora_VMs.yml', 'r') as file:
            prime_service = yaml.safe_load(file)
        prime_service[0]["tasks"][0]["with_sequence"] = "4-"+str(ymlSeq)#Since the sequence starts with 4
        pprint.pprint(prime_service[0]["tasks"][0]["with_sequence"])
        time.sleep(5)
        with open('/root/CAPI_FrameWork_ForVTMICROS/testcases/vce_plat_enabling/create_fedora_VMs.yml', 'w+') as json_file:
            yaml.dump(prime_service, json_file)
            time.sleep(5)
            prime_service = yaml.safe_load(json_file)

        print("Check the YML_2 file if it is updated properly")
        time.sleep(20)
        
		#If the VMs are already there, then even if we calling this cloning of VMs, it will not take into effect
        _logger.info("Calling ansible script")
        os.system("ansible-playbook /root/CAPI_FrameWork_ForVTMICROS/testcases/vce_plat_enabling/create_fedora_VMs.yml")

        for VM in vms_list:
            vm_actions.power_off_vm(VM)
            time.sleep(10)

        #*************************************************************************
        # Modifying the VMX files of each VM
        #*************************************************************************
		
        DS_path = "/vmfs/volumes/19df80f7-f7c725d3"
        vmNameArray = []
        vmNameArray = [0 for k in range(30)]
        vmxNameArray = []
        vmxNameArray = [0 for k in range(30)]
        vmPathArray = []
        vmPathArray = [0 for k in range(30)]
        for index in range(seqVMs):
            print("index is: ", index)
            vmNameArray[index+4]="SJ_WithUbuntu_VTMicros_"+str(index+4)
            vmxNameArray[index+4]=vmNameArray[index+4]+".vmx"
            vmPathArray[index+4]=DS_path+'/'+vmNameArray[index+4]+'/'+vmxNameArray[index+4]
            print("VMX PATH IS: ")
            esxi_session.scp_remote_to_local(vmPathArray[index+4])
            location = os.getcwd()
            cmd = 'cp  ' + vmxNameArray[index+4] + ' ' +  vmxNameArray[index+4] + '.bkp'
            os.system(cmd)

            with open(vmxNameArray[index+4], 'r', encoding='utf-8') as fp_NA:
                data_NA = fp_NA.readlines()
                for lineNum_NA in range(len(data_NA)):
                    if ('numa.nodeAffinity' in data_NA[lineNum_NA]):
                        print("Matching Node Affinity line is found")
                        lineNumNodeAffinity=lineNum_NA
                        tempLine_NA=index%3
                        data_NA[lineNumNodeAffinity] = "numa.nodeAffinity ="+" "+'"'+str(tempLine_NA)+'"'+"\n"
                        print("***Setting the Node Affinity to this in the vmx file: ", data[lineNumNodeAffinity])

            with open(vmxNameArray[index+4], 'w', encoding='utf-8') as fp_NA_V1:
                fp_NA_V1.writelines(data_NA)
            
            time.sleep(10)
            self.log.debug('completed updating the local VM vmx file')
            path = os.getcwd() + "/" + vmxNameArray[index+4]
            print("path is: ", path)
            esxi_session.scp_local_to_remote(path, vmPathArray[index+4])
            self.log.debug('completed scp_local_to_remote')
            print("CHECK IF THE VMX FILE OF VM IS UDPATED PROPERLY")
            print("END OF FOR LOOP AND ALL THE VMX FILES ARE UPDATED - CHECK ONCE")
        
        time.sleep(100)
        

        for VM in vms_list:
            vm_actions.power_on_vm(VM)
            time.sleep(10)
        
        vms_list = vm_actions.get_VM_names(vm_name, 4, seqVMs)#name, vm starting id, number of VMs
        vms_list.append(vm_name)
        print("Vms list - initial is ", vms_list)

        print("Vms list is ", vms_list)
        time.sleep(10)
        for VM in vms_list:
            print("VM name to power ON",VM)
            if vm_actions.power_on_vm(VM) != 0:
                self.fail('powering on VM failed in iteration')
                
        _logger.info('VM Power-ON - Command Completed (machine is booting)')
        
        time.sleep(10)
        vm_username = self.yaml_configuration['sut']['esxi']['vms']['vm1']['vm_username']
        vm_password = self.yaml_configuration['sut']['esxi']['vms']['vm1']['vm_password']

        si = SmartConnectNoSSL(host=esxi_ip, user=esxi_user, pwd=esxi_password, port=443)
        for VM in vms_list:
            print("vmname inside loop", VM)
            upload_file_to_vm(si,esxi_ip,VM,vm_username,vm_password,"/home/root1/vtmicros", '/root/CAPI_FrameWork_ForVTMICROS/vtmicros')        
            time.sleep(20)
            upload_file_to_vm(si,esxi_ip,VM,vm_username,vm_password,"/home/root1/inputFile.config", '/root/CAPI_FrameWork_ForVTMICROS/inputFile.config')        
            time.sleep(10)
            cmd_chng_permission = '777 vtmicros'
            cmd_chng_permission_1 = '777 inputFile.config'

            execute_program_in_vm(si, VM, vm_username, vm_password, "/usr/bin/chmod", cmd_chng_permission)  
            execute_program_in_vm(si, VM, vm_username, vm_password, "/usr/bin/chmod", cmd_chng_permission_1)

        _logger.info("establish SSH connection")       
        
        cmd_to_vm_session = './vtmicros'
        _logger.info("Executing vtmicros...")
            
        thread_list = []
        for VM in vms_list:
                output = thread(si, VM, vm_username, vm_password, '/home/root1/vtmicros', cmd_to_vm_session)
                thread_list.append(output)
    
        for i in range(0,len(thread_list)):
            thread_list[i].start()

        for i in range(0,len(thread_list)):
            rval = thread_list[i].join()
            print("Returned Value for script execution in VM {} = {}".format(i, rval))
            if rval != 0 :
                print("Script execution failed in VM {}".format(i+1))
                return -1
        
        time.sleep(20*1)

        for VM in vms_list:
            download_file_from_vm(si, esxi_ip, VM, vm_username, vm_password, '/home/root1/output.txt', "/root/CAPI_FrameWork_ForVTMICROS/output_"+ VM +".txt", port_no=443)
            time.sleep(10)

        for VM in vms_list:
            cmd_remv = ' -rf output.txt'
            execute_program_in_vm(si, VM, vm_username, vm_password, "/usr/bin/rm", cmd_remv)
        time.sleep(20)

        print("Giving 1 minute 40 seconds delay for just waiting at the end of execution")
        time.sleep(100)#Giving 1 minute 40 seconds delay for just waiting at the end of execution

        _logger.info("TestCase.test_demo: completed")
