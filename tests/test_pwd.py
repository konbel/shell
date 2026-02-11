import os

from shell_test_utils import ShellTester


def test_pwd(shell_executable):
    """Test that the pwd builtin command works correctly.

    This test verifies:
    1. The pwd command is recognized as a shell builtin
    2. The pwd command outputs the current working directory
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Verify pwd is a shell builtin using type command
    output = shell_tester.execute("type pwd")
    assert output == "pwd is a shell builtin", f'Expected "pwd is a shell builtin" but got "{output}"'

    # Test 2: Verify pwd outputs the current working directory
    # The shell should start in its own directory
    output = shell_tester.execute("pwd")
    cwd = os.path.abspath(shell_executable)
    cwd = cwd[:cwd.rfind(os.sep)]
    assert output == cwd, f'Expected "{cwd}" but got "{output}"'

    shell_tester.stop()
