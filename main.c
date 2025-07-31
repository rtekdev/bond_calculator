#include <stdio.h>
#include <stdlib.h>
#include "src/logic/operations.h"
#include "src/logic/inflation.h"
#include "src/logic/bond_loader.h"

int main() {
    // double inflation = getInflation("2024");
    // compound_return result = compound_interest(1000, 6.25, 10, 2.0, inflation, "inflation");

    // printf("Total: %.2lf\n", result.total);
    // printf("Profit: %.2lf\n", result.profit);
    // printf("Influation lost: %.2f\n", result.inflation_lost);
    // printf("Last year inflation: %.2lf%%\n", inflation - 100);

    // compound_return result2 = compound_interest(1000, 6.25, 10, 0, inflation, "permament");

    // printf("Total: %.2lf\n", result2.total);
    // printf("Profit: %.2lf\n", result2.profit);
    // printf("Influation lost: %.2f\n", result2.inflation_lost);
    // printf("Last year inflation: %.2lf%%\n", inflation - 100);

    // size_t count;
    // BondType *bonds = load_bond_types(&count);
    // if(!bonds) return 1;

    // printf("Loaded %zu bond types: \n", count);
    // printf("Loaded %zu bond types:\n", count);
    // for (size_t i = 0; i < count; i++) {
    //     printf(" • %s: %d years @ %.2f%% (next: %.2f%%) [%s]\n",
    //            bonds[i].name,
    //            bonds[i].years,
    //            bonds[i].interest_rate,
    //            bonds[i].next_rate,
    //            bonds[i].type
    //     );
    //     free(bonds[i].name);
    //     free(bonds[i].type);
    // }
    // free(bonds);

    return 0;
}