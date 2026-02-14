from shell_test_utils import ShellTester


def test_builtin_completion(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        output = shell_tester.execute("ech\tCompletion")[0]
        assert output == "Completion\n", f"Expected \"Completion\", got '{output}'"

        output = shell_tester.execute("ty\t exit")[0]
        assert output == "exit is a shell builtin\n", f"Expected \"exit is a shell builtin\", got '{output}'"
    finally:
        shell_tester.stop()
