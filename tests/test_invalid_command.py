from shell_test_utils import ShellTester


def test_invalid_command(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        output = shell_tester.execute("invalid_command")[0]
        assert output == "invalid_command: command not found\n", f"Expected \"invalid_command: command not found\" but got \"{output}\""
    finally:
        shell_tester.stop()
