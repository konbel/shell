#include <iostream>
#include <pwd.h>
#include <regex>
#include <termios.h>
#include <fcntl.h>
#include <sys/wait.h>

#include "commands.h"
#include "utils.h"
#include "graphics.h"

// session and user information
uid_t uid;
passwd *pw;
char hostname[256];
bool piped = false;

void print_prompt() {
    if (piped) {
        return;
    }

    const std::string dir = std::regex_replace(getcwd(nullptr, 0), std::regex(getenv("HOME")), "~");

    std::cout << ORANGE << BOLD << pw->pw_name << "@" << hostname << RESET << ":" << BLUE << BOLD
            << dir << RESET << "$ ";
}

inline bool check_redirect_destination(const std::vector<std::string> &arg, const int i) {
    if (i + 1 >= arg.size()) {
        std::cout << "syntax error near unexpected token `newline'" << std::endl;
        return false;
    }
    return true;
}

void eval(const std::string &input) {
    const std::vector<std::string> inputs = split(input, '|');

    // parse individual commands
    for (const auto &cmd: inputs) {
        const auto command = parse_command(cmd);
        const auto args = parse_args(cmd);

        // check for output and error redirecting
    }

    // create pipes if necessary
    const size_t pipe_count = inputs.size() - 1;
    std::vector<int[2]> pipes(pipe_count);
    for (int i = 0; i < pipe_count; i++) {
        if (pipe(pipes[i]) == -1) {
            perror("error creating pipe");
            return;
        }
    }

    // handle commands
    std::vector<int> pids;
    for (int i = 0; i < inputs.size(); i++) {
        const auto &command = parse_command(inputs[i]);
        const auto &args = parse_args(inputs[i]);

        int output_fd = -1;
        int input_fd = -1;
        int error_fd = -1;

        // check for output and error redirecting
        std::vector<std::string> filtered_args;
        for (int j = 0; j < args.size(); j++) {
            const std::string &arg = args[j];

            if (arg == ">" || arg == "1>") {
                if (check_redirect_destination(args, j)) {
                    const std::string &output = args[j + 1];
                    output_fd = open(output.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
                    if (output_fd == -1) {
                        perror("error opening file for output");
                    }
                }
                break;
            }

            if (arg == "2>") {
                if (check_redirect_destination(args, j)) {
                    const std::string &output = args[j + 1];
                    error_fd = open(output.c_str(), O_WRONLY | O_CREAT | O_TRUNC, 0644);
                    if (error_fd == -1) {
                        perror("error opening file for error");
                    }
                }
                break;
            }

            if (arg == ">>" || arg == "1>>") {
                if (check_redirect_destination(args, j)) {
                    const std::string &output = args[j + 1];
                    output_fd = open(output.c_str(), O_WRONLY | O_CREAT | O_APPEND, 0644);
                    if (output_fd == -1) {
                        perror("error opening file for output");
                    }
                }
                break;
            }

            if (arg == "2>>") {
                if (check_redirect_destination(args, j)) {
                    const std::string &output = args[j + 1];
                    error_fd = open(output.c_str(), O_WRONLY | O_CREAT | O_APPEND, 0644);
                    if (error_fd == -1) {
                        perror("error opening file for error");
                    }
                }
                break;
            }

            filtered_args.push_back(arg);
        }

        // connect pipes
        if (i <= static_cast<int>(pipe_count - 1)) {
            output_fd = pipes[i][1];
        }

        if (i > 0 && i - 1 <= pipe_count) {
            input_fd = pipes[i - 1][0];
        }

        // execute command
        redirect_io(output_fd, input_fd, error_fd);
        if (builtins.contains(command)) {
            builtins[command](input, filtered_args);
        } else if (executables_cache.contains(command)) {
            const int pid = exec(executables_cache[command], filtered_args, output_fd, input_fd);
            if (pid != -1) {
                pids.push_back(pid);
            }
        } else {
            std::cout << command << ": command not found" << std::endl;
        }
        restore_io();

        // close pipes
        if (output_fd != -1) {
            close(output_fd);
        }

        if (input_fd != -1) {
            close(input_fd);
        }

        if (error_fd != -1) {
            close(error_fd);
        }
    }

    for (const int pid: pids) {
        waitpid(pid, nullptr, 0);
    }
}

void set_raw_mode(const termios &orig_termios) {
    termios raw = orig_termios;
    raw.c_lflag &= ~(ECHO | ICANON); // Disable echo and canonical mode
    raw.c_cc[VMIN] = 1; // Read returns after 1 character
    raw.c_cc[VTIME] = 0; // No timeout, return immediately
    tcsetattr(STDIN_FILENO, TCSAFLUSH, &raw);
}

std::vector<std::string> read_input() {
    termios orig_termios{};
    tcgetattr(STDIN_FILENO, &orig_termios);
    set_raw_mode(orig_termios);

    std::vector<std::string> command_buffer;
    std::string command;

    bool last_char_tab = false;

    while (true) {
        const int next = getchar();

        if (next == '\t') {
            auto completions = autocomplete_builtin(command);
            const auto executable_completions = autocomplete_executable(command);
            completions.insert(executable_completions.begin(), executable_completions.end());

            std::vector<std::string> completions_sorted;
            for (const auto &completion: completions) {
                completions_sorted.push_back(completion);
            }
            std::ranges::sort(completions_sorted);

            if (completions_sorted.size() == 1) {
                const auto &completed = completions_sorted[0];
                if (!piped) {
                    // print the remaining to stdout
                    for (size_t i = command.length(); i < completed.size(); i++) {
                        std::cout << completed[i];
                    }
                    std::cout << " ";
                }
                command = completed + " ";
                last_char_tab = false;
                continue;
            }

            if (completions_sorted.size() > 1 && last_char_tab) {
                // print possible completions
                std::cout << std::endl;
                for (int i = 0; i < completions_sorted.size(); i++) {
                    std::cout << completions_sorted[i];

                    if (i < completions_sorted.size() - 1) {
                        std::cout << '\t';
                    }
                }
                std::cout << std::endl;
                if (!piped) {
                    print_prompt();
                    std::cout << command;
                }
                continue;
            }

            if (completions_sorted.size() > 1) {
                const std::string common_prefix = lcp(completions_sorted);

                if (command.size() != common_prefix.size()) {
                    if (!piped) {
                        // print the remaining to stdout
                        for (size_t i = command.length(); i < common_prefix.size(); i++) {
                            std::cout << common_prefix[i];
                        }
                    }
                    command = common_prefix;
                    continue;
                }
            }

            std::cout << '\a';
            last_char_tab = true;
            continue;
        }
        last_char_tab = false;

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
    build_executables_cache();

    // setup io
    std::cout << std::unitbuf;
    std::cerr << std::unitbuf;

    piped = !isatty(STDOUT_FILENO);

    // get session and host information
    uid = getuid();
    pw = getpwuid(uid);
    if (pw == nullptr) {
        perror("error fetching user info");
        exit(EXIT_FAILURE);
    }

    gethostname(hostname, sizeof(hostname));

    // REPL
    while (true) {
        print_prompt();
        const std::vector<std::string> commands = read_input();
        for (const std::string &command: commands) {
            eval(command);
        }
    }
}
