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

// Now that you know how to play, let's learn a little scala...

/////////////////////////////////////////////////
// 1. Basics
/////////////////////////////////////////////////

// Single-line comments start with two forward slashes

/*
  Multi-line comments, as you can already see from above, look like this.
*/

// Printing, and forcing a new line on the next print
println("Hello world!")
println(10)
// Hello world!
// 10

// Printing, without forcing a new line on next print
print("Hello world")
print(10)
// Hello world10

// Declaring values is done using either var or val.
// val declarations are immutable, whereas vars are mutable. Immutability is
// a good thing.
val x = 10 // x is now 10
x = 20     // error: reassignment to val
var y = 10
y = 20     // y is now 20

/*
  Scala is a statically typed language, yet note that in the above declarations,
  we did not specify a type. This is due to a language feature called type
  inference. In most cases, Scala compiler can guess what the type of a variable
  is, so you don't have to type it every time. We can explicitly declare the
  type of a variable like so:
*/
val z: Int = 10
val a: Double = 1.0

// Notice automatic conversion from Int to Double, result is 10.0, not 10
val b: Double = 10

// Boolean values
true
false

// Boolean operations
!true         // false
!false        // true
true == false // false
10 > 5        // true

// Math is as per usual
1 + 1   // 2
2 - 1   // 1
5 * 3   // 15
6 / 2   // 3
6 / 4   // 1
6.0 / 4 // 1.5
6 / 4.0 // 1.5


// Evaluating an expression in the REPL gives you the type and value of the result

1 + 7

/* The above line results in:

  scala> 1 + 7
  res29: Int = 8

  This means the result of evaluating 1 + 7 is an object of type Int with a
  value of 8

  Note that "res29" is a sequentially generated variable name to store the
  results of the expressions you typed, your output may differ.
*/

"Scala strings are surrounded by double quotes"
'a' // A Scala Char
// 'Single quote strings don't exist' <= This causes an error

// Strings have the usual Java methods defined on them
"hello world".length
"hello world".substring(2, 6)
"hello world".replace("C", "3")

// They also have some extra Scala methods. See also: scala.collection.immutable.StringOps
"hello world".take(5)
"hello world".drop(5)

// String interpolation: notice the prefix "s"
val n = 45
s"We have $n apples" // => "We have 45 apples"

// Expressions inside interpolated strings are also possible
val a = Array(11, 9, 6)
s"My second daughter is ${a(0) - a(2)} years old."    // => "My second daughter is 5 years old."
s"We have double the amount of ${n / 2.0} in apples." // => "We have double the amount of 22.5 in apples."
s"Power of 2: ${math.pow(2, 2)}"                      // => "Power of 2: 4"

// Formatting with interpolated strings with the prefix "f"
f"Power of 5: ${math.pow(5, 2)}%1.0f"         // "Power of 5: 25"
f"Square root of 122: ${math.sqrt(122)}%1.4f" // "Square root of 122: 11.0454"

// Raw strings, ignoring special characters.
raw"New line feed: \n. Carriage return: \r." // => "New line feed: \n. Carriage return: \r."

// Some characters need to be "escaped", e.g. a double quote inside a string:
"They stood outside the \"Rose and Crown\"" // => "They stood outside the "Rose and Crown""

// Triple double-quotes let strings span multiple rows and contain quotes
val html = """<form id="daform">
                <p>Press belo', Joe</p>
                <input type="submit">
              </form>"""

/////////////////////////////////////////////////
// 2. Functions
/////////////////////////////////////////////////

// Functions are defined like so:
//
//   def functionName(args...): ReturnType = { body... }
//
// If you come from more traditional languages, notice the omission of the
// return keyword. In Scala, the last expression in the function block is the
// return value.
def sumOfSquares(x: Int, y: Int): Int = {
  val x2 = x * x
  val y2 = y * y
  x2 + y2
}

// The { } can be omitted if the function body is a single expression:
def sumOfSquaresShort(x: Int, y: Int): Int = x * x + y * y

// Syntax for calling functions is familiar:
sumOfSquares(3, 4)  // => 25

// You can use parameters names to specify them in different order
def subtract(x: Int, y: Int): Int = x - y

subtract(10, 3)     // => 7
subtract(y=10, x=3) // => -7

// In most cases (with recursive functions the most notable exception), function
// return type can be omitted, and the same type inference we saw with variables
// will work with function return values:
def sq(x: Int) = x * x  // Compiler can guess return type is Int

// Functions can have default parameters:
def addWithDefault(x: Int, y: Int = 5) = x + y
addWithDefault(1, 2) // => 3
addWithDefault(1)    // => 6


