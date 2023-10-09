import vm_handler
import vm_tester

levels = list(vm_handler.VM_CONFIGS.keys())
LOW = levels[0]
MEDIUM = levels[1]
HIGH = levels[2]
iter_levels = [LOW, MEDIUM, HIGH]


def main():
    for level in iter_levels:
        print(f"Current config - ({level})")
        print(vm_handler.VM_CONFIGS[level])
        vm_handler.build_vm()
        try:
            vm_handler.run_vm(level)
            vm_tester.run_test(level)
        except KeyboardInterrupt:
            return
        except Exception as e:
            print(f"Error: {e}")
            vm_handler.stop_vm(level)
            return
        vm_handler.stop_vm(level)
        print("\n\n")


if __name__ == "__main__":
    main()
