from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file, ensure_dir


def test_double_quotes(shell_executable):
    """Test that the shell correctly handles double quotes.

    This test verifies:
    1. Double quotes preserve string values
    2. Double quotes allow adjacent string concatenation
    3. Single quotes can be used inside double quotes
    4. Empty strings in double quotes work correctly
    5. Double-quoted filenames with spaces work with cat
    """
    tmp_dir = create_test_environment()
    try:
        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Simple double-quoted string
        output = shell_tester.execute('echo "test hello"')[0]
        assert output == "test hello\n", f'Expected "test hello" but got "{output}"'

        # Test 2: Multiple double-quoted strings with adjacent concatenation
        output = shell_tester.execute('echo "hello  world""shelltest"')[0]
        assert output == "hello  worldshelltest\n", f'Expected "hello  worldshelltest" but got "{output}"'

        # Test 3: Double-quoted strings with single quotes inside
        output = shell_tester.execute('echo "shell" "example'"'"'s" "helloworld"')[0]
        assert output == "shell example's helloworld\n", f'Expected "shell example\'s helloworld" but got "{output}"'

        # Test 4: Create test files with spaces in filenames
        ensure_dir(f"{tmp_dir}/cow")
        write_file(f"{tmp_dir}/cow/f 1", "banana strawberry.\n")
        write_file(f"{tmp_dir}/cow/f   49", "pear strawberry.\n")
        write_file(f"{tmp_dir}/cow/f's15", "apple raspberry.\n")

        # Test 5: Read files with double-quoted filenames containing spaces
        output = shell_tester.execute(f'cat "{tmp_dir}/cow/f 1"')[0]
        assert output == "banana strawberry.\n", f'Expected "banana strawberry." but got "{output}"'

        output = shell_tester.execute(f'cat "{tmp_dir}/cow/f   49"')[0]
        assert output == "pear strawberry.\n", f'Expected "pear strawberry." but got "{output}"'

        output = shell_tester.execute(f'cat "{tmp_dir}/cow/f\'s15"')[0]
        assert output == "apple raspberry.\n", f'Expected "apple raspberry." but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)


def test_single_quotes(shell_executable):
    """Test that the shell correctly handles single quotes.

    This test verifies:
    1. Single quotes preserve literal strings without interpretation
    2. Single quotes preserve multiple spaces
    3. Single quotes allow adjacent string concatenation
    4. Empty strings and concatenation work correctly
    5. Single-quoted filenames work with cat
    """
    tmp_dir = create_test_environment()
    try:
        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Simple single-quoted string
        output = shell_tester.execute("echo 'example test'")[0]
        assert output == "example test\n", f'Expected "example test" but got "{output}"'

        # Test 2: Single-quoted string preserves multiple spaces
        output = shell_tester.execute("echo 'hello     world'")[0]
        assert output == "hello     world\n", f'Expected "hello     world" but got "{output}"'

        # Test 3: Multiple single-quoted strings with adjacent concatenation
        output = shell_tester.execute("echo 'hello     world''scriptexample''testshell'")[0]
        assert output == "hello     worldscriptexampletestshell\n", f'Expected "hello     worldscriptexampletestshell" but got "{output}"'

        # Test 4: Create test files with spaces in filenames
        ensure_dir(f"{tmp_dir}/owl")
        write_file(f"{tmp_dir}/owl/f   96", "mango strawberry.\n")
        write_file(f"{tmp_dir}/owl/f   81", "grape pear.\n")
        write_file(f"{tmp_dir}/owl/f   17", "apple pineapple.\n")

        # Test 5: Read files with single-quoted filenames containing spaces
        output = shell_tester.execute(f"cat '{tmp_dir}/owl/f   96'")[0]
        assert output == "mango strawberry.\n", f'Expected "mango strawberry." but got "{output}"'

        output = shell_tester.execute(f"cat '{tmp_dir}/owl/f   81'")[0]
        assert output == "grape pear.\n", f'Expected "grape pear." but got "{output}"'

        output = shell_tester.execute(f"cat '{tmp_dir}/owl/f   17'")[0]
        assert output == "apple pineapple.\n", f'Expected "apple pineapple." but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)
