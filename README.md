
This is our group's work for **Assignment 5.1*

## What this project is about

The Fibonacci sequence goes 0, 1, 1, 2, 3, 5, 8, 13, and so on. Every number is the sum of the two before it. It's an easy rule, but there are two very different ways to turn it into code, and one of them is far slower than the other.

**Algorithm A (plain recursion)** finds F(n) by asking for F(n-1) and F(n-2) and adding them. The problem is that it remembers nothing, so it ends up solving the same small problems again and again.

**Algorithm B (memoization)** does the same thing, but it saves every answer in a table. When it needs an answer it has already worked out, it just looks it up instead of calculating it again.

## What we did

We counted how many times each function calls itself and timed how long each one takes. We then plotted the results and used simple maths to explain what we saw, including proving the call-count formulas by induction.

## What we found

The difference was huge. At n = 35, plain recursion made almost 30 million calls and took over 2 seconds. Memoization made only 69 calls. The reason is that Algorithm A grows exponentially, while Algorithm B grows in a straight line, needing only 2n - 1 calls.

We also tried to push to n = 1000. Plain recursion would need around 10^209 calls, which would take far longer than the age of the universe, so it is simply not possible. Memoization did it in about one millisecond, but only after we fixed a problem: Python stops recursion at 1000 levels by default, so it crashed with a RecursionError. We solved it by raising the recursion limit and, as a second option, by using a simple loop instead of recursion.

Finally, we looked at why n = 0 can be tricky when checking the table. Since 0 counts as "false" in Python, a careless check can think F(0) was never saved. In our tests this didn't change the answer, but writing the check as `n in fibtable` is the safe way.

## How to run it

You need Python 3 and the `matplotlib` library:

```
pip install matplotlib
python fibonacci_assignment.py
```

The program prints the results and creates the results file and graphs in the same folder.
