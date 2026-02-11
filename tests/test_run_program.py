from shell_test_utils import ShellTester, write_file, create_test_environment, cleanup_test_environment


def test_run_program(shell_executable):
    """Test that the shell can run programs with arguments correctly.

    This test uses common preinstalled executables (cat, ls, etc.)
    to verify that programs receive the correct arguments.
    """
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()
    write_file(f"{tmp_dir}/test.txt", "Hello, World!\n")
    output = shell_tester.execute(f"cat {tmp_dir}/test.txt")
    assert output == "Hello, World!", f'Expected "Hello, World!" but got "{output}"'
    cleanup_test_environment(tmp_dir)

    output = shell_tester.execute("ls -d /tmp")
    assert output == "/tmp", f'Expected "/tmp" but got "{output}"'

    shell_tester.stop()
