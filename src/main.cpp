#include <iostream>
#include <pwd.h>
#include <regex>

#include "commands.h"
#include "utils.h"
#include "graphics.h"

// session and user information
uid_t uid;
passwd *pw;
char hostname[256];
int stdout_fd;
int stderr_fd;

void print_prompt() {
    const std::string dir = std::regex_replace(getcwd(nullptr, 0), std::regex(getenv("HOME")), "~");

    std::cout << ORANGE << BOLD << pw->pw_name << "@" << hostname << RESET << ":" << BLUE << BOLD
            << dir << RESET << "$ ";
}

inline bool check_redirect_destination(const std::vector<std::string> &arg, int i) {
    if (i + 1 >= arg.size()) {
        std::cout << "syntax error near unexpected token `newline'" << std::endl;
        return false;
    }
    return true;
}

void eval(const std::string &input) {
    const auto command = parse_command(input);
    const auto args = parse_args(input.substr(command.length()));

    // check for output and error redirecting
    std::vector<std::string> filtered_args;
    bool redirecting_output = false;
    bool redirecting_error = false;
    for (int i = 0; i < args.size(); i++) {
        const std::string &arg = args[i];
        const std::string &output = args[i + 1];

        if (arg == ">" || arg == "1>") {
            if (check_redirect_destination(args, i)) {
                freopen(output.c_str(), "w", stdout);
                redirecting_output = true;
            }
            break;
        }

        if (arg == "2>") {
            if (check_redirect_destination(args, i)) {
                freopen(output.c_str(), "w", stderr);
                redirecting_error = true;
            }
            break;
        }

        if (arg == ">>" || arg == "1>>") {
            if (check_redirect_destination(args, i)) {
                freopen(output.c_str(), "a", stdout);
                redirecting_output = true;
            }
            break;
        }

        if (arg == "2>>") {
            if (check_redirect_destination(args, i)) {
                freopen(output.c_str(), "a", stderr);
                redirecting_error = true;
            }
            break;
        }

        filtered_args.push_back(arg);
    }

    // handle command
    if (builtins.contains(command)) {
        builtins[command](input, filtered_args);
    } else if (const std::string full_path = find_executable(command); !full_path.empty()) {
        std::system(input.c_str());
    } else {
        std::cout << command << ": command not found" << std::endl;
        return;
    }

    // reset output if it was redirected
    if (redirecting_output) {
        dup2(stdout_fd, STDOUT_FILENO);
        close(stderr_fd);
    } else if (redirecting_error) {
        dup2(stderr_fd, STDERR_FILENO);
        close(stderr_fd);
    }
}

int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    parse_path();

    uid = getuid();
    pw = getpwuid(uid);
    if (pw == nullptr) {
        perror("error fetching user info");
        exit(EXIT_FAILURE);
    }

    gethostname(hostname, sizeof(hostname));

    stdout_fd = dup(STDOUT_FILENO);
    stderr_fd = dup(STDERR_FILENO);

    // REPL
    print_prompt();

    std::string buffer;
    while (std::getline(std::cin, buffer)) {
        eval(buffer);
        buffer.clear();
        print_prompt();
    }

    return EXIT_SUCCESS;
}
