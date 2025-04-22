## Task
Write a parser for a custom directed graph structure format
(please refer to the **format specification** section below for details and to `./data/raw` for samples)

Parser signature:
  - **input**:  file path (string or `Path`)
  - **output**: ordered tabular graph representation (as a `pandas.DataFrame`)


## Format specification

### 1. Basics

Each file contains a text description of a directed graph structure.
A directed graph contains nodes connected by arrows (edges), each arrow has
an optional direction and an optional numerical value, for example:
```
A --[1]--> B --[2]-> C <-[3.75]- E -> A
           B --[4]-- D
```

A graph can be represented by a table with three columns:
  - `L` (left node)
  - `R` (right node)
  - `V` (the corresponding arrow value)

For example, the graph above in tabular form will look like this:

| L | R |   V   |
|---|---|-------|
| A | B |   1   |
| B | C |   2   |
| B | D |   4   |
| D | B |   4   |
| E | A |       |
| E | C | 3.75  |

The table above is the _ordered tabular graph representation_, which is the
parser output (a table is ordered first by `L` and then by `R`).


### 2. Details

The key structural elements are defined as follows:

  - **Node**

     A node is represented by a label, which satisfies the same requirements
     as Python variable name, i.e. it can only contain alphanumerical characters
     and the first character cannot be a digit.

     Examples:
       - valid:   `A`, `B_12`, `__N`
       - invalid: `0`, `A[0]`, `#B`

  - **Arrow**

     An arrow is a connection (optionally directed) between the nodes and is represented by a sequence
     of at least one `-`, optionally starting with `<` and/or ending with `>`; additionally,
     an arrow can contain a numerical value (floating-point literal) enclosed in square brackets,
     surrounded by at least one `-` on each side.

     Notes:
       - the value inside the brackets might contain spaces (but **not** new lines)
       - if an arrow doesn't explicitly specify a value, it is assumed to be `null`

     Examples:
       - valid:   `-`, `->`, `<->`, `------>`, `-[1.5]-`, `<-[7]-`, `<--[ .36 ]--->`
       - invalid: `>`, `<>`, `[0]`, `[]`, `[3]>`, `<[2.1]-`

The graph data is written as **Node** **Arrow** **Node** triplets, in plain text,
possibly with multiple triplets 'merged' into a single expression, e.g.
```
A -> B --> C <--[3]-- D - E
```
Each triplet within the expression should be read left to right, each expression
should be read top to bottom, as triplets can 'override' each other, for example:

1.
   ```
   A -> B <-[0]- A
   A -[2]-> B
   ```
   The second triplet of the first line (`B <-[0]- A`) 'overrides' the first triplet (`A -> B`).
   The second line 'overrides' the whole first line.

2.
   ```
   A <-> B
   A -[1]-> B
   B -[3]-> A
   A -[0]-> B
   ```
   Lines 2 and 3 collectively override line 1, line 4 overrides line 2,
   so the resulting graph is equivalent to:
   ```
   A -[0]-> B
   B -[3]-> A
   ```

#### Notes:

  1. **Arrow directionality:**

     Directionality of an arrow is determined by the presence of `<` and `>` symbols in it:
     if an arrow contains both or none, it is considered bidirectional, otherwise
     `>` denotes a 'right' connection and `<` denotes a 'left' one, for example:

       - `A -> B` reads " 'left' node `A` connects to the 'right' node `B`"
       - `A <- B` reads " 'left' node `B` connects to the 'right' node `A`"
       - `A - B`  is equivalent to the union of the two scenarios above


  2. **Partially invalid expressions:**

     If a triplet (whether a part of a bigger expression or not):  

       - contains an invalid label:  

          this particular triplet should be skipped, without affecting the whole expression.  
          For example, the following:
          ```
          #A -> 1 -> B <- C
          ```
          should pe parsed as if it were this:
          ```
          B <- C
          ```

       - contains an invalid arrow:  
         _in this case the behaviour of the parser is undefined_
