from shell_test_utils import ShellTester


def test_absolute_navigation(shell_executable):
    """Test that the cd builtin command works with absolute paths.

    This test verifies:
    1. The cd command can change to absolute directory paths
    2. The pwd command reports the correct directory after changing
    3. The cd command properly reports errors for non-existent directories
    4. Failed cd commands don't change the current directory
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Verify cd is a shell builtin
    output = shell_tester.execute("type cd")
    assert output == "cd is a shell builtin", f'Expected "cd is a shell builtin" but got "{output}"'

    # Test 2: Create test directory structure
    shell_tester.execute("mkdir -p /tmp/grape/pear/apple", no_output=True)

    # Test 3: Change to absolute path and verify with pwd
    shell_tester.execute("cd /tmp/grape/pear/apple", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/grape/pear/apple", f'Expected "/tmp/grape/pear/apple" but got "{output}"'

    # Test 4: Attempt to change to non-existent directory
    output = shell_tester.execute("cd /non-existing-directory")
    assert "No such file or directory" in output, f'Expected error message containing "No such file or directory" but got "{output}"'

    # Test 5: Verify current directory didn't change after failed cd
    output = shell_tester.execute("pwd")
    assert output == "/tmp/grape/pear/apple", f'Expected "/tmp/grape/pear/apple" after failed cd, but got "{output}"'

    # Test 6: Change to root directory
    shell_tester.execute("cd /", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/", f'Expected "/" but got "{output}"'

    # Test 7: Change to /tmp and verify
    shell_tester.execute("cd /tmp", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp", f'Expected "/tmp" but got "{output}"'

    shell_tester.stop()
