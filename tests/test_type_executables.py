from shell_test_utils import ShellTester, ensure_dir, write_file
import os


def test_type_executables(shell_executable):
    """Create test executables in /tmp and verify `type` reports system binaries and the correct executable.

    Start a fresh shell subprocess with PATH set via the env argument (no in-shell `export`).
    """

    # Use the same shell program path that the test runner is using
    shell_tester = ShellTester(shell_executable)

    # Prepare env with PATH updated without using the shell's export builtin
    current_path = os.environ.get("PATH", "")
    new_path = "/tmp/rat:/tmp/bee:/tmp/pig:" + current_path
    shell_tester.start_shell(env={"PATH": new_path})

    try:
        # Setup: create directories and files under /tmp
        shell_tester.execute("mkdir -p /tmp/rat /tmp/bee /tmp/pig", True)

        shell_tester.execute("touch /tmp/rat/my_exe", True)
        shell_tester.execute("touch /tmp/pig/my_exe", True)
        shell_tester.execute("touch /tmp/bee/my_exe", True)

        # Make only /tmp/bee/my_exe executable
        shell_tester.execute("chmod 644 /tmp/rat/my_exe", True)
        shell_tester.execute("chmod 644 /tmp/pig/my_exe", True)
        shell_tester.execute("chmod 755 /tmp/bee/my_exe", True)

        # Now query `type` for a few system commands and our test executable
        cases = [
            ("type cat", "cat is /usr/bin/cat"),
            ("type cp", "cp is /usr/bin/cp"),
            ("type mkdir", "mkdir is /usr/bin/mkdir"),
            ("type my_exe", "my_exe is /tmp/bee/my_exe"),
            ("type invalid_mango_command", "invalid_mango_command not found"),
            ("type invalid_grape_command", "invalid_grape_command not found"),
        ]

        for cmd, expected in cases:
            output = shell_tester.execute(cmd)[0]
            assert output == expected + "\n", f'Expected "{expected}" but got "{output}"'
    finally:
        shell_tester.stop()
