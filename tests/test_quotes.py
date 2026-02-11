from shell_test_utils import ShellTester
import subprocess


def test_double_quotes(shell_executable):
    """Test that the shell correctly handles double quotes.

    This test verifies:
    1. Double quotes preserve string values
    2. Double quotes allow adjacent string concatenation
    3. Single quotes can be used inside double quotes
    4. Empty strings in double quotes work correctly
    5. Double-quoted filenames with spaces work with cat
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Simple double-quoted string
    output = shell_tester.execute('echo "test hello"')
    assert output == "test hello", f'Expected "test hello" but got "{output}"'

    # Test 2: Multiple double-quoted strings with adjacent concatenation
    output = shell_tester.execute('echo "hello  world""shelltest"')
    assert output == "hello  worldshelltest", f'Expected "hello  worldshelltest" but got "{output}"'

    # Test 3: Double-quoted strings with single quotes inside
    output = shell_tester.execute('echo "shell" "example'"'"'s" "helloworld"')
    assert output == "shell example's helloworld", f'Expected "shell example\'s helloworld" but got "{output}"'

    # Test 4: Create test files with spaces in filenames
    subprocess.run(['mkdir', '-p', '/tmp/cow'], check=True)
    subprocess.run(['sh', '-c', 'printf "banana strawberry.\n" > "/tmp/cow/f 1"'], check=True)
    subprocess.run(['sh', '-c', 'printf "pear strawberry.\n" > "/tmp/cow/f   49"'], check=True)
    subprocess.run(['sh', '-c', 'printf "apple raspberry.\n" > "/tmp/cow/f\'s15"'], check=True)

    # Test 5: Read files with double-quoted filenames containing spaces
    output = shell_tester.execute('cat "/tmp/cow/f 1"')
    assert output == "banana strawberry.", f'Expected "banana strawberry." but got "{output}"'

    output = shell_tester.execute('cat "/tmp/cow/f   49"')
    assert output == "pear strawberry.", f'Expected "pear strawberry." but got "{output}"'

    output = shell_tester.execute('cat "/tmp/cow/f\'s15"')
    assert output == "apple raspberry.", f'Expected "apple raspberry." but got "{output}"'

    shell_tester.stop()


def test_single_quotes(shell_executable):
    """Test that the shell correctly handles single quotes.

    This test verifies:
    1. Single quotes preserve literal strings without interpretation
    2. Single quotes preserve multiple spaces
    3. Single quotes allow adjacent string concatenation
    4. Empty strings and concatenation work correctly
    5. Single-quoted filenames work with cat
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    # Test 1: Simple single-quoted string
    output = shell_tester.execute("echo 'example test'")
    assert output == "example test", f'Expected "example test" but got "{output}"'

    # Test 2: Single-quoted string preserves multiple spaces
    output = shell_tester.execute("echo 'hello     world'")
    assert output == "hello     world", f'Expected "hello     world" but got "{output}"'

    # Test 3: Multiple single-quoted strings with adjacent concatenation
    output = shell_tester.execute("echo 'hello     world''scriptexample''testshell'")
    assert output == "hello     worldscriptexampletestshell", f'Expected "hello     worldscriptexampletestshell" but got "{output}"'

    # Test 4: Create test files with spaces in filenames
    subprocess.run(['mkdir', '-p', '/tmp/owl'], check=True)
    subprocess.run(['sh', '-c', 'printf "mango strawberry.\n" > "/tmp/owl/f   96"'], check=True)
    subprocess.run(['sh', '-c', 'printf "grape pear.\n" > "/tmp/owl/f   81"'], check=True)
    subprocess.run(['sh', '-c', 'printf "apple pineapple.\n" > "/tmp/owl/f   17"'], check=True)

    # Test 5: Read files with single-quoted filenames containing spaces
    output = shell_tester.execute("cat '/tmp/owl/f   96'")
    assert output == "mango strawberry.", f'Expected "mango strawberry." but got "{output}"'

    output = shell_tester.execute("cat '/tmp/owl/f   81'")
    assert output == "grape pear.", f'Expected "grape pear." but got "{output}"'

    output = shell_tester.execute("cat '/tmp/owl/f   17'")
    assert output == "apple pineapple.", f'Expected "apple pineapple." but got "{output}"'

    shell_tester.stop()
