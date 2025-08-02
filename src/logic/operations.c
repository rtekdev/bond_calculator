#include <stdio.h>
#include "operations.h"
#include <math.h>
#include <string.h>

typedef struct {
    double total;
    double profit;
} returnTotalAndProfit;

static returnTotalAndProfit calculate_formula(
  float            amount,
  double           interest_rate,
  int              years,
  double           next_rate,
  double           annual_inflation_rate,
  const char      *type
);

void compound_interest(
  compound_return *out,
  float            initial_amount,
  double           interest_rate,
  int              years,
  double           next_rate,
  double           inflation,
  const char      *bond_type,
  int              total_years,
  float            regular_amount,
  const char      *regular_type
) {
    double annual_inflation_rate = (inflation - 100.0) / 100.0;
    
    compound_return result;

    int iterations = total_years + (total_years - 10 > 0 ? total_years - 10 : 0) - 1;
    
    // First time
    returnTotalAndProfit initial_data = calculate_formula(
        initial_amount, interest_rate, years, next_rate, annual_inflation_rate, bond_type
    );
    result.total = initial_data.total;
    result.profit = initial_data.profit;
    
    float n = total_years / 10;
    for(int i = 0; i < n; i++) {
        returnTotalAndProfit reinvest_initial = calculate_formula(
            result.total, interest_rate, years, next_rate, annual_inflation_rate, bond_type
        );
        result.total = reinvest_initial.total;
        result.profit = reinvest_initial.profit;
    }

    if(strcmp(regular_type, "monthly") == 0)
        iterations *= 12;

    while(iterations > 0) {
        returnTotalAndProfit res_data = calculate_formula(
            regular_amount, interest_rate, years, next_rate, annual_inflation_rate, bond_type
        );

        result.total += res_data.total;
        result.profit += res_data.profit;

        iterations--;
    }

    double inflation_adj    = pow(1 + annual_inflation_rate, years);
    double inflation_lost   = initial_amount / inflation_adj;

    out->total              = result.total;
    out->profit             = result.profit;
    out->inflation_lost     = result.inflation_lost;
}

static returnTotalAndProfit calculate_formula(
  float            amount,
  double           interest_rate,
  int              years,
  double           next_rate,
  double           annual_inflation_rate,
  const char      *type
) {
    
    double first_year = 1 + interest_rate/100.0;
    double total;

    if (strcmp(type, "inflation") == 0) {
        total = amount * first_year
            * pow(1 + next_rate/100.0 + annual_inflation_rate, years - 1);
    } else 
        total = amount * pow(1 + interest_rate/100.0, years);
    
    double profit = total - amount;
    
    returnTotalAndProfit result;
    result.total = total;
    result.profit = profit;

    return result;
}