from shell_test_utils import ShellTester, write_file, create_test_environment, cleanup_test_environment


def test_run_program(shell_executable):
    """Test that the shell can run programs with arguments correctly.

    This test uses common preinstalled executables (cat, ls, etc.)
    to verify that programs receive the correct arguments.
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()
    try:
        write_file(f"{tmp_dir}/test.txt", "Hello, World!\n")
        output = shell_tester.execute(f"cat {tmp_dir}/test.txt")[0]
        assert output == "Hello, World!\n", f'Expected "Hello, World!" but got "{output}"'

        output = shell_tester.execute("ls -d /tmp")[0]
        assert output == "/tmp\n", f'Expected "/tmp" but got "{output}"'
    finally:
        cleanup_test_environment(tmp_dir)
        shell_tester.stop()
