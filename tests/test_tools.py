import pytest
from core.tools import get_treasury_10yr_yield, get_rates_search_tool, calculate_estimates_and_breakeven

@pytest.mark.treasury
def test_live_us10y_range():
    """
    Test to see if CNBC 10 year treasury yield is returned
    """
    val = get_treasury_10yr_yield()
    print(f"TEST #1 - 10 Year Treasury Yield = {val}")
    assert 0.0 < val < 20.0 

@pytest.mark.interest_rate
def test_live_average_interest_rate():
    """
    Test to see what the average interest rate is in the US currently.
    """
    val = get_rates_search_tool()
    print(f"TEST #2 - Average US Interest Rate = {val}")
    assert val is not None

@pytest.mark.calculation
def test_calulcator_rool():
    """
    Test to see how the calculator performs getting the new payment and break even.
    """
    current_payment = 5000
    mortgage_balance = 650000
    market_rate = 6.125
    vals = calculate_estimates_and_breakeven(current_payment, mortgage_balance, market_rate)
    new_payment, monthly_savings, break_even = vals

    print(f"\nTEST #3.1 - New Monthly Payment: {round(new_payment,2)}")
    print(f"\nTEST #3.2 - Monthly Savings: {round(monthly_savings,2)}")
    print(f"\nTest #3.3 - Break Even: {round(break_even,2)} ")

    assert isinstance(vals, tuple)
    assert len(vals) == 3
    assert isinstance(new_payment, float)
    assert isinstance(monthly_savings, float)
    assert isinstance(break_even, float)
    assert monthly_savings > 0
    assert new_payment > 0
    assert break_even > 0


# Run tests with
# poetry run pytest test_tools.py -m treasury -s
# poetry run pytest test_tools.py -m interest_rate -s