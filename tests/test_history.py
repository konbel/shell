from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file


def test_history(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        shell_tester.execute("echo Hello World")
        shell_tester.execute("echo Another Command")
        output = shell_tester.execute("history")
        assert output == ["  1  echo Hello World\n", "  2  echo Another Command\n",
                          "  3  history\n"], f"Expected history output to match the executed commands, but got: {output}"

        output = shell_tester.execute("history 2")
        assert output == ["  3  history\n",
                          "  4  history 2\n"], f"Expected history output to match the executed commands, but got: {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_up_arrow(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        shell_tester.execute("echo First Command")
        shell_tester.execute("echo Second Command")

        output = shell_tester.execute("\x1b[A\x1b[A\n")[0].replace("\x08 \x08", "")
        assert output.strip() == "First Command", f"Expected \"First Command\", but got: {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_down_arrow(shell_executable):
    tmp_dir = create_test_environment()
    history_file = f"{tmp_dir}/history"
    write_file(history_file, "")

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"HISTFILE": history_file})

    try:
        shell_tester.execute("echo First Command")
        shell_tester.execute("echo Second Command")
        shell_tester.execute("echo Third Command")

        output = shell_tester.execute("\x1b[A\x1b[A\x1b[A\x1b[B\x1b[B\n")[0].replace("\x08 \x08", "")
        assert output == "Third Command\n", f"Expected \"Third Command\", but got: {output}"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)