// Anonymous functions look like this:
(x: Int) => x * x

// Unlike defs, even the input type of anonymous functions can be omitted if the
// context makes it clear. Notice the type "Int => Int" which means a function
// that takes Int and returns Int.
val sq: Int => Int = x => x * x

// Anonymous functions can be called as usual:
sq(10)   // => 100

// If each argument in your anonymous function is
// used only once, Scala gives you an even shorter way to define them. These
// anonymous functions turn out to be extremely common, as will be obvious in
// the data structure section.
val addOne: Int => Int = _ + 1
val weirdSum: (Int, Int) => Int = (_ * 2 + _ * 3)

addOne(5)      // => 6
weirdSum(2, 4) // => 16


// The return keyword exists in Scala, but it only returns from the inner-most
// def that surrounds it.
// WARNING: Using return in Scala is error-prone and should be avoided.
// It has no effect on anonymous functions. For example here you may expect foo(7) should return 17 but it returns 7:
def foo(x: Int): Int = {
  val anonFunc: Int => Int = { z =>
    if (z > 5)
      return z // This line makes z the return value of foo!
    else
      z + 2    // This line is the return value of anonFunc
  }
  anonFunc(x) + 10  // This line is the return value of foo
}

foo(7) // => 7

/////////////////////////////////////////////////
// 3. Flow Control
/////////////////////////////////////////////////

1 to 5
val r = 1 to 5
r.foreach(println)

r foreach println
// NB: Scala is quite lenient when it comes to dots and brackets - study the
// rules separately. This helps write DSLs and APIs that read like English

// Why doesn't `println` need any parameters here?
// Stay tuned for first-class functions in the Functional Programming section below!
(5 to 1 by -1) foreach (println)

// A while loop
var i = 0
while (i < 10) { println("i " + i); i += 1 }

while (i < 10) { println("i " + i); i += 1 }   // Yes, again. What happened? Why?

i    // Show the value of i. Note that while is a loop in the classical sense -
     // it executes sequentially while changing the loop variable. while is very
     // fast, but using the combinators and comprehensions above is easier
     // to understand and parallelize

// A do-while loop
i = 0
do {
  println("i is still less than 10")
  i += 1
} while (i < 10)

// Recursion is the idiomatic way of repeating an action in Scala (as in most
// other functional languages).
// Recursive functions need an explicit return type, the compiler can't infer it.
// Here it's Unit, which is analagous to a `void` return type in Java
def showNumbersInRange(a: Int, b: Int): Unit = {
  print(a)
  if (a < b)
    showNumbersInRange(a + 1, b)
}
showNumbersInRange(1, 14)


// Conditionals

val x = 10

if (x == 1) println("yeah")
if (x == 10) println("yeah")
if (x == 11) println("yeah")
if (x == 11) println("yeah") else println("nay")

println(if (x == 10) "yeah" else "nope")
val text = if (x == 10) "yeah" else "nope"

/////////////////////////////////////////////////
// 4. Data Structures
/////////////////////////////////////////////////

val a = Array(1, 2, 3, 5, 8, 13)
a(0)     // Int = 1
a(3)     // Int = 5
a(21)    // Throws an exception

val m = Map("fork" -> "tenedor", "spoon" -> "cuchara", "knife" -> "cuchillo")
m("fork")         // java.lang.String = tenedor
m("spoon")        // java.lang.String = cuchara
m("bottle")       // Throws an exception

val safeM = m.withDefaultValue("no lo se")
safeM("bottle")   // java.lang.String = no lo se

val s = Set(1, 3, 7)
s(0)      // Boolean = false
s(1)      // Boolean = true

/* Look up the documentation of map here -
 * https://www.scala-lang.org/api/current/scala/collection/immutable/Map.html
 * and make sure you can read it
 */


// Tuples

(1, 2)

(4, 3, 2)

(1, 2, "three")

(a, 2, "three")

// Why have this?
val divideInts = (x: Int, y: Int) => (x / y, x % y)

// The function divideInts gives you the result and the remainder
divideInts(10, 3)    // (Int, Int) = (3,1)

// To access the elements of a tuple, use _._n where n is the 1-based index of
// the element
val d = divideInts(10, 3)    // (Int, Int) = (3,1)

d._1    // Int = 3
d._2    // Int = 1

// Alternatively you can do multiple-variable assignment to tuple, which is more
// convenient and readable in many cases
val (div, mod) = divideInts(10, 3)

div     // Int = 3
mod     // Int = 1

