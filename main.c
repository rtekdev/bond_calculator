#include <stdio.h>
#include "src/logic/operations.h"
#include "src/logic/inflation.h"

int add(int a, int b) { return a + b; }

int main() {
    double inflation = getInflation("2024");
    compound_return result = compound_interest(26000, 6.25, 10, inflation);

    printf("Total: %.2f\n", result.total);
    printf("Profit: %.2f\n", result.profit);
    printf("Influation lost: %.2f\n", result.inflation_lost);
    printf("Last year inflation: %.2lf%%\n", inflation - 100);

    return 0;
}