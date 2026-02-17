#include "commands.h"

#include <fstream>
#include <iostream>

#include "utils.h"

int stdout_fd = -1;
int stdin_fd = -1;
int stderr_fd = -1;

void read_history(const std::string &file_path) {
    std::ifstream file(file_path);
    if (!file.is_open()) {
        // std::cout << "history: " << file_path << ": No such file or directory" << std::endl;
        return;
    }

    std::string buffer;
    while (std::getline(file, buffer)) {
        history_cache.push_back(buffer);
    }

    file.close();
}

void write_history(const std::string &file_path) {
    std::ofstream file(file_path);
    if (!file.is_open()) {
        // std::cout << "history: " << file_path << ": No such file or directory" << std::endl;
        return;
    }

    for (const std::string &entry: history_cache) {
        file << entry << std::endl;
    }

    file.close();
}

void append_history(const std::string &file_path) {
    std::ofstream file(file_path, std::ios::app);
    if (!file.is_open()) {
        // std::cout << "history: " << file_path << ": No such file or directory" << std::endl;
        return;
    }

    for (const std::string &entry: history_cache) {
        file << entry << std::endl;
    }

    file.close();
}

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

void redirect_io(const int output_fd = -1, const int input_fd = -1, const int error_fd = -1) {
    stdout_fd = dup(STDOUT_FILENO);
    stdin_fd = dup(STDIN_FILENO);
    stderr_fd = dup(STDERR_FILENO);

    if (output_fd != -1) {
        dup2(output_fd, STDOUT_FILENO);
    }

    if (input_fd != -1) {
        dup2(input_fd, STDIN_FILENO);
    }

    if (error_fd != -1) {
        dup2(error_fd, STDERR_FILENO);
    }
}

void restore_io() {
    if (stdout_fd != 0) {
        dup2(stdout_fd, STDOUT_FILENO);
        close(stdout_fd);
        stdout_fd = -1;
    }

    if (stdin_fd != 0) {
        dup2(stdin_fd, STDIN_FILENO);
        close(stdin_fd);
        stdin_fd = -1;
    }

    if (stderr_fd != 0) {
        dup2(stderr_fd, STDERR_FILENO);
        close(stderr_fd);
        stderr_fd = -1;
    }
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

void history(const std::string &input, const std::vector<std::string> &args) {
    // clear
    if (args.size() > 1 && args[1] == "-c") {
        history_cache.clear();
        history_index = 0;
        return;
    }

    // load from file
    if (args.size() > 2) {
        if (args[1] == "-r") {
            read_history(args[2]);
            return;
        }

        if (args[1] == "-w") {
            write_history(args[2]);
            return;
        }

        if (args[1] == "-a") {
            append_history(args[2]);
            return;
        }
    }

    // print history
    size_t n = 999;
    if (args.size() > 1) {
        if (!is_number(args[1])) {
            std::cout << "history: " << args[1] << ": numeric argument required" << std::endl;
            return;
        }

        if (args.size() > 2) {
            std::cout << "history: too many arguments" << std::endl;
            return;
        }

        n = std::stoul(args[1]);
    }
    if (n > history_cache.size()) {
        n = history_cache.size();
    }

    for (size_t i = history_cache.size() - n; i < history_cache.size(); i++) {
        std::cout << "  " << i + 1 << "  " << history_cache[i] << std::endl;
    }
}

int exec(const std::string &executable, const std::vector<std::string> &args, const int output_fd = -1,
         const int input_fd = -1) {
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

            // redirect input & output
            if (output_fd != -1) {
                dup2(output_fd, STDOUT_FILENO);
            }

            if (input_fd != -1) {
                dup2(input_fd, STDIN_FILENO);
            }

            execv(executable.c_str(), argv);
            perror("exec");
            delete[] argv;
            break;
        }
        default:
            return pid;
    }
    return -1;
}
