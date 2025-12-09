# Homework

Name: Tanav Mylavaram

## Question 1) Define the following unit, integration, regression tests and when you would use each?

Unit test:  
It checks a single small piece of code. you use tests while implementing to make sure each one's behavior is expected for all the tests ran.

Integration test: 
It checks how multiple parts of the system work together. You use it to make sure that modules interact correctly.

Regression test: 
It's written after you find a bug. You first write a test that fails cause of a bug then fix the code so the test passes. keep the regression tests around helps prevent the same bug from coming back later on.

## Question 2) Briefly explain pytest discovery (file/function naming) and what a fixture is.

Pytest discovery:  
Pytest automatically finds tests if the file starts with test_ or ends with _test.py.
It also looks for functions that start with test_.
That’s why our test files and test functions follow those names.

Fixture:  
A fixture is a function that sets up something a test needs, like sample data.
You write it once, and any test that needs it can use it.
Pytest also gives some built-in fixtures, like tmp_path, which creates a temporary folder for tests that use files.

## Pytest features used
-@pytest.mark.parametrize to test many inputs using one test function
-A custom fixture (sample_prices) to reuse the same data across tests
-The built-in tmp_path fixture for file-related tests
