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

BondType *getBonds(int *out_count);
void freeBonds(BondType *arr, int count);

#endif