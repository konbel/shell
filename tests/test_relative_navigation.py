from shell_test_utils import ShellTester


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

    # Test 1: Create test directory structure
    shell_tester.execute("mkdir -p /tmp/pear/raspberry/pear", no_output=True)

    # Test 2: Change to absolute path first as a starting point
    shell_tester.execute("cd /tmp/pear", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/pear", f'Expected "/tmp/pear" but got "{output}"'

    # Test 3: Change using relative path with ./ notation
    shell_tester.execute("cd ./raspberry/pear", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/pear/raspberry/pear", f'Expected "/tmp/pear/raspberry/pear" but got "{output}"'

    # Test 4: Navigate up using ../ notation multiple times
    shell_tester.execute("cd ../../../", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp", f'Expected "/tmp" but got "{output}"'

    # Test 5: Navigate back down using relative path
    shell_tester.execute("cd pear", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/pear", f'Expected "/tmp/pear" but got "{output}"'

    # Test 6: Navigate to parent using ..
    shell_tester.execute("cd ..", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp", f'Expected "/tmp" but got "{output}"'

    # Test 7: Navigate using multiple .. in a row
    shell_tester.execute("cd pear/raspberry/pear", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp/pear/raspberry/pear", f'Expected "/tmp/pear/raspberry/pear" but got "{output}"'

    shell_tester.execute("cd ../../..", no_output=True)
    output = shell_tester.execute("pwd")
    assert output == "/tmp", f'Expected "/tmp" after ../../.. but got "{output}"'

    shell_tester.stop()
