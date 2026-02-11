from shell_test_utils import ShellTester
import subprocess


def test_backslash_double_quotes(shell_executable):
    """Test that the shell correctly handles backslash escaping within double quotes.

    This test verifies:
    1. Single quotes within double quotes don't need escaping
    2. Double quotes within double quotes can be escaped with backslash
    3. Backslashes within double quotes can be escaped
    4. Escaped filenames with special characters work with cat
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Single quotes within double quotes don't need escaping
    output = shell_tester.execute('echo "test\'example\'\\\\\'script"')
    assert output == "test'example'\\\'script", f'Expected "test\'example\'\\\\\'script" but got "{output}"'

    # Test 2: Double quotes within double quotes with escaping
    output = shell_tester.execute('echo "test\\"insidequotes"example\\""')
    assert output == 'test"insidequotesexample"', f'Expected \'test"insidequotesexample"\' but got "{output}"'

    # Test 3: Mixed quotes and backslashes within double quotes
    output = shell_tester.execute('echo "mixed\\"quote\'shell\'\\\\"')
    assert output == "mixed\"quote'shell'\\", f'Expected "mixed\\"quote\'shell\'\\\\" but got "{output}"'

    # Test 4: Create test files with escaped characters in filenames
    subprocess.run(['mkdir', '-p', '/tmp/rat'], check=True)
    subprocess.run(['sh', '-c', 'printf "orange banana." > "/tmp/rat/number 33"'], check=True)
    subprocess.run(['sh', '-c', 'printf "strawberry pear." > "/tmp/rat/doublequote \\" 27"'], check=True)
    subprocess.run(['sh', '-c', 'printf "blueberry strawberry.\n" > "/tmp/rat/backslash \\\\ 44"'], check=True)

    # Test 5: Read files with escaped filenames containing double quotes and backslashes
    output = shell_tester.execute('cat /tmp/rat/"number 33" /tmp/rat/"doublequote \\" 27" /tmp/rat/"backslash \\\\ 44"')
    assert output == "orange banana.strawberry pear.blueberry strawberry.", f'Expected concatenated file output but got "{output}"'

    shell_tester.stop()


def test_backslash_single_quotes(shell_executable):
    """Test that the shell correctly handles backslash escaping within single quotes.

    This test verifies:
    1. Backslashes within single quotes are treated literally
    2. Escape sequences within single quotes are not interpreted
    3. Double quotes within single quotes are treated literally
    4. Single-quoted filenames with backslashes work with cat
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Backslashes and newline escape within single quotes are literal
    output = shell_tester.execute("echo 'example\\\\ntest'")
    assert output == "example\\\\ntest", f'Expected "example\\\\ntest" but got "{output}"'

    # Test 2: Double quotes within single quotes are literal
    output = shell_tester.execute('echo \'hello\\"scriptworld\\"example\'')
    assert output == 'hello\\"scriptworld\\"example', f'Expected "hello\\\\"scriptworld\\\\"example" but got "{output}"'

    # Test 3: Backslashes within single quotes are literal
    output = shell_tester.execute("echo 'world\\\\ntest'")
    assert output == "world\\\\ntest", f'Expected "world\\\\ntest" but got "{output}"'

    # Test 4: Create test files with backslashes in filenames
    subprocess.run(['mkdir', '-p', '/tmp/cow'], check=True)
    subprocess.run(['sh', '-c', 'printf "blueberry apple." > "/tmp/cow/no slash 32"'], check=True)
    subprocess.run(['sh', '-c', 'printf "mango orange." > "/tmp/cow/one slash \\53"'], check=True)
    subprocess.run(['sh', '-c', 'printf "mango raspberry.\n" > "/tmp/cow/two slashes \\99\\\\"'], check=True)

    # Test 5: Read files with single-quoted filenames containing backslashes
    output = shell_tester.execute("cat /tmp/cow/'no slash 32' /tmp/cow/'one slash \\53' /tmp/cow/'two slashes \\99\\'")
    assert output == "blueberry apple.mango orange.mango raspberry.", f'Expected concatenated file output but got "{output}"'

    shell_tester.stop()


def test_backslash_outside_quotes(shell_executable):
    """Test that the shell correctly handles backslash escaping outside quotes.

    This test verifies:
    1. Backslashes escape spaces to preserve them as single arguments
    2. Backslashes can escape quotes outside quoted strings
    3. Backslashes with non-special characters are treated literally
    4. Escaped filenames with underscores work with cat
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Backslashes escape multiple spaces
    output = shell_tester.execute("echo test\\ \\ \\ \\ \\ \\ shell")
    assert output == "test      shell", f'Expected "test      shell" but got "{output}"'

    # Test 2: Backslashes escape quotes outside of quoted strings
    output = shell_tester.execute('echo \\\'\"shell script\"\\\'')
    assert output == '\'shell script\'', f'Expected "\'shell script\'" but got "{output}"'

    # Test 3: Backslash with non-special character (n) is treated literally
    output = shell_tester.execute("echo script\\nhello")
    assert output == "scriptnhello", f'Expected "scriptnhello" but got "{output}"'

    # Test 4: Create test files with escaped underscores in filenames
    subprocess.run(['mkdir', '-p', '/tmp/rat'], check=True)
    subprocess.run(['sh', '-c', 'printf "pineapple apple." > "/tmp/rat/_ignored_65"'], check=True)
    subprocess.run(['sh', '-c', 'printf "blueberry grape." > "/tmp/rat/ignore_95"'], check=True)
    subprocess.run(['sh', '-c', 'printf "blueberry banana.\n" > "/tmp/rat/just_one_\\\\_75"'], check=True)

    # Test 5: Read files with escaped underscores in filenames
    output = shell_tester.execute("cat /tmp/rat/\\_ignored_65 /tmp/rat/ignore_\\95 /tmp/rat/just_one_\\\\\\_75")
    assert output == "pineapple apple.blueberry grape.blueberry banana.", f'Expected concatenated file output but got "{output}"'

    shell_tester.stop()
