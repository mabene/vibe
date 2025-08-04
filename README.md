# Tower of Hanoi Solver: A Human-AI Collaboration Experiment

This project is a flexible, educational solver for (variations over) the Tower of Hanoi puzzle. It is a small scale (~5k LOC, ~50 files, ~20 classes) project developed as an experiment in "**vibe coding**," a novel software development paradigm where a human programmer ([me](https://www.linkedin.com/in/marco-benedetti-art), in this case) collaborates with AI assistants (specifically [Claude Sonnet 4](https://claude.ai/) and [Gemini 2.5 Pro](https://gemini.google.com/)) to produce code and documentation.

In this particular experiment, **100% of the codebase and documentation** (including this README) were generated through iterative dialogue between the human programmer and the AI agents, with no code or text written directly by the human. All interactions took place within [Cursor](https://cursor.sh/), providing a seamless environment for human-AI collaborative programming.

For more information about this vibe coding experiment, please check the article ["Vibe Coding as a Coding Veteran"](https://medium.com/@maxbene/vibe-coding-as-a-coding-veteran-cd370fe2be50), on Medium - or on [my substack](https://open.substack.com/pub/marcobenedetti/p/vibe-coding-as-a-coding-veteran).
**Note**: The above mentioned article is the only piece of text written by the human programmer, not by the AI.

As supplementary reading material, this repository also contains the following (AI-generated) content:
- **[vibe_coding.md](./docs/vibe_coding.md)** - Development goals and methodology, analysis of the collaborative process, observations on bias and features of the AI-generated code, and conclusions on productivity gains;
- **[TLDR.md](./docs/TLDR.md)** - A short summary of the findings from the main human-written ["Vibe Coding as a Coding Veteran"](https://medium.com/@maxbene/vibe-coding-as-a-coding-veteran-cd370fe2be50) piece;
- **[sample_exchanges.md](./docs/sample_exchanges.md)** - A few examples of short Human/AI interactions that happened during the development process;
- **[sample_chats](./docs/sample_chats/)** - Ten longer snippets of Human/AI dialogues in "raw" Cursor format.


## Overview

The solver can handle both the classical version of the puzzle and generalized versions with (a) **arbitrary** start and end configurations, and (b) **multiple** disks liftable at once. It features a clean, well-documented codebase built on Pythonic best practices.

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Quick Start

```bash
python3 hanoi.py -c 3                    # Solve 3-disk classical puzzle  
python3 hanoi.py -c 4 -s COMPARE         # Compare all algorithms
python3 hanoi.py -r 5 --show moves       # Random 5-disk puzzle with moves
python3 hanoi.py -i "1,2:3:: > ::1,2,3"  # Custom puzzle instance
```

## Usage

The script is executed directly from the project directory.

### Solving a Classical Puzzle

To solve a classical puzzle (all disks starting on peg 1 and moving to another peg), use the `-c` or `--classic` flag followed by the number of disks.

```bash
# Solve a 4-disk classical puzzle
python3 hanoi.py -c 4

# Show the full state-by-state solution
python3 hanoi.py -c 3 --show states
```

### Solving a Random Puzzle

To find the shortest path between two randomly generated, valid puzzle states, use the `-r` or `--random` flag.

```bash
# Find a solution between two random 5-disk configurations
python3 hanoi.py -r 5 --show moves
```

Output from the above command:
```
--- Searching for a solution between two random 5-disk states ---

Initial State:
     |            |            |     
     |            |            |     
     |            |           _|_    
     |          __|__       ___|___  
     |       _____|_____   ____|____ 

Target State:
     |            |            |     
     |            |            |     
   __|__          |            |     
  ___|___         |           _|_    
_____|_____       |        ____|____ 

Shortest solution found in 0.0009 seconds: 10 moves required.

Solution:
  Move 1: 1 disk from peg 3 to peg 1
  Move 2: 1 disk from peg 2 to peg 3
  Move 3: 1 disk from peg 1 to peg 3
  Move 4: 1 disk from peg 2 to peg 1
  Move 5: 1 disk from peg 3 to peg 1
  Move 6: 1 disk from peg 3 to peg 2
  Move 7: 1 disk from peg 1 to peg 2
  Move 8: 1 disk from peg 3 to peg 1
  Move 9: 1 disk from peg 2 to peg 3
  Move 10: 1 disk from peg 2 to peg 1
```

*Note*: Any arbitrary initial configuration with disks randomly distributed across all pegs (respecting the traditional Hanoi invariant that larger disks are never placed on top of smaller ones) can always be transformed into any other such valid configuration using a proper sequence of traditional Hanoi moves—a solution is guaranteed to exist. The proof is left as an exercise to the reader.

### Solving a Custom Instance

To solve a specific puzzle configuration that you define, use the `-i` or `--instance` flag with a custom specification.

```bash
# Move all disks from peg 1 to peg 3 (equivalent to classic but explicit)
python3 hanoi.py -i "1,2,3:: > ::1,2,3"

# Solve a custom 4-disk arrangement
python3 hanoi.py -i "1,2:3:4 > ::1,2,3,4" -s BFS

# Complex custom instance with specific disk arrangements
python3 hanoi.py -i "1,2:3,4:5,6 > 4,5,6::1,2,3" --show moves
```

The custom instance format uses `INITIAL>FINAL` where each state is specified as `PEG1:PEG2:PEG3`:
- Disks are listed from **top to bottom** (smallest to largest numbers)
- Empty pegs are represented as empty strings between colons
- Disk numbers can be any positive integers (they don't need to be consecutive)
- Spaces are allowed everywhere, for a more human-readable layout of instances

### Search algorithms

This software implements a suite of search algorithms, from scratch: Direct Recursive, Breadth-First Search, Depth-First Search, Iterative Deepening, A\* Search, Iterative Deepening A\*, Greedy Best-First Search, Bidirectional Breadth-First Search, Parallel Bidirectional Breadth-First Search.

### Benchmarking

To compare all available algorithms on more complex puzzles, use the `COMPARE` mode with profiling enabled:

```bash
python3 hanoi.py -s COMPARE -r 9 -l 2 --timeout 5 --profile 10
```

This command compares all available algorithms on 10 random instances with 9 disks, allowing up to 2 disks to be lifted at once, with a 5-second timeout per solver per instance:

```
=====================================================================================================================================================
🏆 MULTI-INSTANCE ALGORITHM COMPARISON RESULTS (10 instances)
=====================================================================================================================================================
Algorithm    | Timeouts     | Time (s)               | Moves               | Generated    | Explored     | Ratio        | Frontier     | Iterations   
-----------------------------------------------------------------------------------------------------------------------------------------------------
BFS          | -            | 0.1791 [0.0096-0.3468] | 20.1 [9-30]         | 22319        | 9498         | 42.6%        | 2659         | -           
GBFS         | -            | 0.2637 [0.0021-0.7704] | 22.0 [9-48]         | 3175         | 1235         | 38.9%        | 895          | -           
ASTAR        | -            | 0.5677 [0.0041-1.0687] | 20.1 [9-30]         | 7138         | 6252         | 87.6%        | 968          | -           
BIBFS        | -            | 0.5683 [0.0018-1.2031] | 20.1 [9-30]         | 3222         | 2438         | 75.7%        | 793          | -           
DFS          | -            | 1.1630 [0.0549-3.7030] | 5402.9 [1583-10216] | 19589        | 8328         | 42.5%        | 9820         | -           
PBIBFS       | -            | 2.5385 [0.3604-5.0061] | 20.1 [9-30]         | 9959         | 8892         | 89.3%        | <=1218       | -           
IDE          | 8 (5s)       | 4.1188 [0.2190-5.0000] | 10.5 [9-12]         | 12929        | 12926        | 100.0%       | 34           | 12          
IDASTAR      | 9 (5s)       | 4.5312 [0.3119-5.0000] | 9.0                 | 5613         | 1202         | 21.4%        | 10           | 7           
=====================================================================================================================================================

Legend:
- Timeouts: number of instances that timed out, if any
- Time: average execution time across all instances, in seconds
- Moves: average number of moves in the solution found (successful instances only)
- Generated: average number of nodes/states generated during search
- Explored: average number of nodes/states explored during search
- Ratio: search efficiency as (Explored/Generated)*100%
- Frontier: maximum number of entries in the search queue/stack
- Iterations: maximum search depth (iterative deepening variants only)
- [min-max]: range of values across instances where applicable
====================================================================================================================================================
```

### Other Features

For the complete list of command-line options and detailed usage information, see the [full help documentation](docs/help.txt) or run:

```bash
python3 hanoi.py -h
```


