#ifndef OPERATIONS_H
#define OPERATIONS_H

typedef struct {
  double total;
  double profit;
  double inflation_lost;
  float allInvested;
  float profit_percent;
  float lost_percent;
} compound_return;


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
);

#endif