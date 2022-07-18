#!/usr/bin/env bash
# First line of the script is the shebang which tells the system how to execute
# the script: https://en.wikipedia.org/wiki/Shebang_(Unix)
# As you already figured, comments start with #. Shebang is also a comment.

# Simple hello world example:
echo Hello world! # => Hello world!

# Each command starts on a new line, or after a semicolon:
echo 'This is the first line'; echo 'This is the second line'
# => This is the first line
# => This is the second line

# Declaring a variable looks like this:
Variable="Some string"

# But not like this:
Variable = "Some string" # => returns error "Variable: command not found"
# Bash will decide that Variable is a command it must execute and give an error
# because it can't be found.

# Nor like this:
Variable= 'Some string' # => returns error: "Some string: command not found"
# Bash will decide that 'Some string' is a command it must execute and give an
# error because it can't be found. (In this case the 'Variable=' part is seen
# as a variable assignment valid only for the scope of the 'Some string'
# command.)

# Using the variable:
echo $Variable # => Some string
echo "$Variable" # => Some string
echo '$Variable' # => $Variable
# When you use the variable itself — assign it, export it, or else — you write
# its name without $. If you want to use the variable's value, you should use $.
# Note that ' (single quote) won't expand the variables!

# Parameter expansion ${ }:
echo ${Variable} # => Some string
# This is a simple usage of parameter expansion
# Parameter Expansion gets a value from a variable.
# It "expands" or prints the value
# During the expansion time the value or parameter can be modified
# Below are other modifications that add onto this expansion

# String substitution in variables
echo ${Variable/Some/A} # => A string
# This will substitute the first occurrence of "Some" with "A"

# Substring from a variable
Length=7
echo ${Variable:0:Length} # => Some st
# This will return only the first 7 characters of the value
echo ${Variable: -5} # => tring
# This will return the last 5 characters (note the space before -5)

