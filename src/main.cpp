#include <iostream>
#include <pwd.h>
#include <regex>
#include <termios.h>

#include "commands.h"
#include "utils.h"
#include "graphics.h"

// session and user information
uid_t uid;
passwd *pw;
char hostname[256];
int stdout_fd;
int stderr_fd;
bool piped = false;

void print_prompt() {
    if (piped) {
        return;
    }

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

void set_raw_mode(const termios &orig_termios) {
    termios raw = orig_termios;
    raw.c_lflag &= ~(ECHO | ICANON);  // Disable echo and canonical mode
    raw.c_cc[VMIN] = 1;   // Read returns after 1 character
    raw.c_cc[VTIME] = 0;  // No timeout, return immediately
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}

std::vector<std::string> read_input() {
    termios orig_termios{};
    tcgetattr(STDIN_FILENO, &orig_termios);
    set_raw_mode(orig_termios);

    std::vector<std::string> command_buffer;
    std::string command;

    while (true) {
        const int next = getchar();

        if (next == '\n') {
            if (!piped) {
                std::cout << std::endl;
            }

            if (!command.empty()) {
                command_buffer.push_back(command);
                command.clear();
            }
            break;
        }

        if (next == '\t') {
            const auto completions = autocomplete(command);
            if (completions.size() == 1) {
                if (!piped) {
                    // echo the remaining to stdout
                    for (size_t i = command.length(); i < completions[0].length(); i++) {
                        std::cout << completions[0][i];
                    }
                    std::cout << " ";
                }
                command = completions[0] + " ";
            }
            continue;
        }

        if (next == 127) {
            if (command.empty()) {
                continue;
            }

            command.pop_back();
            std::cout << "\b \b";
            continue;
        }

        const char c = static_cast<char>(next);
        command += c;
        if (!piped) {
            std::cout << c;
        }
    }

    // restore original terminal mode
    tcsetattr(STDIN_FILENO, TCSANOW, &orig_termios);

    return command_buffer;
}

[[noreturn]] int main() {
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    piped = !isatty(STDOUT_FILENO);

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
    while (true) {
        print_prompt();
        const std::vector<std::string> commands = read_input();
        for (const std::string &command: commands) {
            eval(command);
        }
    }
}
