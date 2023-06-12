requirements python, flask,flask-wtf libraries
pip install flask
pip install flask-wtf

run web_app.py
goto http://127.0.0.1:5000/valid_id

This webform will take a ID in webform and will return if it satisfies following requirements:
1: ID must all be numbers, no letters or other superfluous characters
2: ID must be 11 digits
3: The first number of the ID can't be 0
4: The sum of: 1st, 3rd, 5th, 7th and 9th digits multiplied by seven, decremented by the sum of: 2nd, 4th, 6th and 8th digits, divided by 10, have the remainder equal to the 10th digit
5: The remainder from the sum of the first 10 digits, divided by 10, gives the 11th digit.

Here is an example of a valid Turkish National ID: 12345678950
