#ifndef SHELL_COLORS_H
#define SHELL_COLORS_H

// effects
inline constexpr char RESET[]           = "\033[0m";
inline constexpr char BOLD[]            = "\033[1m";
inline constexpr char ITALIC[]          = "\033[3m";
inline constexpr char UNDERLINE[]       = "\033[4m";
inline constexpr char BLINK[]           = "\033[5m";
inline constexpr char REVERSE[]         = "\033[7m";
inline constexpr char CROSSED_OUT[]     = "\033[9m";

// foreground colors
inline constexpr char BLACK[]           = "\033[30m";
inline constexpr char RED[]             = "\033[31m";
inline constexpr char GREEN[]           = "\033[32m";
inline constexpr char YELLOW[]          = "\033[33m";
inline constexpr char BLUE[]            = "\033[34m";
inline constexpr char MAGENTA[]         = "\033[35m";
inline constexpr char CYAN[]            = "\033[36m";
inline constexpr char WHITE[]           = "\033[37m";

inline constexpr char BRIGHT_BLACK[]    = "\033[90m";
inline constexpr char BRIGHT_RED[]      = "\033[91m";
inline constexpr char BRIGHT_GREEN[]    = "\033[92m";
inline constexpr char BRIGHT_YELLOW[]   = "\033[93m";
inline constexpr char BRIGHT_BLUE[]     = "\033[94m";
inline constexpr char BRIGHT_MAGENTA[]  = "\033[95m";
inline constexpr char BRIGHT_CYAN[]     = "\033[96m";
inline constexpr char BRIGHT_WHITE[]    = "\033[97m";

// background colors
inline constexpr char BG_BLACK[]        = "\033[40m";
inline constexpr char BG_RED[]          = "\033[41m";
inline constexpr char BG_GREEN[]        = "\033[42m";
inline constexpr char BG_YELLOW[]       = "\033[43m";
inline constexpr char BG_BLUE[]         = "\033[44m";
inline constexpr char BG_MAGENTA[]      = "\033[45m";
inline constexpr char BG_CYAN[]         = "\033[46m";
inline constexpr char BG_WHITE[]        = "\033[47m";

inline constexpr char BG_BRIGHT_BLACK[]   = "\033[100m";
inline constexpr char BG_BRIGHT_RED[]     = "\033[101m";
inline constexpr char BG_BRIGHT_GREEN[]   = "\033[102m";
inline constexpr char BG_BRIGHT_YELLOW[]  = "\033[103m";
inline constexpr char BG_BRIGHT_BLUE[]    = "\033[104m";
inline constexpr char BG_BRIGHT_MAGENTA[] = "\033[105m";
inline constexpr char BG_BRIGHT_CYAN[]    = "\033[106m";
inline constexpr char BG_BRIGHT_WHITE[]   = "\033[107m";

#endif //SHELL_COLORS_H
