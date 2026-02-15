#include "commands.h"

#include <iostream>
#include <sys/wait.h>

#include "utils.h"

void build_executables_cache() {
    path = parse_path();
    for (const auto &dir: path) {
        if (!std::filesystem::exists(dir) || !std::filesystem::is_directory(dir)) {
            continue;
        }

        for (const auto &entry: std::filesystem::directory_iterator(dir)) {
            if (access(entry.path().c_str(), X_OK) == 0) {
                executables_cache[entry.path().filename()] = entry.path();
            }
        }
    }
}

std::unordered_set<std::string> autocomplete_builtin(const std::string &input) {
    std::unordered_set<std::string> results;

    for (const auto &key: builtins | std::views::keys) {
        if (key.starts_with(input)) {
            results.insert(key);
        }
    }

    return results;
}

std::unordered_set<std::string> autocomplete_executable(const std::string &input) {
    std::unordered_set<std::string> results;

    for (const auto &key: executables_cache | std::views::keys) {
        if (key.starts_with(input)) {
            results.insert(key);
        }
    }

    return results;
}

void exit_builtin(const std::string &input, const std::vector<std::string> &args) {
    int exit_code = EXIT_SUCCESS;

    if (args.size() == 2 && is_number(args[1])) {
        exit_code = std::stoi(args[1]);
    } else if (args.size() > 2) {
        std::cout << "exit: too many arguments" << std::endl;
        return;
    }

    exit(exit_code);
}

void echo(const std::string &input, const std::vector<std::string> &args) {
    for (int i = 1; i < args.size(); i++) {
        std::cout << args[i];
        if (i < args.size() - 1) {
            std::cout << " ";
        }
    }
    std::cout << std::endl;
}

void type(const std::string &input, const std::vector<std::string> &args) {
    for (int i = 1; i < args.size(); i++) {
        const std::string &arg = args[i];

        if (builtins.contains(arg)) {
            std::cout << arg << " is a shell builtin" << std::endl;
            continue;
        }

        if (auto full_path = find_executable(arg); !full_path.empty()) {
            std::cout << arg << " is " << full_path << std::endl;
            continue;
        }

        std::cout << args[i] << " not found" << std::endl;
    }
}

void pwd(const std::string &input, const std::vector<std::string> &args) {
    std::cout << getcwd(nullptr, 0) << std::endl;
}

void cd(const std::string &input, const std::vector<std::string> &args) {
    if (args.size() > 2) {
        std::cout << "cd: too many arguments" << std::endl;
        return;
    }

    std::string dir = getenv("HOME");

    if (args.size() > 1 && !args[1].empty() && args[1][0] == '~') {
        if (args[1].length() > 1) {
            for (int i = 1; i < args[1].length(); i++) {
                dir += args[1][i];
            }
        }
    } else if (args.size() > 1 && !args[1].empty()) {
        dir = args[1];
    }

    if (chdir(dir.c_str()) != 0) {
        std::cout << "cd: " << args[1] << ": No such file or directory" << std::endl;
    }
}

void exec(const std::string &executable, const std::vector<std::string> &args) {
    switch (const int pid = fork()) {
        case -1:
            perror("fork");
            break;
        case 0: {
            const auto argv = new char *[args.size() + 1];
            for (int i = 0; i < args.size(); i++) {
                argv[i] = const_cast<char *>(args[i].c_str());
            }
            argv[args.size()] = nullptr;

            execv(executable.c_str(), argv);
            perror("exec");
            delete[] argv;
            break;
        }
        default:
            waitpid(pid, nullptr, 0);
    }
}