# String length
echo ${#Variable} # => 11

# Indirect expansion
OtherVariable="Variable"
echo ${!OtherVariable} # => Some String
# This will expand the value of OtherVariable

# Default value for variable
echo ${Foo:-"DefaultValueIfFooIsMissingOrEmpty"}
# => DefaultValueIfFooIsMissingOrEmpty
# This works for null (Foo=) and empty string (Foo=""); zero (Foo=0) returns 0.
# Note that it only returns default value and doesn't change variable value.

# Declare an array with 6 elements
array0=(one two three four five six)
# Print first element
echo $array0 # => "one"
# Print first element
echo ${array0[0]} # => "one"
# Print all elements
echo ${array0[@]} # => "one two three four five six"
# Print number of elements
echo ${#array0[@]} # => "6"
# Print number of characters in third element
echo ${#array0[2]} # => "5"
# Print 2 elements starting from forth
echo ${array0[@]:3:2} # => "four five"
# Print all elements. Each of them on new line.
for i in "${array0[@]}"; do
    echo "$i"
done

# Brace Expansion { }
# Used to generate arbitrary strings
echo {1..10} # => 1 2 3 4 5 6 7 8 9 10
echo {a..z} # => a b c d e f g h i j k l m n o p q r s t u v w x y z
# This will output the range from the start value to the end value

# Built-in variables:
# There are some useful built-in variables, like
echo "Last program's return value: $?"
echo "Script's PID: $$"
echo "Number of arguments passed to script: $#"
echo "All arguments passed to script: $@"
echo "Script's arguments separated into different variables: $1 $2..."

# Now that we know how to echo and use variables,
# let's learn some of the other basics of bash!

# Our current directory is available through the command `pwd`.
# `pwd` stands for "print working directory".
# We can also use the built-in variable `$PWD`.
# Observe that the following are equivalent:
echo "I'm in $(pwd)" # execs `pwd` and interpolates output
echo "I'm in $PWD" # interpolates the variable

# If you get too much output in your terminal, or from a script, the command
# `clear` clears your screen
clear
# Ctrl-L also works for clearing output

# Reading a value from input:
echo "What's your name?"
read Name # Note that we didn't need to declare a new variable
echo Hello, $Name!

# We have the usual if structure:
# use `man test` for more info about conditionals
if [ $Name != $USER ]
then
    echo "Your name isn't your username"
else
    echo "Your name is your username"
fi
# True if the value of $Name is not equal to the current user's login username

# NOTE: if $Name is empty, bash sees the above condition as:
#if [ != $USER ]
# which is invalid syntax
# so the "safe" way to use potentially empty variables in bash is:
#if [ "$Name" != $USER ] ...
# which, when $Name is empty, is seen by bash as:
#if [ "" != $USER ] ...
# which works as expected

# There is also conditional execution
echo "Always executed" || echo "Only executed if first command fails"
# => Always executed
echo "Always executed" && echo "Only executed if first command does NOT fail"
# => Always executed
# => Only executed if first command does NOT fail

# A single ampersand & after a command runs it in the background. A background command's
# output is printed to the terminal, but it cannot read from the input.
sleep 30 &
# List background jobs
jobs # => [1]+  Running                 sleep 30 &
# Bring the background job to the foreground
fg
# Ctrl-C to kill the process, or Ctrl-Z to pause it
# Resume a background process after it has been paused with Ctrl-Z
bg
# Kill job number 2
kill %2
# %1, %2, etc. can be used for fg and bg as well

# To use && and || with if statements, you need multiple pairs of square brackets:
if [ "$Name" == "Steve" ] && [ "$Age" -eq 15 ]
then
    echo "This will run if $Name is Steve AND $Age is 15."
fi

if [ "$Name" == "Daniya" ] || [ "$Name" == "Zach" ]
then
    echo "This will run if $Name is Daniya OR Zach."
fi

# There is also the `=~` operator, which tests a string against a Regex pattern:
Email=me@example.com
if [[ "$Email" =~ [a-z]+@[a-z]{2,}\.(com|net|org) ]]
then
    echo "Valid email!"
fi
# Note that =~ only works within double [[ ]] square brackets,
# which are subtly different from single [ ].
# See https://www.gnu.org/software/bash/manual/bashref.html#Conditional-Constructs for more on this.

# Redefine command `ping` as alias to send only 5 packets
alias ping='ping -c 5'
# Escape the alias and use command with this name instead
\ping 192.168.1.1
# Print all aliases
alias -p

# Expressions are denoted with the following format:
echo $(( 10 + 5 )) # => 15

# Unlike other programming languages, bash is a shell so it works in the context
# of a current directory. You can list files and directories in the current
# directory with the ls command:
ls # Lists the files and subdirectories contained in the current directory

# This command has options that control its execution:
ls -l # Lists every file and directory on a separate line
ls -t # Sorts the directory contents by last-modified date (descending)
ls -R # Recursively `ls` this directory and all of its subdirectories

# Results (stdout) of the previous command can be passed as input (stdin) to the next command
# using a pipe |. Commands chained in this way are called a "pipeline", and are run concurrently.
# The `grep` command filters the input with provided patterns.
# That's how we can list .txt files in the current directory:
ls -l | grep "\.txt"

# Use `cat` to print files to stdout:
cat file.txt

# We can also read the file using `cat`:
Contents=$(cat file.txt)
# "\n" prints a new line character
# "-e" to interpret the newline escape characters as escape characters
echo -e "START OF FILE\n$Contents\nEND OF FILE"
# => START OF FILE
# => [contents of file.txt]
# => END OF FILE

# Use `cp` to copy files or directories from one place to another.
# `cp` creates NEW versions of the sources,
# so editing the copy won't affect the original (and vice versa).
# Note that it will overwrite the destination if it already exists.
cp srcFile.txt clone.txt
cp -r srcDirectory/ dst/ # recursively copy

# Look into `scp` or `sftp` if you plan on exchanging files between computers.
# `scp` behaves very similarly to `cp`.
# `sftp` is more interactive.

# Use `mv` to move files or directories from one place to another.
# `mv` is similar to `cp`, but it deletes the source.
# `mv` is also useful for renaming files!
mv s0urc3.txt dst.txt # sorry, l33t hackers...