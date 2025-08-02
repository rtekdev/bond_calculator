#include <stdio.h>
#include "operations.h"
#include <math.h>
#include <string.h>

static double calculate_formula(
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
    double res_total = calculate_formula(
        initial_amount, interest_rate, years, next_rate, annual_inflation_rate, bond_type
    );
    result.total = res_total;
    
    float n = total_years / 10;
    for(int i = 0; i < n; i++) {
        double res_profit = calculate_formula(
            result.total, interest_rate, years, next_rate, annual_inflation_rate, bond_type
        );
        result.total = res_profit;
    }

    if(strcmp(regular_type, "monthly") == 0)
        iterations *= 12;

    while(iterations > 0) {
        res_total = calculate_formula(
            regular_amount, interest_rate, years, next_rate, annual_inflation_rate, bond_type
        );

        result.total += res_total;
        iterations--;
    }

    float allRegularAmount = strcmp(regular_type, "monthly") == 0 ? 
        (regular_amount * 12 * total_years) : (regular_amount * total_years);
    float allInvestedAmount = initial_amount + allRegularAmount;

    double inflation_adj    = pow(1 + annual_inflation_rate, total_years);
    double inflation_lost   = allInvestedAmount / inflation_adj;
    double money_reduced_by_inflation = allInvestedAmount - inflation_lost;

    double profit = result.total - allInvestedAmount; 
    float profit_percent = result.total / allInvestedAmount;
    float lost_percent = money_reduced_by_inflation / allInvestedAmount;

    out->total              = result.total;
    out->profit             = profit;
    out->inflation_lost     = money_reduced_by_inflation;
    out->allInvested        = allInvestedAmount;
    out->profit_percent     = profit_percent;
    out->lost_percent       = lost_percent;
}

static double calculate_formula(
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
    
    return total;
}