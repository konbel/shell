from shell_test_utils import ShellTester


def test_repl(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    for i in range(1, 6):
        output = shell_tester.execute(f"invalid_command_{i}")
        assert output == f"invalid_command_{i}: command not found", f"Expected \"invalid_command_{i}: command not found\" but got \"{output}\""

    shell_tester.stop()
