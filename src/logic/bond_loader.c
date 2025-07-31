// bond_loader.c
#include "bond_loader.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cjson/cJSON.h"

// Path to your JSON
static const char *JSON_PATH = "./src/data/bond_types.json";

// Read entire file into a NUL-terminated malloc()’d buffer.
static char *read_file(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    rewind(f);

    char *buf = malloc(len + 1);
    if (!buf) { fclose(f); return NULL; }

    if (fread(buf, 1, len, f) != (size_t)len) {
        free(buf);
        fclose(f);
        return NULL;
    }
    buf[len] = '\0';
    fclose(f);
    return buf;
}

BondType *load_bond_types(size_t *out_count) {
    *out_count = 0;
    char *json_text = read_file(JSON_PATH);
    if (!json_text) {
        fprintf(stderr, "Error reading JSON file %s\n", JSON_PATH);
        return NULL;
    }

    cJSON *root = cJSON_Parse(json_text);
    if (!root || !cJSON_IsArray(root)) {
        fprintf(stderr, "JSON parse error or not an array: %s\n",
                cJSON_GetErrorPtr());
        free(json_text);
        cJSON_Delete(root);
        return NULL;
    }

    size_t n = cJSON_GetArraySize(root);
    BondType *arr = calloc(n, sizeof *arr);
    if (!arr) {
        perror("calloc");
        free(json_text);
        cJSON_Delete(root);
        return NULL;
    }

    for (size_t i = 0; i < n; i++) {
        cJSON *item = cJSON_GetArrayItem(root, i);

        // name
        cJSON *jname = cJSON_GetObjectItem(item, "name");
        arr[i].name = strdup(
            (jname && cJSON_IsString(jname)) 
              ? jname->valuestring 
              : "");

        // years
        cJSON *jyears = cJSON_GetObjectItem(item, "years");
        arr[i].years = (jyears && cJSON_IsNumber(jyears))
                       ? jyears->valueint
                       : 0;

        // interest_rate
        cJSON *jrate = cJSON_GetObjectItem(item, "interest_rate");
        arr[i].interest_rate = (jrate && cJSON_IsNumber(jrate))
                               ? jrate->valuedouble
                               : 0.0;

        // next_rate
        cJSON *jnextr = cJSON_GetObjectItem(item, "next_rate");
        arr[i].next_rate = (jnextr && cJSON_IsNumber(jnextr))
                           ? jnextr->valuedouble
                           : 0.0;

        // type
        cJSON *jtype = cJSON_GetObjectItem(item, "type");
        arr[i].type = strdup(
            (jtype && cJSON_IsString(jtype)) 
              ? jtype->valuestring 
              : "");
    }

    // clean up parse tree, then free the buffer we malloc’d
    cJSON_Delete(root);
    free(json_text);

    *out_count = n;
    return arr;
}

void free_bond_types(BondType *arr, size_t count) {
    if (!arr) return;
    for (size_t i = 0; i < count; i++) {
        free(arr[i].name);
        free(arr[i].type);
    }
    free(arr);
}
