from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file, ensure_dir, file_exists
import os


def test_redirect_stdout(shell_executable):
    """Test that the shell correctly redirects stdout to files.

    This test verifies:
    1. The > operator redirects stdout to a file
    2. The 1> operator explicitly redirects stdout to a file
    3. Multiple commands can write to files sequentially
    4. Stderr is still printed when stdout is redirected
    """
    tmp_dir = create_test_environment()
    try:
        # Create test files
        ensure_dir(f"{tmp_dir}/duck")
        write_file(f"{tmp_dir}/duck/mango", "mango")
        write_file(f"{tmp_dir}/duck/pineapple", "pineapple\n")
        write_file(f"{tmp_dir}/duck/raspberry", "raspberry")
        ensure_dir(f"{tmp_dir}/dog")

        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Redirect stdout using >
        shell_tester.execute(f"ls {tmp_dir}/duck > {tmp_dir}/dog/cow.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/dog/cow.md")
        assert output == ["mango\n", "pineapple\n", "raspberry\n"], f'Expected file listing but got "{output}"'

        # Test 2: Redirect stdout using 1>
        shell_tester.execute(f"echo 'Hello David' 1> {tmp_dir}/dog/owl.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/dog/owl.md")[0]
        assert output == "Hello David\n", f'Expected "Hello David" but got "{output}"'

        # Test 3: Stderr is still printed when stdout is redirected
        output = shell_tester.execute(f"cat {tmp_dir}/duck/pineapple nonexistent 1> {tmp_dir}/dog/pig.md")[0]
        assert "nonexistent: No such file or directory" in output, f'Expected error message but got "{output}"'

        # Test 4: Verify redirected stdout was captured in file
        output = shell_tester.execute(f"cat {tmp_dir}/dog/pig.md")[0]
        assert output == "pineapple\n", f'Expected "pineapple" but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)


def test_redirect_stderr(shell_executable):
    """Test that the shell correctly redirects stderr to files.

    This test verifies:
    1. The 2> operator redirects stderr to a file
    2. Stderr is captured in the file while stdout goes to console
    3. Non-existent files produce errors that are redirected
    4. Valid stdout output still appears on console
    """
    tmp_dir = create_test_environment()
    try:
        # Create test files
        ensure_dir(f"{tmp_dir}/dog")
        write_file(f"{tmp_dir}/dog/pear", "pear\n")
        ensure_dir(f"{tmp_dir}/pig")

        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Redirect stderr using 2>
        shell_tester.execute(f"ls -1 nonexistent 2> {tmp_dir}/pig/bee.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/pig/bee.md")[0]
        assert "No such file or directory" in output, f'Expected error message but got "{output}"'

        # Test 2: Stdout is not redirected when using 2>
        output = shell_tester.execute(f"echo 'Alice file cannot be found' 2> {tmp_dir}/pig/dog.md")[0]
        assert output == "Alice file cannot be found\n", f'Expected stdout but got "{output}"'

        # Test 3: Verify stderr file is empty when echo (no error) is redirected
        file_path = f"{tmp_dir}/pig/dog.md"
        file_size = os.path.getsize(file_path)
        assert file_size == 0, f'Expected empty file but got {file_size} bytes'

        # Test 4: Mix of stdout and stderr redirection
        output = shell_tester.execute(f"cat {tmp_dir}/dog/pear nonexistent 2> {tmp_dir}/pig/pig.md")[0]
        assert output == "pear\n", f'Expected "pear" but got "{output}"'

        # Test 5: Verify stderr was captured
        output = shell_tester.execute(f"cat {tmp_dir}/pig/pig.md")[0]
        assert "nonexistent: No such file or directory" in output, f'Expected error message but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)


def test_append_stdout(shell_executable):
    """Test that the shell correctly appends stdout to files.

    This test verifies:
    1. The >> operator appends stdout to a file instead of overwriting
    2. The 1>> operator explicitly appends stdout to a file
    3. Multiple append operations add content sequentially
    4. First write with > creates file, subsequent >> appends
    """
    tmp_dir = create_test_environment()
    try:
        # Create test files
        ensure_dir(f"{tmp_dir}/ant")
        write_file(f"{tmp_dir}/ant/apple", "apple")
        write_file(f"{tmp_dir}/ant/orange", "orange")
        write_file(f"{tmp_dir}/ant/strawberry", "strawberry")
        ensure_dir(f"{tmp_dir}/owl")

        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Append stdout using >>
        shell_tester.execute(f"ls -1 {tmp_dir}/ant >> {tmp_dir}/owl/ant.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/owl/ant.md")
        assert output == ["apple\n", "orange\n", "strawberry\n"], f'Expected file listing but got "{output}"'

        # Test 2: Append stdout using 1>> multiple times
        shell_tester.execute(f"echo 'Hello James' 1>> {tmp_dir}/owl/cow.md", no_output=True)
        shell_tester.execute(f"echo 'Hello David' 1>> {tmp_dir}/owl/cow.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/owl/cow.md")
        assert output == ["Hello James\n", "Hello David\n"], f'Expected appended content but got "{output}"'

        # Test 3: Write with > then append with >>
        shell_tester.execute(f"echo \"List of files: \" > {tmp_dir}/owl/fox.md", no_output=True)
        shell_tester.execute(f"ls -1 {tmp_dir}/ant >> {tmp_dir}/owl/fox.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/owl/fox.md")
        assert output == ["List of files: \n", "apple\n", "orange\n", "strawberry\n"], f'Expected mixed content but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)


def test_append_stderr(shell_executable):
    """Test that the shell correctly appends stderr to files.

    This test verifies:
    1. The 2>> operator appends stderr to a file instead of overwriting
    2. Multiple stderr redirections append content sequentially
    3. Stdout is printed to console when stderr is appended
    4. Multiple error messages accumulate in the redirected file
    """
    tmp_dir = create_test_environment()
    try:
        # Create test directories
        ensure_dir(f"{tmp_dir}/pig")
        ensure_dir(f"{tmp_dir}/cow")

        shell_tester = ShellTester(shell_executable)
        shell_tester.start_shell()

        # Test 1: Redirect stderr with >> (should create file or append)
        shell_tester.execute(f"ls -1 nonexistent >> {tmp_dir}/pig/cow.md")
        file_path = f"{tmp_dir}/pig/cow.md"
        file_size = os.path.getsize(file_path)
        assert file_size == 0, f'Expected empty file with >> (stdout) but got {file_size} bytes'

        # Test 2: Append stderr using 2>>
        shell_tester.execute(f"ls -1 nonexistent 2>> {tmp_dir}/pig/dog.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/pig/dog.md")[0]
        assert "No such file or directory" in output, f'Expected error message but got "{output}"'

        # Test 3: Stdout appears while stderr is appended
        output = shell_tester.execute(f"echo \"James says Error\" 2>> {tmp_dir}/pig/fox.md")[0]
        assert output == "James says Error\n", f'Expected stdout but got "{output}"'

        # Test 4: Multiple stderr messages accumulate
        shell_tester.execute(f"cat nonexistent 2>> {tmp_dir}/pig/fox.md", no_output=True)
        shell_tester.execute(f"ls -1 nonexistent 2>> {tmp_dir}/pig/fox.md", no_output=True)
        output = shell_tester.execute(f"cat {tmp_dir}/pig/fox.md")
        assert len(["No such file or directory" in x for x in output]) >= 2, f'Expected multiple error messages but got "{output}"'

        shell_tester.stop()
    finally:
        cleanup_test_environment(tmp_dir)
