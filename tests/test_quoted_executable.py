from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file, ensure_dir
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
    tmp_dir = create_test_environment()
    try:
        # Create test data files
        write_file(f"{tmp_dir}/f1", "pear blueberry.\n")
        write_file(f"{tmp_dir}/f2", "apple blueberry.\n")
        write_file(f"{tmp_dir}/f3", "mango banana.\n")
        write_file(f"{tmp_dir}/f4", "raspberry banana.\n")

        # Create executable scripts with special characters in names
        # Test 1: Executable with spaces in name
        exe_with_spaces = os.path.join(tmp_dir, 'exe  with  space')
        with open(exe_with_spaces, 'w') as f:
            f.write('#!/bin/sh\ncat "$@"\n')
        os.chmod(exe_with_spaces, 0o755)

        # Test 2: Executable with double quotes in name
        exe_with_double_quotes = os.path.join(tmp_dir, 'exe with "quotes"')
        with open(exe_with_double_quotes, 'w') as f:
            f.write('#!/bin/sh\ncat "$@"\n')
        os.chmod(exe_with_double_quotes, 0o755)

        # Test 3: Executable with single quotes in name
        exe_with_single_quotes = os.path.join(tmp_dir, "exe with 'single quotes'")
        with open(exe_with_single_quotes, 'w') as f:
            f.write('#!/bin/sh\ncat "$@"\n')
        os.chmod(exe_with_single_quotes, 0o755)

        # Test 4: Executable with backslash in name
        exe_with_backslash = os.path.join(tmp_dir, 'exe with \\ backslash')
        with open(exe_with_backslash, 'w') as f:
            f.write('#!/bin/sh\ncat "$@"\n')
        os.chmod(exe_with_backslash, 0o755)

        # Update PATH to include the test directory
        env = {'PATH': tmp_dir + ':' + os.environ.get('PATH', '')}

        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell(env=env)

        # Test 1: Execute executable with spaces using single quotes
        output = shell_tester.execute(f"'exe  with  space' {tmp_dir}/f1")[0]
        assert output == "pear blueberry.\n", f'Expected "pear blueberry." but got "{output}"'

        # Test 2: Execute executable with double quotes using single quotes
        output = shell_tester.execute("'exe with \"quotes\"' {}/f2".format(tmp_dir))[0]
        assert output == "apple blueberry.\n", f'Expected "apple blueberry." but got "{output}"'

        # Test 3: Execute executable with single quotes using double quotes
        output = shell_tester.execute("\"exe with 'single quotes'\" {}/f3".format(tmp_dir))[0]
        assert output == "mango banana.\n", f'Expected "mango banana." but got "{output}"'

        # Test 4: Execute executable with backslash using double quotes with escaping
        output = shell_tester.execute("\"exe with \\\\ backslash\" {}/f4".format(tmp_dir))[0]
        assert output == "raspberry banana.\n", f'Expected "raspberry banana." but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)
