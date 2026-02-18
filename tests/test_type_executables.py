from shell_test_utils import ShellTester, ensure_dir, write_file, create_test_environment, cleanup_test_environment
import os


def test_type_executables(shell_executable):
    """Create test executables in {tmp_dir} and verify `type` reports system binaries and the correct executable.

    Start a fresh shell subprocess with PATH set via the env argument (no in-shell `export`).
    """

    tmp_dir = create_test_environment()

    # Use the same shell program path that the test runner is using
    shell_tester = ShellTester(shell_executable)

    # Prepare env with PATH updated without using the shell's export builtin
    current_path = os.environ.get("PATH", "")
    new_path = f"{tmp_dir}/rat:{tmp_dir}/bee:{tmp_dir}/pig:" + current_path
    shell_tester.start_shell(env={"PATH": new_path})

    try:
        # Setup: create directories and files under {tmp_dir}
        shell_tester.execute(f"mkdir -p {tmp_dir}/rat {tmp_dir}/bee {tmp_dir}/pig", True)

        shell_tester.execute(f"touch {tmp_dir}/rat/my_exe", True)
        shell_tester.execute(f"touch {tmp_dir}/pig/my_exe", True)
        shell_tester.execute(f"touch {tmp_dir}/bee/my_exe", True)

        # Make only {tmp_dir}/bee/my_exe executable
        shell_tester.execute(f"chmod 644 {tmp_dir}/rat/my_exe", True)
        shell_tester.execute(f"chmod 644 {tmp_dir}/pig/my_exe", True)
        shell_tester.execute(f"chmod 755 {tmp_dir}/bee/my_exe", True)

        # Now query `type` for a few system commands and our test executable
        cases = [
            ("type cat", "cat is /usr/bin/cat"),
            ("type cp", "cp is /usr/bin/cp"),
            ("type mkdir", "mkdir is /usr/bin/mkdir"),
            ("type my_exe", f"my_exe is {tmp_dir}/bee/my_exe"),
            ("type invalid_mango_command", "invalid_mango_command not found"),
            ("type invalid_grape_command", "invalid_grape_command not found"),
        ]

        for cmd, expected in cases:
            output = shell_tester.execute(cmd)[0]
            assert output == expected + "\n", f'Expected "{expected}" but got "{output}"'
    finally:
        shell_tester.stop()
        cleanup_test_environment(tmp_dir)
