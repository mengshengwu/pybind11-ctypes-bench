#ifndef STRING_FUNC_H
#define STRING_FUNC_H

#ifdef __cplusplus
extern "C" {
#endif

// Process string and return a new string
// Caller is responsible for freeing the returned string
char* process_string(const char* input);

// Free string allocated by process_string
void free_string(char* str);

#ifdef __cplusplus
}
#endif

#endif // STRING_FUNC_H

