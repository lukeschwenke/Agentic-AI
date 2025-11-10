import pytest
from core.tools import get_treasury_10yr_yield, get_rates_search_tool

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

# Run tests with
# poetry run pytest test_tools.py -m treasury -s
# poetry run pytest test_tools.py -m interest_rate -s