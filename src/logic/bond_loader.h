#ifndef BOND_LOADER_H
#define BOND_LOADER_H

#include <stdlib.h>

typedef struct {
    char *name;
    int years;
    double interest_rate;
    double next_rate;
    char *type;
} BondType;

BondType *load_bond_types(size_t *out_count);
void free_bond_types(BondType *arr, size_t count);

#endif