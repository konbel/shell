#ifndef SHELL_UTILS_H
#define SHELL_UTILS_H

#include <algorithm>
#include <filesystem>
#include <ranges>
#include <unistd.h>
#include <regex>

inline std::vector<std::string> path;
inline std::regex ws_regex("\\s+");

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
    std::istringstream ss(str + delimiter);

    while (std::getline(ss, buffer, delimiter)) {
        if (buffer.empty()) {
            continue;
        }
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

inline bool is_number(const std::string& str) {
    std::string::const_iterator it = str.begin();
    while (it != str.end() && std::isdigit(*it)) ++it;
    return !str.empty() && it == str.end();
}

inline std::vector<std::string> parse_path() {
    const std::string path_env = std::getenv("PATH");
    return split(path_env, ':');
}

inline std::string parse_command(const std::string &input) {
    std::string command;
    bool in_single_quotes = false;
    bool in_double_quotes = false;
    bool escaped = false;

    for (const char c : input) {
        // escaping
        if (escaped) {
            command += c;
            escaped = false;
            continue;
        }

        if (c == '\\' && !in_single_quotes) {
            escaped = true;
            continue;
        }

        // whitespaces
        if (isspace(c) && !in_single_quotes && !in_double_quotes) {
            break;
        }

        // single quotes
        if (c == '\'' && !in_double_quotes) {
            in_single_quotes = !in_single_quotes;
            continue;
        }

        // double quotes
        if (c == '"' && !in_single_quotes) {
            in_double_quotes = !in_double_quotes;
            continue;
        }

        // default
        command += c;
    }

    return command;
}

inline std::vector<std::string> parse_args(const std::string &arg_string) {
    std::vector<std::string> args;
    std::string buffer;
    bool in_single_quotes = false;
    bool in_double_quotes = false;
    bool escaped = false;

    for (const char c : arg_string) {
        // escaping
        if (escaped) {
            buffer += c;
            escaped = false;
            continue;
        }

        if (c == '\\' && !in_single_quotes) {
            escaped = true;
            continue;
        }

        // single quotes
        if (c == '\'' && !in_double_quotes) {
            in_single_quotes = !in_single_quotes;
            continue;
        }

        if (in_single_quotes) {
            buffer += c;
            continue;
        }

        // double quotes
        if (c == '"') {
            in_double_quotes = !in_double_quotes;
            continue;
        }

        if (in_double_quotes) {
            buffer += c;
            continue;
        }

        // whitespaces
        if (isspace(c)) {
            if (buffer.empty()) {
                continue;
            }
            args.push_back(buffer);
            buffer.clear();
            continue;
        }

        // default
        buffer += c;
    }

    if (!buffer.empty()) {
        args.push_back(buffer);
    }
    return args;
}

inline std::string lcp(const std::vector<std::string> &candidates) {
    std::string result;

    int index = 0;
    while (true) {
        if (index >= candidates[0].length()) {
            return result;
        }

        const char current = candidates[0][index];

        for (int i = 1; i < candidates.size(); i++) {
            const auto &candidate = candidates[i];

            if (index >= candidate.length()) {
                return result;
            }

            if (candidate[index] != current) {
                return result;
            }
        }

        index++;
        result += current;
    }
}

#endif //SHELL_UTILS_H
