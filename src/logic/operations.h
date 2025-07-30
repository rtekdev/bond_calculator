#ifndef OPERATIONS_H
#define OPERATIONS_H

typedef struct {
    double total;
    double profit;
    double inflation_lost;
} compound_return;

compound_return compound_interest(float initial_amount, double interest_rate, int years, double next_rate, double infation, char type[10]);

#endif