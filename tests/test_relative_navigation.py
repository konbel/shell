from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment


def test_relative_navigation(shell_executable):
    """Test that the cd builtin command works with relative paths.

    This test verifies:
    1. The cd command can change to relative directory paths
    2. The pwd command reports the correct directory after changing
    3. The cd command handles ./ (current directory) notation
    4. The cd command handles ../ (parent directory) notation
    5. Multiple directory traversals work correctly
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()

    try:
        # Test 1: Create test directory structure
        shell_tester.execute(f"mkdir -p {tmp_dir}/pear/raspberry/pear", no_output=True)

        # Test 2: Change to absolute path first as a starting point
        shell_tester.execute(f"cd {tmp_dir}/pear", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/pear\n", f'Expected "{tmp_dir}/pear" but got "{output}"'

        # Test 3: Change using relative path with ./ notation
        shell_tester.execute("cd ./raspberry/pear", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/pear/raspberry/pear\n", f'Expected "{tmp_dir}/pear/raspberry/pear" but got "{output}"'

        # Test 4: Navigate up using ../ notation multiple times
        shell_tester.execute("cd ../../../", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}\n", f'Expected "{tmp_dir}" but got "{output}"'

        # Test 5: Navigate back down using relative path
        shell_tester.execute("cd pear", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/pear\n", f'Expected "{tmp_dir}/pear" but got "{output}"'

        # Test 6: Navigate to parent using ..
        shell_tester.execute("cd ..", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}\n", f'Expected "{tmp_dir}" but got "{output}"'

        # Test 7: Navigate using multiple .. in a row
        shell_tester.execute("cd pear/raspberry/pear", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/pear/raspberry/pear\n", f'Expected "{tmp_dir}/pear/raspberry/pear" but got "{output}"'

        shell_tester.execute("cd ../../..", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}\n", f'Expected "{tmp_dir}" after ../../.. but got "{output}"'
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)
