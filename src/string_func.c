#include <stdlib.h>
#include <string.h>
#include "string_func.h"

char* process_string(const char* input) {
    if (input == NULL) {
        return NULL;
    }
    
    size_t len = strlen(input);
    char* output = (char*)malloc(len + 1);
    if (output == NULL) {
        return NULL;
    }
    
    // Simple string copy operation
    strcpy(output, input);
    return output;
}

void free_string(char* str) {
    if (str != NULL) {
        free(str);
    }
}

