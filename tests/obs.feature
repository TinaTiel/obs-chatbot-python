Feature: Command execution
	In order to make something happen
	As an User
	I want to make a thing happen 
	and specify variants of that thing

	@wip
	Scenario: Command with arguments
		Given a command
		When that command is executed with arguments
		Then each action receives those arguments

	Scenario: Customised Command
		Given a command
		When that command is executed without arguments
		Then each action has no arguments

	Scenario: Command Actions
		Given a command with several actions
		When that command is executed
		Then actions are executed in order

	Scenario: Command with Allows
		Given a command with restrictions
		When that command is executed
		Then it executes with "failure"

	Scenario: Command with No Allows
		Given a command with no restrictions
		When that command is executed
		Then it executes with "success"

	Scenario: Command Priority
		Given two or more users executing a command
		When the commands are received
		Then they are executed in order received

	Scenario: Command Cooldown
		Given two or more users executing a command
		And the first command triggers a cooldown
		When the commands are received
		Then the second command is ignored


