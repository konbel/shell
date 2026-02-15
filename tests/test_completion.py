from shell_test_utils import ShellTester, create_test_environment, cleanup_test_environment, write_file
import os


def test_builtin_completion(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        output = shell_tester.execute("ech\tCompletion")[0]
        assert output == "Completion\n", f"Expected \"Completion\", got '{output}'"

        output = shell_tester.execute("ty\t exit")[0]
        assert output == "exit is a shell builtin\n", f"Expected \"exit is a shell builtin\", got \"{output}\""
    finally:
        shell_tester.stop()


def test_missing_completions(shell_executable):
    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell()

    try:
        output = shell_tester.execute("xyz\t")[0]
        assert output == "\axyz: command not found\n", f"Expected \"xyz: command not found\", got \"{output}\""
    finally:
        shell_tester.stop()


def test_executable_completion(shell_executable):
    tmp_dir = create_test_environment()
    write_file(f"{tmp_dir}/test_executable", "#!/bin/sh\necho Successfull completion\n")
    os.chmod(f"{tmp_dir}/test_executable", 0o755)

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"PATH": tmp_dir})

    try:
        output = shell_tester.execute("test_\t")[0]
        assert output == "Successfull completion\n", f"Expected \"Successfull completion\", got '{output}'"
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)


def test_multiple_completion(shell_executable):
    tmp_dir = create_test_environment()
    write_file(f"{tmp_dir}/xyz_quz", "")
    os.chmod(f"{tmp_dir}/xyz_quz", 0o755)
    write_file(f"{tmp_dir}/xyz_bar", "")
    os.chmod(f"{tmp_dir}/xyz_bar", 0o755)
    write_file(f"{tmp_dir}/xyz_buz", "")
    os.chmod(f"{tmp_dir}/xyz_buz", 0o755)

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"PATH": tmp_dir})

    try:
        output = shell_tester.execute("xyz_\t\t")
        assert output[:2] == ["\x07\n", "xyz_bar\txyz_buz\txyz_quz\n"], f"Expected \"xyz_foo\txyz_bar\txyz_buz\", got \"{output}\""
    finally:
        shell_tester.stop()


def test_longest_common_prefix(shell_executable):
    tmp_dir = create_test_environment()
    write_file(f"{tmp_dir}/xyz_quz", "#!/bin/sh\necho Hello World")
    os.chmod(f"{tmp_dir}/xyz_quz", 0o755)
    write_file(f"{tmp_dir}/xyz_bar", "")
    os.chmod(f"{tmp_dir}/xyz_bar", 0o755)
    write_file(f"{tmp_dir}/xyz_buz", "")
    os.chmod(f"{tmp_dir}/xyz_buz", 0o755)

    shell_tester = ShellTester(shell_executable)
    shell_tester.start_shell(env={"PATH": tmp_dir})

    try:
        output = shell_tester.execute("x\tquz")[0]
        assert output == "Hello World\n", f"Expected \"Hello World\", got \"{output}\""
    finally:
        shell_tester.stop()
