from edgar_utils.xbrl_parser import Edgar
from edgar_utils.params import EXAMPLE_EMAIL

#test data request
def test_fetch_data():
    email = str(input("Enter your email: "))  # Prompt the user for email input
    edgar_instance = Edgar()  # Create an instance of the Edgar class
    edgar_instance.fetch_data(email)  # Call the fetch_data method of the Edgar instance

def test_fetch_ticker():
    comp_name = str(input("Enter a company name: "))  # Prompt the user for email input
    edgar_instance = Edgar()
    edgar_instance.fetch_ticker(comp_name)

def test_fetch_cik():
    company_ticker = str(input("Enter the company ticker: "))
    edgar_instance = Edgar()
    result = edgar_instance.fetch_cik(company_ticker)
    print(result)

if __name__ == "__main__":
    # test_fetch_data()
    # test_fetch_ticker()
    test_fetch_cik()
