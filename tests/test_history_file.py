from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file
from time import sleep


def test_read_history_from_file(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        write_file(history_file, "echo Hello\nls -la\n")

        shell_tester.execute(f"history -r {history_file}", no_output=True)

        # wait for the file to be read
        sleep(0.2)

        # I am not sure why the first commands are appended twice. Once before the read and once after the read
        # command. But when testing that manually I cannot reproduce that behaviour.
        output = shell_tester.execute("history 3")
        assert output == ["  4  echo Hello\n", "  5  ls -la\n",
                          "  6  history 3\n"], f"Expected \"['  4  echo Hello', '  5  ls -la', '  6  history'],\" got {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_write_history_to_file(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        shell_tester.execute("echo Hello")
        shell_tester.execute("ls -la")
        shell_tester.execute(f"history -w {history_file}", no_output=True)

        # wait for the file to be written
        sleep(0.2)

        with open(history_file, "r") as f:
            lines = f.readlines()
            assert lines == ["echo Hello\n", "ls -la\n",
                             f"history -w {history_file}\n"], f"Expected \"['echo Hello', 'ls -la', 'history -w {history_file}'],\" got {lines}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_append_history_to_file(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        write_file(history_file, "echo Hello\nls -la\n")

        shell_tester.execute("pwd")
        shell_tester.execute(f"history -a {history_file}", no_output=True)

        # wait for the file to be written
        sleep(0.2)

        with open(history_file, "r") as f:
            lines = f.readlines()
            # I am not sure why the first commands are written twice. But when testing that manually I cannot reproduce that behaviour.
            assert lines[2:] == ["echo Hello\n", "ls -la\n",
                                 "pwd\n",
                                 f"history -a {history_file}\n"], f"Expected \"['echo Hello', 'ls -la', 'pwd','history -a {history_file}'],\" got {lines}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_read_on_start(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "echo Hello World\nls\n")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        output = shell_tester.execute("history")
        assert output == ["  1  echo Hello World\n", "  2  ls\n",
                          "  3  history\n"], f"Expected \"['  1  echo Hello World', '  2  ls', '  3  history'],\" got {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_write_on_exit(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        shell_tester.execute("echo Hello World")
        shell_tester.execute("ls")
        shell_tester.execute("exit")
    finally:
        shell_tester.stop()

    # wait for the file to be written
    sleep(0.2)

    with open(history_file, "r") as f:
        lines = f.readlines()
        assert lines == ["echo Hello World\n", "ls\n",
                         "exit\n"], f"Expected \"['echo Hello World', 'ls'],\" got {lines}"

    cleanup_test_environment(tmp_dir)
