// bond_loader.c
#include "bond_loader.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cjson/cJSON.h"

// Path to your JSON
static const char *JSON_PATH = "./src/data/bond_types.json";

// Read entire file into a NUL-terminated malloc()’d buffer.
BondType *getBonds(int *out_count) {
    *out_count = 0;

    // 1) open + size
    FILE *f = fopen(JSON_PATH, "rb");
    if (!f) {
        perror("fopen");
        exit(1);
    }
    fseek(f, 0, SEEK_END);
    long filesize = ftell(f);
    rewind(f);

    // 2) alloc + read + nul-term
    char *buffer = malloc(filesize + 1);
    if (!buffer) {
        fclose(f);
        perror("malloc");
        exit(1);
    }
    size_t got = fread(buffer, 1, filesize, f);
    fclose(f);
    if (got != (size_t)filesize) {
        fprintf(stderr, "fread: expected %ld, got %zu\n", filesize, got);
        free(buffer);
        exit(1);
    }
    buffer[filesize] = '\0';

    // 3) parse
    cJSON *json = cJSON_Parse(buffer);
    free(buffer);
    if (!json) {
        fprintf(stderr, "JSON parse error: %s\n", cJSON_GetErrorPtr());
        exit(1);
    }

    // 4) build array
    size_t n = cJSON_GetArraySize(json);
    *out_count = (int)n;
    BondType *arr = calloc(n, sizeof *arr);
    if (!arr) {
        perror("calloc");
        cJSON_Delete(json);
        exit(1);
    }

    for (int i = 0; i < (int)n; i++) {
        cJSON *item = cJSON_GetArrayItem(json, i);

        cJSON *j = cJSON_GetObjectItemCaseSensitive(item, "name");
        const char *nm = (cJSON_IsString(j) && j->valuestring) ? j->valuestring : "";
        arr[i].name = strdup(nm);

        j = cJSON_GetObjectItemCaseSensitive(item, "years");
        arr[i].years = (cJSON_IsNumber(j) ? j->valueint : 0);

        j = cJSON_GetObjectItemCaseSensitive(item, "interest_rate");
        arr[i].interest_rate = (cJSON_IsNumber(j) ? j->valuedouble : 0.0);

        j = cJSON_GetObjectItemCaseSensitive(item, "next_rate");
        arr[i].next_rate = (cJSON_IsNumber(j) ? j->valuedouble : 0.0);

        j = cJSON_GetObjectItemCaseSensitive(item, "type");
        const char *ty = (cJSON_IsString(j) && j->valuestring) ? j->valuestring : "";
        arr[i].type = strdup(ty);
    }

    cJSON_Delete(json);
    return arr;
}

void freeBonds(BondType *arr, int count) {
    if (!arr) return;
    for (int i = 0; i < count; i++) {
        free(arr[i].name);
        free(arr[i].type);
    }
    free(arr);
}