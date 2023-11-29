# UOCIS322 - Project 5 #

Author: Nabil Abdel-Rahman

Contact: nabilabdel-rahman@outlook.com

This project consists of a web application that is based on RUSA's online calculator. The algorithm for calculating controle times is described here https://rusa.org/pages/acp-brevet-control-times-calculator. Additional background information is given here https://rusa.org/pages/rulesForRiders. The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly.

We are essentially replacing the calculator here https://rusa.org/octime_acp.html. We can also use that calculator to clarify requirements and develop test data.

The brevet calculator also has a submit button and a display button. When the submit button is pressed, all data entered is stored in a database in Mongo. If new edits are made and the user presses submit again, the old information in the database becomes overriden with whatever is currently entered. When the display button is hit, all information is cleared and replaced with the most recent information stored in the database. The database contains the brevet distance, the beginning date and time, and the distance, opening time, and closing time of each checkpoint.

We run the calculator using Docker Compose and Flask to load the page onto our machine locally. In a Linux environment, use the command "docker compose up" to spon everything up. A YAML is provided in the folder in order to run the program. Make sure to adjust the YAML file accordingly, such as the port numbers to which your machine binds to. Further, all page templates are provided in the folder "templates". Lastly, a skeleton to create your credentials page to run the program is provided as well. 

The frontend, calc.html, contains a javascript which allows for AJAX requests to the flask application. The file acp_times.py computes the calculations and returns it back to the flask application, which processes the data and returns the date and time for each interval back to calc.html, which then updates the page accordingly.

When the submit button is pressed, the frontend gathers all information entered on the page and stores it in a dictionary, which gets sent to flask_brevets where it is stored in a dictionary. When the display button is pressed, the frontend calls the back end to retrieve the dicitonary from the database and then parses through the dictionary to enter the respective fields with their values.

A file called test_flask_brevets.py is provided along with test_acp_times.py to hold test cases to ensure that the calculations in acp_times.py are correct and information stored and retrieved in Mongo is correct. Some tests contains variables which can be manipulated to ensure different scenarios are correct. To run the tests, in your terminal, make sure your current directory is "brevets" and run the command "nosetests tests".

Make sure to run the command "docker compose down --rmi local" to stop the program and delete all local images when finished running the program.