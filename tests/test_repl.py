from shell_test_utils import ShellTester


def test_repl(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        for i in range(1, 6):
            output = shell_tester.execute(f"invalid_command_{i}")[0]
            assert output == f"invalid_command_{i}: command not found\n", f"Expected \"invalid_command_{i}: command not found\" but got \"{output}\""
    finally:
        shell_tester.stop()
