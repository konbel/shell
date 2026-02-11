from shell_test_utils import ShellTester


def test_echo(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    test_strings = ["pineapple pear", "mango blueberry strawberry"]

    for test_string in test_strings:
        output = shell_tester.execute(f"echo {test_string}")
        assert output == f"{test_string}", f"Expected \"{test_string}\" but got \"{output}\""

    shell_tester.stop()
