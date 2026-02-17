from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file


def test_read_history_from_file(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()

    try:
        history_file_path = f"{tmp_dir}/history"
        write_file(history_file_path, "echo Hello\nls -la\n")

        shell_tester.execute(f"history -r {history_file_path}", no_output=True)
        output = shell_tester.execute("history 3")
        assert output == ["  2  echo Hello\n", "  3  ls -la\n",
                          "  4  history 3\n"], f"Expected \"['  1  echo Hello', '  2  ls -la', '  3  history'],\" got {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_write_history_to_file(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()

    try:
        history_file_path = f"{tmp_dir}/history"
        shell_tester.execute("echo Hello")
        shell_tester.execute("ls -la")
        shell_tester.execute(f"history -w {history_file_path}", no_output=True)

        # wait for the file to be written
        from time import sleep
        sleep(0.2)

        with open(history_file_path, "r") as f:
            lines = f.readlines()
            assert lines == ["echo Hello\n", "ls -la\n",
                             f"history -w {history_file_path}\n"], f"Expected \"['echo Hello', 'ls -la', 'history -w {history_file_path}'],\" got {lines}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_append_history_to_file(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    tmp_dir = create_test_environment()

    try:
        history_file_path = f"{tmp_dir}/history"
        write_file(history_file_path, "echo Hello\nls -la\n")

        shell_tester.execute("pwd")
        shell_tester.execute(f"history -a {history_file_path}", no_output=True)

        # wait for the file to be written
        from time import sleep
        sleep(0.2)

        with open(history_file_path, "r") as f:
            lines = f.readlines()
            assert lines == ["echo Hello\n", "ls -la\n",
                             "pwd\n",
                             f"history -a {history_file_path}\n"], f"Expected \"['echo Hello', 'ls -la', 'pwd','history -a {history_file_path}'],\" got {lines}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)
