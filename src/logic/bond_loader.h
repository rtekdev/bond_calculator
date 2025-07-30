#ifndef BOND_LOADER_H
#define BOND_LOADER_H

typedef struct {
    char *name;
    int years;
    double interest_rate;
    double next_rate;
    char *type;
} BondType;

static char *read_file(const char *file_path);
BondType *load_bond_types(size_t *out_count);

#endif