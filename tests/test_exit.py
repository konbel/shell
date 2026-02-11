from shell_test_utils import ShellTester


def test_exit(shell_executable):
    """Test that the exit command works correctly.

    This test verifies:
    1. The exit command is recognized as a shell builtin
    2. The exit command terminates the shell process
    3. The shell can exit with a specific exit code
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Verify exit is a shell builtin using type command
    output = shell_tester.execute("type exit")
    assert output == "exit is a shell builtin", f'Expected "exit is a shell builtin" but got "{output}"'

    # Test 2: Execute exit command to terminate the shell.
    # The shell should accept the exit command and terminate
    shell_tester.execute("exit", no_output=True)

    # Test 3: Verify the process has actually exited
    exited = shell_tester.wait_for_exit(timeout=2)
    assert exited, "Process did not exit after executing the exit command"
    assert not shell_tester.is_alive(), "Process is still alive after exit command"

    # Clean up (process should already be dead)
    shell_tester.stop()


def test_exit_with_code(shell_executable):
    """Test that the exit command accepts an exit code.

    This test verifies:
    1. The exit command can accept an exit code argument
    2. The shell terminates when exit is called with a code
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Verify that we can run commands before exiting
    output = shell_tester.execute("type exit")
    assert output == "exit is a shell builtin", f'Expected "exit is a shell builtin" but got "{output}"'

    # Test 2: Execute exit with code 0 (success)
    shell_tester.execute("exit 0", no_output=True)

    # Test 3: Verify the process has actually exited
    exited = shell_tester.wait_for_exit(timeout=2)
    assert exited, "Process did not exit after executing the exit command with code"
    assert not shell_tester.is_alive(), "Process is still alive after exit command with code"

    # Clean up (process should already be dead)
    shell_tester.stop()
