#include <stdio.h>
#include <stdlib.h>
#include "src/logic/operations.h"
#include "src/logic/inflation.h"
#include "src/logic/bond_loader.h"

// Example test libraries
#include <time.h>
#include <string.h>

int main() {
    // You can test C logic here
    // Only you need to execute [make build] inside terminal
    // Then ./my_app

    // Get Inflation example:
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    char year_as_string[5];
    sprintf(year_as_string, "%d", tm.tm_year + 1900 - 1);
    double lastInflation = getInflation(year_as_string); 
    printf("Last Year inflation: %.2lf%%", lastInflation - 100);

    // White space
    printf("\n\n");

    // Read Bond Types 
    // Unfortunately Bonds must have be write manually (No free API)
    int numOfBonds;
    BondType *bonds = getBonds(&numOfBonds);
    printf("Num of bonds: %d\n", numOfBonds);

    for(int i = 0; i < numOfBonds; i++)
        printf("Name %d: %s\n", i + 1, bonds[i].name);
    
    // White space
    printf("\n");

    // Calculating example:
    compound_return calc_data;
    compound_interest(&calc_data, 10000, 6.0, 10, 2.0, lastInflation, "inflation", 12, 20, "monthly");
    printf("Total: %.2lf PLN\n", calc_data.total);
    printf("Profit: %.2lf PLN\n", calc_data.profit);
    printf("Inflation Lost: %.2lf PLN\n", calc_data.inflation_lost);
    printf("All Invested Money: %.2lf PLN\n\n", calc_data.allInvested);
    printf("Profit in Percentage: %.2f%%\n", calc_data.profit_percent*100);
    printf("Profit is based on total/all Invested Money\n");
    printf("Lost in Percentage: %.2f%%\n", calc_data.lost_percent*100);
    printf("Lost is based on last year inflation (GUS data)\n");

    return 0;
}