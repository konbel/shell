from shell_test_utils import ShellTester


def test_type(shell_executable):
    """Verify `type` reports builtins and reports not found for unknown commands."""

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        cases = [
            ("type echo", "echo is a shell builtin"),
            ("type exit", "exit is a shell builtin"),
            ("type type", "type is a shell builtin"),
            ("type invalid_raspberry_command", "invalid_raspberry_command not found"),
            ("type invalid_orange_command", "invalid_orange_command not found"),
        ]

        for cmd, expected in cases:
            output = shell_tester.execute(cmd)[0]
            assert output == expected + "\n", f'Expected "{expected}" but got "{output}"'
    finally:
        shell_tester.stop()
