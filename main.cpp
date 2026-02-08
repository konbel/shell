#include <iostream>
#include <vector>
#include <sstream>
#include <unordered_map>
#include <unistd.h>
#include <filesystem>
#include <sys/wait.h>

std::vector<std::string> path;

#pragma region util

std::string find_executable(const std::string &executable) {
    for (const std::string &dir: path) {
        std::string full_path = std::filesystem::path(dir) / executable;
        if (access(full_path.c_str(), X_OK) == 0) {
            return full_path;
        }
    }
    return "";
}

void exec(const std::string &full_path, const std::vector<std::string> &args) {
    if (const pid_t pid = fork(); pid == 0) {
        // child process
        const size_t argc = args.size() + 1;
        const auto args_cstr = new char *[argc];
        args_cstr[0] = const_cast<char *>(full_path.c_str());
        for (int i = 0; i < args.size(); i++) {
            args_cstr[i + 1] = const_cast<char *>(args[i].c_str());
        }

        execv(full_path.c_str(), args_cstr);
    } else if (pid > 0) {
        // parent process
        int status;
        waitpid(pid, &status, 0);
    } else {
        perror("fork");
    }
}

#pragma endregion // util

#pragma region builtins

void echo(const std::vector<std::string> &args);
void type(const std::vector<std::string> &args);

void exit_builtin(const std::vector<std::string> &args) {
    exit(EXIT_SUCCESS);
}

std::unordered_map<std::string, void (*)(const std::vector<std::string> &)> builtins = {
    {std::string("exit"), &exit_builtin},
    {std::string("echo"), &echo},
    {std::string("type"), &type},
};

void echo(const std::vector<std::string> &args) {
    std::stringstream output;
    for (int i = 0; i < args.size(); i++) {
        output << args[i];
        if (i != args.size() - 1) {
            output << " ";
        }
    }
    output << std::endl;
    std::cout << output.str();
}

void type(const std::vector<std::string> &args) {
    if (args.empty()) {
        std::cout << "type: not enough arguments" << std::endl;
        return;
    }

    if (builtins.contains(args[0])) {
        std::cout << args[0] << " is a shell builtin" << std::endl;
        return;
    }

    const std::string full_path = find_executable(args[0]);
    if (!full_path.empty()) {
        std::cout << args[0] << " is " << full_path << std::endl;
        return;
    }

    std::cout << args[0] << " not found" << std::endl;
}

#pragma endregion // builtins

void print_prompt() {
    std::cout << "$ ";
}

void eval(const std::string &command, const std::vector<std::string> &args) {
    // handle built in commands
    if (builtins.contains(command)) {
        builtins[command](args);
        return;
    }

    // handle external executables
    if (const std::string full_path = find_executable(command); !full_path.empty()) {
        exec(full_path, args);
        return;
    }

    std::cout << command << ": command not found" << std::endl;
}

int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    std::string buffer;

    std::string path_env = std::getenv("PATH");
    std::stringstream path_stream(path_env);

    while (std::getline(path_stream, buffer, ':')) {
        path.push_back(buffer);
        buffer.clear();
    }

    print_prompt();

    std::istringstream input(buffer);
    std::string command;
    std::vector<std::string> args;

    while (std::getline(std::cin, buffer)) {
        input.str(buffer);
        buffer.clear();

        input >> command;
        while (input) {
            input >> buffer;
            args.push_back(buffer);
            buffer.clear();
        }

        args.pop_back();
        eval(command, args);

        buffer.clear();
        input.clear();
        command.clear();
        args.clear();

        print_prompt();
    }

    return EXIT_SUCCESS;
}
