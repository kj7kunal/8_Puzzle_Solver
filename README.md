# 8 Puzzle Solver

## Description

The code takes the goal state of the 8-puzzle, and randomly shuffles it n number of times and then A* algorithm is applied to solve the resulting puzzle using 4 heuristics as follows:

### Heuristic-1. Zero

This is the case of the Djikstra search, where there is no heuristic and the nodes are expanded according to normal breadth first search.

ha(n) = 0 


### Heuristic-2. Euclidean Distance

This is the "ordinary" straight-line distance between two points in Euclidean space. It is also called the L2 distance/L2 norm.

he(n) = Σ19{ sqrt((target_row - current_row)^2 + (target_col – current_col)**2) }


### Heuristic-3. Chessboard/Chebyshev Distance

This is a metric defined on a vector space where the distance between two vectors is the greatest of their differences along any coordinate dimension.

hc(n) = Σ19{ max(|target_row – current_row|, |target_col – current_col|) }


### Heuristic-4. Manhattan Distance

This is a metric in which the distance between two points is the sum of the absolute differences of their Cartesian coordinates. It is also called the L1 distance/L1 norm.

hm(n) = Σ19{ |target_row - current_row| + |target_col – current_col| }

## Inference

It can be inferred that out of the 4 heuristics, the following order is followed both in the case of the number of nodes expanded and the time taken to do so:

ZERO > EUCLIDEAN > CHEBYSHEV > MANHATTAN
