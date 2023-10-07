# QEMU/KVM Benchmark

This is a QEMU and KVM benchmark script with various vm configurations.
There are 3 configurations -

- LOW (1GiB, 2 CPU)
- MEDIUM (4GiB, 4 CPU)
- HIGH (8GiB, 8 CPU)

Note - More configurations can be added from vm_handler.py

## How to run

1. Requirements -
   - KVM
   - QEMU
   - libvirt-python
   - sysbench
2. Run -
   ```sh
   sudo apt install sysbench
   mkdir images
   mkdir test_io
   cd test_io
   sysbench fileio prepare
   cd ..
   python main.py
   ```

Note - This is a project to my cloud computing course.
