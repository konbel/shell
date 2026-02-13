from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file, ensure_dir


def test_backslash_double_quotes(shell_executable):
    """Test that the shell correctly handles backslash escaping within double quotes.

    This test verifies:
    1. Single quotes within double quotes don't need escaping
    2. Double quotes within double quotes can be escaped with backslash
    3. Backslashes within double quotes can be escaped
    4. Escaped filenames with special characters work with cat
    """
    tmp_dir = create_test_environment()
    try:
        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Single quotes within double quotes don't need escaping
        output = shell_tester.execute('echo "test\'example\'\\\\\'script"')[0]
        assert output == "test'example'\\\'script\n", f'Expected "test\'example\'\\\\\'script" but got "{output}"'

        # Test 2: Double quotes within double quotes with escaping
        output = shell_tester.execute('echo "test\\"insidequotes"example\\""')[0]
        assert output == 'test"insidequotesexample"\n', f'Expected \'test"insidequotesexample"\' but got "{output}"'

        # Test 3: Mixed quotes and backslashes within double quotes
        output = shell_tester.execute('echo "mixed\\"quote\'shell\'\\\\"')[0]
        assert output == "mixed\"quote'shell'\\\n", f'Expected "mixed\\"quote\'shell\'\\\\" but got "{output}"'

        # Test 4: Create test files with escaped characters in filenames
        ensure_dir(f"{tmp_dir}/rat")
        write_file(f"{tmp_dir}/rat/number 33", "orange banana.")
        write_file(f'{tmp_dir}/rat/doublequote " 27', "strawberry pear.")
        write_file(f"{tmp_dir}/rat/backslash \\ 44", "blueberry strawberry.\n")

        # Test 5: Read files with escaped filenames containing double quotes and backslashes
        output = shell_tester.execute(f'cat "{tmp_dir}/rat/number 33" "{tmp_dir}/rat/doublequote \\" 27" "{tmp_dir}/rat/backslash \\\\ 44"')[0]
        assert output == "orange banana.strawberry pear.blueberry strawberry.\n", f'Expected concatenated file output but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)


def test_backslash_single_quotes(shell_executable):
    """Test that the shell correctly handles backslash escaping within single quotes.

    This test verifies:
    1. Backslashes within single quotes are treated literally
    2. Escape sequences within single quotes are not interpreted
    3. Double quotes within single quotes are treated literally
    4. Single-quoted filenames with backslashes work with cat
    """
    tmp_dir = create_test_environment()
    try:
        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Backslashes and newline escape within single quotes are literal
        output = shell_tester.execute("echo 'example\\\\ntest'")[0]
        assert output == "example\\\\ntest\n", f'Expected "example\\\\ntest" but got "{output}"'

        # Test 2: Double quotes within single quotes are literal
        output = shell_tester.execute('echo \'hello\\"scriptworld\\"example\'')[0]
        assert output == 'hello\\"scriptworld\\"example\n', f'Expected "hello\\\\"scriptworld\\\\"example" but got "{output}"'

        # Test 3: Backslashes within single quotes are literal
        output = shell_tester.execute("echo 'world\\\\ntest'")[0]
        assert output == "world\\\\ntest\n", f'Expected "world\\\\ntest" but got "{output}"'

        # Test 4: Create test files with backslashes in filenames
        ensure_dir(f"{tmp_dir}/cow")
        write_file(f"{tmp_dir}/cow/no slash 32", "blueberry apple.")
        write_file(f"{tmp_dir}/cow/one slash \\53", "mango orange.")
        write_file(f"{tmp_dir}/cow/two slashes \\99\\\\", "mango raspberry.\n")

        # Test 5: Read files with single-quoted filenames containing backslashes
        output = shell_tester.execute(f"cat {tmp_dir}/cow/'no slash 32' {tmp_dir}/cow/'one slash \\53' {tmp_dir}/cow/'two slashes \\99\\\\'")[0]
        assert output == "blueberry apple.mango orange.mango raspberry.\n", f'Expected concatenated file output but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)


def test_backslash_outside_quotes(shell_executable):
    """Test that the shell correctly handles backslash escaping outside quotes.

    This test verifies:
    1. Backslashes escape spaces to preserve them as single arguments
    2. Backslashes can escape quotes outside quoted strings
    3. Backslashes with non-special characters are treated literally
    4. Escaped filenames with underscores work with cat
    """
    tmp_dir = create_test_environment()
    try:
        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Backslashes escape multiple spaces
        output = shell_tester.execute("echo test\\ \\ \\ \\ \\ \\ shell")[0]
        assert output == "test      shell\n", f'Expected "test      shell" but got "{output}"'

        # Test 2: Backslashes escape quotes outside of quoted strings
        output = shell_tester.execute('echo \\\'\"shell script\"\\\'')[0]
        assert output == '\'shell script\'\n', f'Expected "\'shell script\'" but got "{output}"'

        # Test 3: Backslash with non-special character (n) is treated literally
        output = shell_tester.execute("echo script\\nhello")[0]
        assert output == "scriptnhello\n", f'Expected "scriptnhello" but got "{output}"'

        # Test 4: Create test files with escaped underscores in filenames
        ensure_dir(f"{tmp_dir}/rat")
        write_file(f"{tmp_dir}/rat/_ignored_65", "pineapple apple.")
        write_file(f"{tmp_dir}/rat/ignore_95", "blueberry grape.")
        write_file(f"{tmp_dir}/rat/just_one_\\_75", "blueberry banana.\n")

        # Test 5: Read files with escaped underscores in filenames
        output = shell_tester.execute(f"cat {tmp_dir}/rat/\\_ignored_65 {tmp_dir}/rat/ignore_\\95 {tmp_dir}/rat/just_one_\\\\_75")[0]
        assert output == "pineapple apple.blueberry grape.blueberry banana.\n", f'Expected concatenated file output but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)
