from shell_test_utils import ShellTester
import subprocess
import os


def test_quoted_executable(shell_executable):
    """Test that the shell can execute programs with quoted names containing special characters.

    This test verifies:
    1. Executables with spaces in their names can be executed with single quotes
    2. Executables with double quotes in their names can be executed with single quotes
    3. Executables with single quotes in their names can be executed with double quotes
    4. Executables with backslashes in their names can be executed with proper escaping
    5. Quoted executables receive arguments correctly
    """
    # Create test executables in /tmp/cow
    test_dir = '/tmp/cow'
    subprocess.run(['mkdir', '-p', test_dir], check=True)

    # Create test data files
    subprocess.run(['sh', '-c', 'printf "pear blueberry.\n" > "/tmp/cow/f1"'], check=True)
    subprocess.run(['sh', '-c', 'printf "apple blueberry.\n" > "/tmp/cow/f2"'], check=True)
    subprocess.run(['sh', '-c', 'printf "mango banana.\n" > "/tmp/cow/f3"'], check=True)
    subprocess.run(['sh', '-c', 'printf "raspberry banana.\n" > "/tmp/cow/f4"'], check=True)

    # Create executable scripts with special characters in names
    # Test 1: Executable with spaces in name
    exe_with_spaces = os.path.join(test_dir, 'exe  with  space')
    with open(exe_with_spaces, 'w') as f:
        f.write('#!/bin/sh\ncat "$@"\n')
    os.chmod(exe_with_spaces, 0o755)

    # Test 2: Executable with double quotes in name
    exe_with_double_quotes = os.path.join(test_dir, 'exe with "quotes"')
    with open(exe_with_double_quotes, 'w') as f:
        f.write('#!/bin/sh\ncat "$@"\n')
    os.chmod(exe_with_double_quotes, 0o755)

    # Test 3: Executable with single quotes in name
    exe_with_single_quotes = os.path.join(test_dir, "exe with 'single quotes'")
    with open(exe_with_single_quotes, 'w') as f:
        f.write('#!/bin/sh\ncat "$@"\n')
    os.chmod(exe_with_single_quotes, 0o755)

    # Test 4: Executable with backslash in name
    exe_with_backslash = os.path.join(test_dir, 'exe with \\ backslash')
    with open(exe_with_backslash, 'w') as f:
        f.write('#!/bin/sh\ncat "$@"\n')
    os.chmod(exe_with_backslash, 0o755)

    # Update PATH to include the test directory
    env = {'PATH': test_dir + ':' + os.environ.get('PATH', '')}

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env=env)

    # Test 1: Execute executable with spaces using single quotes
    output = shell_tester.execute("'exe  with  space' /tmp/cow/f1")
    assert output == "pear blueberry.", f'Expected "pear blueberry." but got "{output}"'

    # Test 2: Execute executable with double quotes using single quotes
    output = shell_tester.execute("'exe with \"quotes\"' /tmp/cow/f2")
    assert output == "apple blueberry.", f'Expected "apple blueberry." but got "{output}"'

    # Test 3: Execute executable with single quotes using double quotes
    output = shell_tester.execute("\"exe with 'single quotes'\" /tmp/cow/f3")
    assert output == "mango banana.", f'Expected "mango banana." but got "{output}"'

    # Test 4: Execute executable with backslash using double quotes with escaping
    output = shell_tester.execute("\"exe with \\\\ backslash\" /tmp/cow/f4")
    assert output == "raspberry banana.", f'Expected "raspberry banana." but got "{output}"'

    shell_tester.stop()
