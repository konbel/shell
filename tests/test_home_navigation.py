from shell_test_utils import ShellTester, create_test_environment, ensure_dir, cleanup_test_environment


def test_home_navigation(shell_executable):
    """Test that the cd builtin command works with home directory notation (~).

    This test verifies:
    1. The cd command can change to absolute directory paths
    2. The ~ tilde notation correctly expands to the home directory
    3. The pwd command reports the correct directory after changing
    4. Navigation between regular paths and home directory works correctly
    """
    tmp_dir = create_test_environment()

    # Set HOME to a test directory for this test
    home_dir = f"{tmp_dir}/orange/raspberry/grape"
    test_env = {"HOME": home_dir}

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env=test_env)

    try:
        # Test 1: Create test directory structure
        ensure_dir(f"{tmp_dir}/mango/strawberry/grape")
        ensure_dir(f"{tmp_dir}/orange/raspberry/grape")

        # Test 2: Change to a regular absolute path
        shell_tester.execute(f"cd {tmp_dir}/mango/strawberry/grape", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/mango/strawberry/grape\n", f'Expected "{tmp_dir}/mango/strawberry/grape" but got "{output}"'

        # Test 3: Navigate using ~ tilde notation (which should expand to HOME)
        shell_tester.execute("cd ~", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == home_dir + "\n", f'Expected "{home_dir}" but got "{output}"'

        # Test 4: Verify we can navigate from home to another location
        shell_tester.execute(f"cd {tmp_dir}/mango", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/mango\n", f'Expected "{tmp_dir}/mango" but got "{output}"'

        # Test 5: Navigate back to home using ~
        shell_tester.execute("cd ~", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == home_dir + "\n", f'Expected "{home_dir}" after cd ~ but got "{output}"'

        # Test 6: Navigate using ~/ with relative path
        # First navigate to home, then create subdir there, then navigate into it
        shell_tester.execute("cd ~", no_output=True)
        ensure_dir(f"{home_dir}/subdir")
        shell_tester.execute("cd ~/subdir", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{home_dir}/subdir\n", f'Expected "{home_dir}/subdir" but got "{output}"'

        # Test 7: Verify we can navigate away and back again
        shell_tester.execute(f"cd {tmp_dir}/mango/strawberry/grape", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == f"{tmp_dir}/mango/strawberry/grape\n", f'Expected "{tmp_dir}/mango/strawberry/grape" but got "{output}"'

        # Test 8: Final navigation back to home using cd with no arguments
        shell_tester.execute("cd", no_output=True)
        output = shell_tester.execute("pwd")[0]
        assert output == home_dir + "\n", f'Expected "{home_dir}" at end but got "{output}"'
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)
