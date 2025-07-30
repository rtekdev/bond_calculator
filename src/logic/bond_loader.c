#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "cjson/cJSON.h"
#include "bond_loader.h"

const char *path = "./src/data/bond_types.json";

static char *read_file(const char *file_path) {
    FILE *f = fopen(file_path, "rb");
    if(!f) return NULL;
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    rewind(f);

    char *buf = malloc(len + 1);
    if(!buf) { fclose(f); return NULL; }

    if(fread(buf, 1, len, f) != (size_t)len){
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
    char *json_text = read_file(path);
    if (!json_text) {
        fprintf(stderr, "Could not read %s\n", path);
        return NULL;
    }

    cJSON *root = cJSON_Parse(json_text);
    free(json_text);
    if (!root || !cJSON_IsArray(root)) {
        fprintf(stderr, "JSON is not an array\n");
        cJSON_Delete(root);
        return NULL;
    }

    size_t n = cJSON_GetArraySize(root);
    BondType *arr = calloc(n, sizeof(BondType));
    if (!arr) {
        cJSON_Delete(root);
        return NULL;
    }

    for (size_t i = 0; i < n; i++) {
        cJSON *item = cJSON_GetArrayItem(root, i);

        // name
        cJSON *jname = cJSON_GetObjectItem(item, "name");
        arr[i].name = strdup(cJSON_IsString(jname) ? jname->valuestring : "");

        // years
        cJSON *jyears = cJSON_GetObjectItem(item, "years");
        arr[i].years = cJSON_IsNumber(jyears) ? jyears->valueint : 0;

        // interest_rate
        cJSON *jrate = cJSON_GetObjectItem(item, "interest_rate");
        arr[i].interest_rate = cJSON_IsNumber(jrate) ? jrate->valuedouble : 0.0;

        // next_rate
        cJSON *jnextr = cJSON_GetObjectItem(item, "next_rate");
        arr[i].next_rate = cJSON_IsNumber(jnextr) ? jnextr->valuedouble : 0.0;

        // type
        cJSON *jtype = cJSON_GetObjectItem(item, "type");
        arr[i].type = strdup(cJSON_IsString(jtype) ? jtype->valuestring : "");
    }

    cJSON_Delete(root);
    *out_count = n;
    return arr;
}