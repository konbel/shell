#include <iostream>
#include <vector>
#include <sstream>
#include <unordered_map>
#include <unistd.h>
#include <filesystem>

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

std::vector<std::string> split(const std::string &str, const char delimiter) {
    std::string buffer;
    std::vector<std::string> parts;
    std::istringstream ss(str);

    while (std::getline(ss, buffer, delimiter)) {
        parts.push_back(buffer);
    }

    return parts;
}

#pragma endregion // util

#pragma region builtins

void echo(const std::string &input, const std::vector<std::string> &args);
void type(const std::string &input, const std::vector<std::string> &args);

void exit_builtin(const std::string& input, const std::vector<std::string> &args) {
    exit(EXIT_SUCCESS);
}

std::unordered_map<std::string, void (*)(const std::string&, const std::vector<std::string> &)> builtins = {
    {std::string("exit"), &exit_builtin},
    {std::string("echo"), &echo},
    {std::string("type"), &type},
};

void echo(const std::string &input, const std::vector<std::string> &args) {
    std::cout << input.substr(5) << std::endl;
}

void type(const std::string &input, const std::vector<std::string> &args) {
    for (auto &arg : args) {
        if (builtins.contains(arg)) {
            std::cout << arg << " is a shell builtin" << std::endl;
            continue;
        }

        if (auto full_path = find_executable(arg); !full_path.empty()) {
            std::cout << arg << " is " << full_path << std::endl;
            continue;
        }

        std::cout << args[0] << " not found" << std::endl;
    }
}

#pragma endregion // builtins

void print_prompt() {
    std::cout << "$ ";
}

void eval(const std::string &input) {
    auto args = split(input, ' ');
    const std::string command = args[0];
    args.erase(args.begin());

    // handle built in commands
    if (builtins.contains(command)) {
        builtins[command](input, args);
        return;
    }

    // handle external executables
    if (const std::string full_path = find_executable(command); !full_path.empty()) {
        std::system(input.c_str());
        return;
    }

    std::cout << command << ": command not found" << std::endl;
}

int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    std::string buffer;

    // parse PATH environment variable
    const std::string path_env = std::getenv("PATH");
    std::stringstream path_stream(path_env);
    while (std::getline(path_stream, buffer, ':')) {
        path.push_back(buffer);
        buffer.clear();
    }

    // REPL
    print_prompt();
    while (std::getline(std::cin, buffer)) {
        eval(buffer);
        buffer.clear();
        print_prompt();
    }

    return EXIT_SUCCESS;
}
