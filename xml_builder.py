def generate_xml(config):
    return f"""
    <domain type="kvm">
    <name>{config["name"]}</name>
    <uuid>ea58d274-3fb5-4ccb-8e26-7beaddc29c5f</uuid>
    <metadata>
        <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
        <libosinfo:os id="http://debian.org/debian/11"/>
        </libosinfo:libosinfo>
    </metadata>
    <currentMemory unit="KiB">{config["ram_size"] * 1024}</currentMemory>
    <memory unit='KiB'>{config["ram_size"] * 1024}</memory>
    <vcpu placement='static'>{config["cpu_count"]}</vcpu>
    <os>
        <type arch="x86_64" machine="pc-q35-7.2">hvm</type>
        <boot dev="hd"/>
    </os>
    <features>
        <acpi/>
        <apic/>
        <vmport state="off"/>
    </features>
    <cpu mode="host-passthrough" check="none" migratable="on"/>
    <clock offset="utc">
        <timer name="rtc" tickpolicy="catchup"/>
        <timer name="pit" tickpolicy="delay"/>
        <timer name="hpet" present="no"/>
    </clock>
    <on_poweroff>destroy</on_poweroff>
    <on_reboot>restart</on_reboot>
    <on_crash>destroy</on_crash>
    <pm>
        <suspend-to-mem enabled="no"/>
        <suspend-to-disk enabled="no"/>
    </pm>
    <devices>
        <emulator>/usr/bin/qemu-system-x86_64</emulator>
        <disk type="file" device="disk">
        <driver name="qemu" type="qcow2"/>
        <source file="/home/gourav/codes/cloud/assignment1/images/debian.qcow2"/>
        <target dev="vda" bus="virtio"/>
        <address type="pci" domain="0x0000" bus="0x04" slot="0x00" function="0x0"/>
        </disk>
        <controller type="usb" index="0" model="qemu-xhci" ports="15">
        <address type="pci" domain="0x0000" bus="0x02" slot="0x00" function="0x0"/>
        </controller>
        <controller type="pci" index="0" model="pcie-root"/>
        <controller type="pci" index="1" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="1" port="0x10"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x0" multifunction="on"/>
        </controller>
        <controller type="pci" index="2" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="2" port="0x11"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x1"/>
        </controller>
        <controller type="pci" index="3" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="3" port="0x12"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x2"/>
        </controller>
        <controller type="pci" index="4" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="4" port="0x13"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x3"/>
        </controller>
        <controller type="pci" index="5" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="5" port="0x14"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x4"/>
        </controller>
        <controller type="pci" index="6" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="6" port="0x15"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x5"/>
        </controller>
        <controller type="pci" index="7" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="7" port="0x16"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x6"/>
        </controller>
        <controller type="pci" index="8" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="8" port="0x17"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x02" function="0x7"/>
        </controller>
        <controller type="pci" index="9" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="9" port="0x18"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x0" multifunction="on"/>
        </controller>
        <controller type="pci" index="10" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="10" port="0x19"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x1"/>
        </controller>
        <controller type="pci" index="11" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="11" port="0x1a"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x2"/>
        </controller>
        <controller type="pci" index="12" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="12" port="0x1b"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x3"/>
        </controller>
        <controller type="pci" index="13" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="13" port="0x1c"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x4"/>
        </controller>
        <controller type="pci" index="14" model="pcie-root-port">
        <model name="pcie-root-port"/>
        <target chassis="14" port="0x1d"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x03" function="0x5"/>
        </controller>
        <controller type="sata" index="0">
        <address type="pci" domain="0x0000" bus="0x00" slot="0x1f" function="0x2"/>
        </controller>
        <controller type="virtio-serial" index="0">
        <address type="pci" domain="0x0000" bus="0x03" slot="0x00" function="0x0"/>
        </controller>
        <interface type="network">
        <mac address="52:54:00:7a:d0:07"/>
        <source network="default"/>
        <model type="virtio"/>
        <address type="pci" domain="0x0000" bus="0x01" slot="0x00" function="0x0"/>
        </interface>
        <serial type="pty">
        <target type="isa-serial" port="0">
            <model name="isa-serial"/>
        </target>
        </serial>
        <console type="pty">
        <target type="serial" port="0"/>
        </console>
        <channel type="unix">
        <target type="virtio" name="org.qemu.guest_agent.0"/>
        <address type="virtio-serial" controller="0" bus="0" port="1"/>
        </channel>
        <channel type="spicevmc">
        <target type="virtio" name="com.redhat.spice.0"/>
        <address type="virtio-serial" controller="0" bus="0" port="2"/>
        </channel>
        <input type="tablet" bus="usb">
        <address type="usb" bus="0" port="1"/>
        </input>
        <input type="mouse" bus="ps2"/>
        <input type="keyboard" bus="ps2"/>
        <graphics type="spice" autoport="yes">
        <listen type="address"/>
        <image compression="off"/>
        </graphics>
        <sound model="ich9">
        <address type="pci" domain="0x0000" bus="0x00" slot="0x1b" function="0x0"/>
        </sound>
        <audio id="1" type="spice"/>
        <video>
        <model type="virtio" heads="1" primary="yes"/>
        <address type="pci" domain="0x0000" bus="0x00" slot="0x01" function="0x0"/>
        </video>
        <redirdev bus="usb" type="spicevmc">
        <address type="usb" bus="0" port="2"/>
        </redirdev>
        <redirdev bus="usb" type="spicevmc">
        <address type="usb" bus="0" port="3"/>
        </redirdev>
        <memballoon model="virtio">
        <address type="pci" domain="0x0000" bus="0x05" slot="0x00" function="0x0"/>
        </memballoon>
        <rng model="virtio">
        <backend model="random">/dev/urandom</backend>
        <address type="pci" domain="0x0000" bus="0x06" slot="0x00" function="0x0"/>
        </rng>
    </devices>
    </domain>"""
