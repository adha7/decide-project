# Launch Interceptor Program
The project is an implementation of an anti-ballistic missile system's launch interceptor program based on 
an experimental evaluation of the assumption of independence in multiversion programming by J. C. Knight and N. G. Leveson from 1986.

# Overview
The project implements a class *Decide()* with a method *launch_decision()* that generate a boolean signal which determines whether an 
interceptor should be launched based upon input radar tracking information (e.g. an array of 2D-coordinates, representing the missile's position at different points in time). 
The input radar tracking information is provided when an object of Decide() class is instantiated.


# Requirements
* Pyhton 3.8
* Pytest 6.2.2


# Running the test suite
With the *pytest* package, tests can be executed with a simple command:
`<$ pytest>`

With no arguments, pytest looks at the current working directory (or some other preconfigured directory) and all subdirectories for test files and runs the test code it finds.

Additionalz, you can run a specific test file by giving its name as an argument.

$ pytest test_interceptor_program.py::lic_1

# Contributors
* Adha Hrusto
	* Worked on creating the skeleton for the project.
	* Helped creating helper classes
	* Implemented the requirements of LIC 0 - LIC 7.
	* Implemented unit tests for methods in the Decide class: LIC 0 - LIC 7, Decide and ComputeCMV
	* Helped writing the README file

* Momina Rizwan
