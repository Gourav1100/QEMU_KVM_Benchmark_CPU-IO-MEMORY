import libvirt
import json
import subprocess
from vm_handler import VM_CONFIGS, WORK_DIR
from time import sleep, time
from base64 import b64decode

""""
cd /test_io
sysbench cpu --threads=8 run > cpu_{vm_name}.log
sysbench memory --threads=8 run > memory_{vm_name}.log
sysbench fileio --file-test-mode=seqrewr --threads=8 run > io_{vm_name}_seqrewr.log
sysbench fileio --file-test-mode=rndrw --threads=8 run > io_{vm_name}_rndrw.log
"""


def run_test(level):
    print("Setting up config")
    vm_name = VM_CONFIGS[level]["name"]
    print("generating testing command")
    qemu_agent_command_list_names = [
        f"cpu_{level}.log",
        f"memory_{level}.log",
        f"io_{level}_seqrewr.log",
        f"io_{level}_rndrw.log",
    ]
    qemu_agent_command_list = [
        {
            "execute": "guest-exec",
            "arguments": {
                "path": "/usr/bin/sysbench",
                "arg": ["cpu", f"--threads={VM_CONFIGS[level]['cpu_count']}", "run"],
                "capture-output": True,
            },
        },
        {
            "execute": "guest-exec",
            "arguments": {
                "path": "/usr/bin/sysbench",
                "arg": ["memory", f"--threads={VM_CONFIGS[level]['cpu_count']}", "run"],
                "capture-output": True,
            },
        },
        {
            "execute": "guest-exec",
            "arguments": {
                "path": "/usr/bin/sysbench",
                "arg": [
                    "fileio",
                    "--file-test-mode=seqrewr",
                    f"--threads={VM_CONFIGS[level]['cpu_count']}",
                    "run",
                ],
                "capture-output": True,
            },
        },
        {
            "execute": "guest-exec",
            "arguments": {
                "path": "/usr/bin/sysbench",
                "arg": [
                    "fileio",
                    "--file-test-mode=rndrw",
                    f"--threads={VM_CONFIGS[level]['cpu_count']}",
                    "run",
                ],
                "capture-output": True,
            },
        },
    ]
    index = 0
    for qemu_agent_command in qemu_agent_command_list:
        qemu_agent_command_json = json.dumps(qemu_agent_command)
        begin = time() * 1000
        virsh_command = (
            "sudo virsh -c qemu:///system qemu-agent-command {} '{}'".format(
                vm_name, qemu_agent_command_json
            )
        )
        print("running test")
        print(f"Running: {virsh_command}")
        try:
            process = subprocess.run(virsh_command, shell=True, capture_output=True)
            print(process)
            result = json.loads(
                process
                .stdout.decode("utf-8")
                .split("\n")[0]
            )
            status_command = json.dumps(
                {
                    "execute": "guest-exec-status",
                    "arguments": {"pid": result["return"]["pid"]},
                }
            )
            status_command = (
                "sudo virsh -c qemu:///system qemu-agent-command {} '{}'".format(
                    vm_name, status_command
                )
            )
            print(f"Running: {status_command}")
            status_response = json.loads(
                subprocess.run(status_command, shell=True, capture_output=True)
                .stdout.decode("utf-8")
                .split("\n")[0]
            )
            while status_response["return"]["exited"] is not True:
                print("waiting for result. Retrying in 5 seconds...")
                sleep(5.0)
                status_response = json.loads(
                    subprocess.run(status_command, shell=True, capture_output=True)
                    .stdout.decode("utf-8")
                    .split("\n")[0]
                )
            print(b64decode(status_response["return"]["out-data"]).decode("utf-8"))
            time_taken = (time() * 1000) - begin
            print(f"time taken - {time_taken}")
            print(
                f"Writing to {WORK_DIR}/results/{qemu_agent_command_list_names[index]}"
            )
            with open(
                f"{WORK_DIR}/results/{qemu_agent_command_list_names[index]}", "w"
            ) as file:
                file.write(
                    f"{b64decode(status_response['return']['out-data']).decode('utf-8')}\ntime taken - {time_taken}"
                )
                file.close()
            print("done")
            index += 1
        except libvirt.libvirtError as e:
            print("Error executing command: {}".format(e))
