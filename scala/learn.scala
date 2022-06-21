/////////////////////////////////////////////////
// 0. Basics
/////////////////////////////////////////////////
/*
  Setup Scala:

  1) Download Scala - http://www.scala-lang.org/downloads
  2) Unzip/untar to your favorite location and put the bin subdir in your `PATH` environment variable
*/

/*
  Try the REPL

  Scala has a tool called the REPL (Read-Eval-Print Loop) that is analogous to
  commandline interpreters in many other languages. You may type any Scala
  expression, and the result will be evaluated and printed.

  The REPL is a very handy tool to test and verify code.  Use it as you read
  this tutorial to quickly explore concepts on your own.
*/

// Start a Scala REPL by running `scala`. You should see the prompt:
$ scala
scala>

// By default each expression you type is saved as a new numbered value
scala> 2 + 2
res0: Int = 4

// Default values can be reused.  Note the value type displayed in the result..
scala> res0 + 2
res1: Int = 6

// Scala is a strongly typed language. You can use the REPL to check the type
// without evaluating an expression.
scala> :type (true, 2.0)
(Boolean, Double)

// REPL sessions can be saved
scala> :save /sites/repl-test.scala

// Files can be loaded into the REPL
scala> :load /sites/repl-test.scala
Loading /sites/repl-test.scala...
res2: Int = 4
res3: Int = 6

// You can search your recent history
scala> :h?
1 2 + 2
2 res0 + 2
3 :save /sites/repl-test.scala
4 :load /sites/repl-test.scala
5 :h?