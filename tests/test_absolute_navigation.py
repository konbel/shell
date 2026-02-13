from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, ensure_dir


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
    output = shell_tester.execute("type cd")[0]
    assert output == "cd is a shell builtin\n", f'Expected "cd is a shell builtin" but got "{output}"'

    tmp_dir = create_test_environment()
    ensure_dir(f"{tmp_dir}/grape/pear/apple")

    # Test 2: Change to absolute path and verify with pwd
    shell_tester.execute(f"cd {tmp_dir}/grape/pear/apple", no_output=True)
    output = shell_tester.execute("pwd")[0]
    assert output == f"{tmp_dir}/grape/pear/apple\n", f'Expected "{tmp_dir}/grape/pear/apple" but got "{output}"'

    # Test 3: Attempt to change to non-existent directory
    output = shell_tester.execute("cd /non-existing-directory")[0]
    assert "No such file or directory" in output, f'Expected error message containing "No such file or directory" but got "{output}"'

    # Test 4: Verify current directory didn't change after failed cd
    output = shell_tester.execute("pwd")[0]
    assert output == f"{tmp_dir}/grape/pear/apple\n", f'Expected "{tmp_dir}/grape/pear/apple" after failed cd, but got "{output}"'

    # Test 5: Change to root directory
    shell_tester.execute("cd /", no_output=True)
    output = shell_tester.execute("pwd")[0]
    assert output == "/\n", f'Expected "/" but got "{output}"'

    # Test 6: Change to /tmp and verify
    shell_tester.execute(f"cd {tmp_dir}", no_output=True)
    output = shell_tester.execute("pwd")[0]
    assert output == f"{tmp_dir}\n", f'Expected "{tmp_dir}" but got "{output}"'

    cleanup_test_environment(tmp_dir)
    shell_tester.stop()
