#ifndef SHELL_UTILS_H
#define SHELL_UTILS_H

#include <algorithm>
#include <filesystem>
#include <ranges>
#include <unistd.h>
#include <regex>

inline std::vector<std::string> path;
inline std::regex ws_regex("\\s+");
inline std::regex trim_regex("^\\s+|\\s+$");

inline std::string find_executable(const std::string &executable) {
    for (const std::string &dir: path) {
        std::string full_path = std::filesystem::path(dir) / executable;
        if (access(full_path.c_str(), X_OK) == 0) {
            return full_path;
        }
    }
    return "";
}

inline std::vector<std::string> split(const std::string &str, const char delimiter) {
    std::string buffer;
    std::vector<std::string> parts;
    std::istringstream ss(str);

    while (std::getline(ss, buffer, delimiter)) {
        parts.push_back(buffer);
    }

    return parts;
}

inline std::string join(const std::vector<std::string> &parts, const std::string &delimiter) {
    std::string result;
    for (size_t i = 0; i < parts.size(); i++) {
        result += parts[i];
        if (i != parts.size() - 1) {
            result += delimiter;
        }
    }
    return result;
}

inline bool is_whitespace(const std::string &str) {
    return std::ranges::all_of(str, [](const char c) { return std::isspace(c); });
}

inline void parse_path() {
    const std::string path_env = std::getenv("PATH");
    path = split(path_env, ':');
}

inline std::string parse_command(const std::string &input) {
    size_t command_length = input.length();
    for (int i = 0; i < input.length(); i++) {
        if (std::isspace(input[i])) {
            command_length = i;
            break;
        }
    }
    return input.substr(0, command_length);
}

inline std::vector<std::string> parse_args(const std::string &arg_string) {
    const std::string trimmed = std::regex_replace(arg_string, trim_regex, "");

    std::string result;
    bool in_quotes = false;
    for (const char c : trimmed) {
        if (c == '\'') {
            in_quotes = !in_quotes;
        } else if (isspace(c) && !in_quotes) {
            if (result.back() != ' ') {
                result += ' ';
            }
        } else {
            result += c;
        }
    }

    return split(result, ' ');
}

#endif //SHELL_UTILS_H
