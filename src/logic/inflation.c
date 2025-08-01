// main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <curl/curl.h>
#include <cjson/cJSON.h>
#include <math.h>
#include "inflation.h"

// Buffer for the HTTP response
typedef struct {
    char *data;
    size_t length;
} Buffer;

// libcurl write-callback: append incoming data into resp
static size_t write_cb(void *ptr, size_t size, size_t nmemb, void *userdata) {
    Buffer *r = userdata;
    size_t total = size * nmemb;
    char *tmp = realloc(r->data, r->length + total + 1);
    if(!tmp) return 0;
    r->data = tmp;
    memcpy(r->data + r->length, ptr, total);
    r->length += total;
    r->data[r->length] = '\0';
    return total;
}

double getInflation(char *year) {
    CURL *curl = curl_easy_init();
    if (!curl) {
        fprintf(stderr, "Failed to initialize libcurl\n");
        return 1;
    }

    Buffer resp = { .data = NULL, .length = 0 };

    // GUS BDL API endpoint for Poland (unit 000000000000) CPI (var-id 217230)
    char url[256];

    int n = snprintf(
        url, sizeof(url),
        "https://bdl.stat.gov.pl/api/v1/data/by-unit/"
        "000000000000?var-id=217230&year=%s&format=json",
        year
    );

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    // headers = curl_slist_append(headers, "X-ClientId: YOUR_CLIENT_ID");

    curl_easy_setopt(curl, CURLOPT_URL, url);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &resp);

    if (curl_easy_perform(curl) != CURLE_OK) {
        fprintf(stderr, "HTTP request failed\n");
        curl_slist_free_all(headers);
        free(resp.data);
        return NAN;
    }

    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    cJSON *root    = cJSON_Parse(resp.data);
    if(!root) {
         fprintf(stderr, "JSON pare error: %s\n", cJSON_GetErrorPtr());
         free(resp.data);
         return NAN;
    }

    cJSON *results = cJSON_GetObjectItemCaseSensitive(root, "results");
    cJSON *first = cJSON_GetArrayItem(results, 0);
    cJSON *values = cJSON_GetObjectItemCaseSensitive(first, "values");
    cJSON *single = cJSON_GetArrayItem(values, 0);
    cJSON *val    = cJSON_GetObjectItemCaseSensitive(single, "val");
    
    double inflation =  cJSON_IsNumber(val) ? val->valuedouble : NAN;
   
    cJSON_Delete(root);
    free(resp.data);

    return inflation;
}
