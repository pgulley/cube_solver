

Paul Gulley  |  March 2015 | Cube Solver
===========================
Tools for solving a puzzle which has been on my desk for ages
---------------

We have a sequence of 64 wooden cubes strung together. 
There are 44 right-angle bends at irregular positions along this string.
We want to bend the string such that it forms one 4x4 cube.

![The puzzle](http://cdn.shopify.com/s/files/1/0181/8685/products/snakecube4x4f_1024x1024.jpg?v=1352159392)

Setting this up as a search problem, going depth first. 

###The constraints

Accounting for symmetry, There are 4 starting positions. We can start off in any of 6 directions, and each of the 44 bends offers 4 new possible directions.
The space contains around 4^45 possibilities, or
**300 quadrillion states**

Its too chaotic for many optimizations, but we have a few things on our side:
  * Symmetry allows for some starting positions to be ignored.
  * We don't check past failure, so we can throw out whole branches as we go.
  * If we need to, we can start checking for cube segmentation, which would let us 
		throw out more dead ends (not implemented yet, though)

On my machine it runs at 1 million loops every 15 seconds, or 5.7 billion loops per day.

For some reason, the script halts after about 830 million steps, around 4 hours in.
Fails to find solution. Further investigation to follow

