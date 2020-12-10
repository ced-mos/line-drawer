# Execute all test
# ! Workaround because VS Code Test application suddenly didn't work anymore !
clear
./venv/bin/python3 -m unittest discover -s "./test" -p "test_*.py" -v
