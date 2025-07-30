#include <stdio.h>
#include "operations.h"
#include <math.h>
#include <string.h>

compound_return compound_interest(float initial_amount, double interest_rate, int years, double next_rate, double inflation, char type[10]) {
    float annual_inflation_rate = (inflation - 100) / 100;

    float first_year = 1 + interest_rate/100;
    float total = 0.0;

    if(strcmp(type, "inflation") == 0){
        total = initial_amount * first_year * powf((1 + next_rate / 100 + annual_inflation_rate), years - 1);
    }else {
        total = initial_amount * powf(1 + interest_rate/100, years);
    }
    float profit = total - initial_amount; 

    float inflation_adjustment = powf(1 + annual_inflation_rate, years);
    float inflation_lost = initial_amount / inflation_adjustment;

    compound_return result;
    result.total = total;
    result.profit = profit;
    result.inflation_lost = inflation_lost;

    return result;
}