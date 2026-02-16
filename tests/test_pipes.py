from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file


def test_dual_command_pipe(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()
    write_file(f"{tmp_dir}/foo/file", "Hello, World!")
    write_file(f"{tmp_dir}/bar/file",
               "Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7\nLine 8\nLine 9\nLine 10\n")

    try:
        output = shell_tester.execute(f"cat {tmp_dir}/foo/file | wc -w")[0]
        assert output == "2\n", f"Expected \"2\", got '{output}'"

        output = shell_tester.execute(f"tail -n 5 {tmp_dir}/bar/file | head -n 3")
        assert output == ["Line 6\n", "Line 7\n", "Line 8\n"], f"Expected ['Line 6', 'Line 7', 'Line 8'], got {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_pipes_with_builtins(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        output = shell_tester.execute("echo raspberry\\nblueberry | wc -w")[0]
        assert output == "1\n", f"Expected \"1\", got '{output}'"

        output = shell_tester.execute("ls | type exit")[0]
        assert output == "exit is a shell builtin\n", f"Expected \"exit is a shell builtin\", got '{output}'"
    finally:
        shell_tester.stop()


def test_multi_command_pipelines(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()
    write_file(f"{tmp_dir}/foo/file", "apple\nbanana\ncherry\n")

    try:
        output = shell_tester.execute(f"cat {tmp_dir}/foo/file | head -n 3 | wc -c")[0]
        assert output == "20\n", f"Expected \"20\", got '{output}'"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)
