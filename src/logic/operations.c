#include <stdio.h>
#include "operations.h"
#include <math.h>
#include <string.h>

void compound_interest(
  compound_return *out,
  float            initial_amount,
  double           interest_rate,
  int              years,
  double           next_rate,
  double           inflation,
  const char      *type
) {
    double annual_inflation_rate = (inflation - 100.0) / 100.0;
    double first_year = 1 + interest_rate/100.0;
    double total;
    if (strcmp(type, "inflation")==0) {
        total = initial_amount * first_year
            * pow(1 + next_rate/100.0 + annual_inflation_rate, years - 1);
    } else {
        total = initial_amount * pow(1 + interest_rate/100.0, years);
    }
    double profit           = total - initial_amount;
    double inflation_adj    = pow(1 + annual_inflation_rate, years);
    double inflation_lost   = initial_amount / inflation_adj;

    out->total          = total;
    out->profit         = profit;
    out->inflation_lost = inflation_lost;
}