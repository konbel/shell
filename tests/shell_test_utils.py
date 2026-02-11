"""Utility functions for shell testing"""
import subprocess
import os
import tempfile
import shutil
import select


class ShellTester:
    """Helper class to run shell commands through the shell program"""

    def __init__(self, shell_program_path="./shell"):
        self.shell_program_path = shell_program_path
        self.process = None

    def start_shell(self, env=None):
        """Start the shell process"""
        full_env = os.environ.copy()
        if env:
            full_env.update(env)

        try:
            self.process = subprocess.Popen(
                [self.shell_program_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                env=full_env,
                cwd=os.path.dirname(self.shell_program_path) or "."
            )
        except FileNotFoundError:
            raise RuntimeError(f"Shell program not found at {self.shell_program_path}")

    def execute(self, command, no_output=False):
        """Execute a command and return the output.

        This will wait up to `timeout` seconds for output to be available
        on the subprocess stdout. If nothing is available within the timeout
        a RuntimeError is raised. This avoids blocking indefinitely on
        readline().
        """
        if not self.process:
            raise RuntimeError("Shell process not started. Call start() first.")

        try:
            # send the command
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()

            if no_output:
                return ""

            output = self.process.stdout.readline()
            while True:
                if "$ " in output:
                    break
                output = self.process.stdout.readline()

            # try to extract prompt and the first line
            if "$ " in output:
                output = output[output.rfind("$ ") + 2:].split("\n")[0]
            else:
                # prompt not found in the line; return the raw line stripped
                output = output.strip()

            return output
        except subprocess.TimeoutExpired:
            self.process.kill()
            raise RuntimeError(f"Command timed out: {command}")

    def is_alive(self):
        """Check if the shell process is still running"""
        if not self.process:
            return False
        return self.process.poll() is None

    def wait_for_exit(self, timeout=2):
        """Wait for the shell process to exit naturally.

        Returns True if the process exited, False if timeout occurred.
        """
        if not self.process:
            return True
        try:
            self.process.wait(timeout=timeout)
            return True
        except subprocess.TimeoutExpired:
            return False

    def stop(self):
        """Stop the shell process"""
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


def create_test_environment(temp_dir=None):
    """Create a temporary test environment"""
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()
    return temp_dir


def cleanup_test_environment(temp_dir):
    """Clean up temporary test environment"""
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def ensure_dir(path):
    """Ensure a directory exists"""
    os.makedirs(path, exist_ok=True)


def write_file(path, content):
    """Write content to a file"""
    ensure_dir(os.path.dirname(path))
    with open(path, 'w') as f:
        f.write(content)


def read_file(path):
    """Read content from a file"""
    with open(path, 'r') as f:
        return f.read()


def file_exists(path):
    """Check if a file exists"""
    return os.path.exists(path)


def file_is_empty(path):
    """Check if a file is empty"""
    return os.path.getsize(path) == 0
