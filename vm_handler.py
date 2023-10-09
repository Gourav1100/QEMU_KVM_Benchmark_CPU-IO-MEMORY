import subprocess
import libvirt
import os
from time import time, sleep
from xml_builder import generate_xml
import json

_PASSWORD = "debian"
WORK_DIR = "/media/G/Codes/cloud/assignment1"
_TARGET_DIR = f"{WORK_DIR}/images"
_TARGET_NAME = "debian.qcow2"
_CONF = {
    "": "debian-12",
    "o": f"{_TARGET_DIR}/{_TARGET_NAME}",
    "format": "qcow2",
    "root-password": f"password:{_PASSWORD}",
    "install": "sysbench",
    "size": "8G",
    "firstboot-command": '"apt install -y --fix-missing qemu-guest-agent && systemctl enable qemu-guest-agent && systemctl start qemu-guest-agent"',
}

VM_CONFIGS = {
    "low": {
        "name": "debian_low",
        "cpu_count": 2,
        "ram_size": 1024,
        "image_path": f"{_TARGET_DIR}/debian.qcow2",
    },
    "medium": {
        "name": "debian_medium",
        "cpu_count": 4,
        "ram_size": 4096,
        "image_path": f"{_TARGET_DIR}/debian.qcow2",
    },
    "high": {
        "name": "debian_high",
        "cpu_count": 8,
        "ram_size": 8192,
        "image_path": f"{_TARGET_DIR}/debian.qcow2",
    },
}


def get_command():
    args = ""
    for key in _CONF:
        if key == "":
            args += f"{_CONF[key]}"
        else:
            args += f" --{key} {_CONF[key]}"
    return f"virt-builder {args}"


def build_vm():
    if _TARGET_NAME not in os.listdir(_TARGET_DIR):
        print("Building VM")
        subprocess.run(get_command(), shell=True)
        print("Copying testing software")
        subprocess.run(
            f"virt-copy-in -a {_TARGET_DIR}/{_TARGET_NAME} {WORK_DIR}/test_io/* /",
            shell=True,
        )
        print("done")
    else:
        print("Image already exists, skipping.")


def run_vm(level):
    if level not in VM_CONFIGS.keys():
        print("invalid configuration")
        return
    begin = time() * 1000
    print("Connecting to QEMU")
    connection = libvirt.open("qemu:///system")
    print("Creating VM")
    connection.createXML(generate_xml(VM_CONFIGS[level]))
    ping_args = {
        "execute": "guest-exec",
        "arguments": {
            "path": "/usr/bin/echo",
            "arg": ["foo"],
            "capture-output": True,
        },
    }
    ping_jsonified = json.dumps(ping_args)
    ping_command = (
        f"sudo virsh qemu-agent-command {VM_CONFIGS[level]['name']} '{ping_jsonified}'"
    )
    process = (
        subprocess.run(
            ping_command,
            shell=True,
            capture_output=True,
        )
        .stdout.decode("utf-8")
        .split("\n")[0]
    )
    timeout = 6
    while timeout and not len(process):
        print(
            f"waiting for vm to boot (remaining retries: {timeout}). Retrying in 10 seconds..."
        )
        sleep(10.0)
        process = (
            subprocess.run(
                ping_command,
                shell=True,
                capture_output=True,
            )
            .stdout.decode("utf-8")
            .split("\n")[0]
        )
        timeout -= 1
    if not timeout:
        raise Exception("VM did not start")
    print(process)
    end = time() * 1000
    print("VM created.")
    connection.close()
    print(
        f"""VM '{VM_CONFIGS[level]["name"]}' created and started. time taken: {end - begin} seconds"""
    )


def stop_vm(level):
    if level not in VM_CONFIGS.keys():
        print("invalid configuration")
        return
    begin = time() * 1000
    print("Connecting to QEMU")
    connection = libvirt.open("qemu:///system")
    print("Searching for VM")
    domain = connection.lookupByName(VM_CONFIGS[level]["name"])
    print("Shutting down VM")
    try:
        domain.destroy()
        end = time() * 1000
        print(
            "VM '{}' has been forcefully destroyed. time taken: {} seconds".format(
                VM_CONFIGS[level]["name"], end - begin
            )
        )
    except libvirt.libvirtError as e:
        print(
            "Error while forcefully destroying VM '{}': {}".format(
                VM_CONFIGS[level]["name"], e
            )
        )

    connection.close()
