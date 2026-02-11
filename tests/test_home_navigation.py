from shell_test_utils import ShellTester


def test_home_navigation(shell_executable):
    """Test that the cd builtin command works with home directory notation (~).

    This test verifies:
    1. The cd command can change to absolute directory paths
    2. The ~ tilde notation correctly expands to the home directory
    3. The pwd command reports the correct directory after changing
    4. Navigation between regular paths and home directory works correctly
    """
    # Set HOME to a test directory for this test
    home_dir = "/tmp/orange/raspberry/grape"
    test_env = {"HOME": home_dir}

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env=test_env)

    # Test 1: Create test directory structure
    shell_tester.execute("mkdir -p /tmp/mango/strawberry/grape", no_output=True)
    shell_tester.execute("mkdir -p /tmp/orange/raspberry/grape", no_output=True)

    # Test 2: Change to a regular absolute path
    shell_tester.execute("cd /tmp/mango/strawberry/grape", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/mango/strawberry/grape", f'Expected "/tmp/mango/strawberry/grape" but got "{output}"'

    # Test 3: Navigate using ~ tilde notation (which should expand to HOME)
    shell_tester.execute("cd ~", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == home_dir, f'Expected "{home_dir}" but got "{output}"'

    # Test 4: Verify we can navigate from home to another location
    shell_tester.execute("cd /tmp/mango", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/mango", f'Expected "/tmp/mango" but got "{output}"'

    # Test 5: Navigate back to home using ~
    shell_tester.execute("cd ~", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == home_dir, f'Expected "{home_dir}" after cd ~ but got "{output}"'

    # Test 6: Navigate using ~/ with relative path
    # First navigate to home, then create subdir there, then navigate into it
    shell_tester.execute("cd ~", no_output=True)
    shell_tester.execute("mkdir -p subdir", no_output=True)
    shell_tester.execute("cd ~/subdir", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == f"{home_dir}/subdir", f'Expected "{home_dir}/subdir" but got "{output}"'

    # Test 7: Verify we can navigate away and back again
    shell_tester.execute("cd /tmp/mango/strawberry/grape", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/mango/strawberry/grape", f'Expected "/tmp/mango/strawberry/grape" but got "{output}"'

    # Test 8: Final navigation back to home using cd with no arguments
    shell_tester.execute("cd", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == home_dir, f'Expected "{home_dir}" at end but got "{output}"'

    shell_tester.stop()
