"""Test runner for shell tests"""
import sys
import inspect
import importlib
import os


def discover_test_modules(test_dir="."):
    """Discover all test modules in the test directory"""
    test_modules = []
    for filename in os.listdir(test_dir):
        if filename.startswith("test_") and filename.endswith(".py"):
            module_name = filename[:-3]  # Remove .py extension
            test_modules.append(module_name)
    return test_modules


def discover_test_functions(module):
    """Discover all test functions in a module"""
    test_functions = []
    for name, obj in inspect.getmembers(module):
        if name.startswith("test_") and inspect.isfunction(obj):
            test_functions.append((name, obj))
    return test_functions


def run_tests(shell_executable):
    """Discover and run all test functions"""
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)

    # Discover test modules
    test_modules = discover_test_modules(".")

    if not test_modules:
        print("No test modules found")
        return 0

    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    errors = []

    # Run tests from each module
    for module_name in test_modules:
        try:
            module = importlib.import_module(module_name)
            test_functions = discover_test_functions(module)

            if not test_functions:
                continue

            for test_name, test_func in test_functions:
                total_tests += 1

                try:
                    test_func(shell_executable)

                    print(f"✓ {module_name}.{test_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"✗ {module_name}.{test_name}")
                    failed_tests += 1
                    errors.append((module_name, test_name, str(e)))

        except ImportError as e:
            print(f"Error importing {module_name}: {e}")
            failed_tests += 1

    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")

    if errors:
        print("\nFailures:")
        for module_name, test_name, error in errors:
            print(f"  {module_name}.{test_name}: {error}")

    return 0 if failed_tests == 0 else 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_runner.py <shell_executable>")
        sys.exit(1)

    exit_code = run_tests(sys.argv[1])
    sys.exit(exit_code)
