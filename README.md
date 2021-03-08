# Launch Interceptor Program
The project is an implementation of a hypothetical anti-ballistic missile system's launch interceptor program based on 
`“An experimental evaluation of the assumption of independence in multiversion programming,” J. C. Knight and
N. G. Leveson, IEEE Transactions on Software Engineering`

# Overview
The project implements a class *Decide()* with a method *launch_decision()* that generate a boolean signal which determines whether an 
interceptor should be launched based upon input radar tracking information (e.g. an array of 2D-coordinates, representing the missile's position at different points in time). 
The input radar tracking information is provided when an object of Decide() class is instantiated.

In addition to *Decide()* method and the LIC requirements LIC-0-14, there is also vectors like:
	* CMV: The fifteen elements of a Conditions Met Vector (CMV) will be assigned boolean values true or false; each element of the CMV corresponds to one
LIC’s condition.
	* LCM: The input Logical Connector Matrix (LCM), defines which individual LIC’s must be considered jointly in some way. The LCM is a 15x15 symmetric matrix with elements valued ANDD,
ORR, or NOTUSED
	* PUM: Preliminary Unlocking Matric (PUM) is a combination of LCM and CMV, i.e. 15*15 matrix.
	* PUV: Preliminary Unlocking Vector (PUV) represents which LIC actually matters in this particular launch determination.

The input parameters are the number of planar data points, array containing those data points, constant parameters, LCM and PUV. 

* File Structure:
	* Connector.py : Implements a helper class to provide Logical operations for LCM
	* launch_Parameters.py : Implements a helper class to provide a set of input parameters 
	* Point2D.py : Implements a helper class to represent a point in 2D.
	* launch_interceptor_program.py : Implements a class *Decide()* with all the LIC requirements.
	* test_interceptor_program.py : Implements the tests for the methods of class *Decide()* with all the LIC requirements.


# Branching convention
Supporting branches were created to aid group members to work parallelly, and to help the TAs so that they can easily track individual commits for versioning and testing.

The branches and their purposes are as follows:

* main 		(Containing all fetures and fixed README file)
* lic07_features_AH   (LIC 0-7 implemented by Adha Hrusto)
* lic8-14_features_MR   (LIC 8-14 implemented by Momina Rizwan)
* lic0-7_test_feat_AH	(Tests for LIC 0-7 implemented by Adha Hrusto)
* lic8-14_test_feat_MR	 (Tests for LIC 8-14 implemented by Momina Rizwan)

You can switch between branches using the following command in the terminal.

	`<$ git checkout $Branch_name$ >`

# Requirements
* Python 3.8
* Pytest 6.2.2


# Running the Test Suite
With the *pytest* package, tests can be executed with a simple command:
`<$ pytest>`

With no arguments, pytest looks at the current working directory (or some other preconfigured directory) and all subdirectories for test files and runs the test code it finds.

Additionaly, you can run a specific test file by giving its name as an argument.

`<$ pytest test_interceptor_program.py::test_lic1>`

# Contributors
* Adha Hrusto
	* Worked on creating the skeleton for the project.
	* Helped creating helper classes.
	* Implemented the requirements of LIC 0 - LIC 7.
<<<<<<< HEAD
	* Implemented unit tests for methods in the Decide class: LIC 0 - LIC 7, Decide and ComputeCMV.
	* Helped writing the README file.
=======
	* Implemented unit tests for methods in the Decide class: LIC 0 - LIC 7, launch_decision and compute_CMV
	* Helped writing the README file
>>>>>>> 286315fc1b6eceedbbbe3ff60794b2432b22e0dc

* Momina Rizwan
	* Helped creating helper classes (Point2D, Parameters and Connector class).
	* Implemented the requirements of LIC 08 - LIC 14.
	* Implemented helper method "within_circle" for LIC 08 and LIC 14.
	* Implemented the unit tests for methods in the Decide class: LIC 08 - LIC 14, Compute_FUV, Compute_PUM.
	* Helped writing the README file.


	
