from shell_test_utils import ShellTester


def test_invalid_command(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    output = shell_tester.execute("invalid_command")
    assert output == "invalid_command: command not found", f"Expected \"invalid_command: command not found\" but got \"{output}\""

    shell_tester.stop()
