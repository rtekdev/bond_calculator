#include <stdio.h>
#include "operations.h"
#include <math.h>

compound_return compound_interest(float initial_amount, float interest_rate, int years, double inflation) {
    // formula = P*()
    float annual_inflation_rate = (inflation - 100) / 100;

    float first_year = 1 + interest_rate/100;
    float total = initial_amount * first_year * powf((1.02 + annual_inflation_rate), years - 1);
    float profit = total - initial_amount; 

    float inflation_adjustment = powf(1 + annual_inflation_rate, years);
    float inflation_lost = initial_amount / inflation_adjustment;

    compound_return result;
    result.total = total;
    result.profit = profit;
    result.inflation_lost = inflation_lost;

    return result;
}