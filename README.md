# lab
### lane changing and merging
#### generate input.py:
Generates the input of vehicles based on a Poisson Distribution
#### input.py
Preprocesses the inputs into a Vehicle class
#### run.py
The flow of the whole experiment
#### greedyV1.py dpV1.py
Decides the passing orders based on each algorithm
#### test.py
Simulates and outputs the time consumption for all vehicles to pass
#### verify.py
Makes sure constraints for problem formulation aren't violated

#### makefile
```
make ingen
```
This command generates the input for different cases
```
make target
```
This command runs the experiment for each case and outputs the time consumption of different algorithms for each case

### load balancing
#### generate input.py:
Generates the input of vehicles based on a Poisson Distribution
#### input.py
Preprocesses the inputs into a Vehicle class
#### loadV7.py
Deals with balancing loads on outgoing lanes
#### FCFS.py Heuristic
Decide how vehicles enter the outgoing lanes
#### two_phase.py
Combines load distribution methods and passing order decision methods

#### makefile
```
make ingen
```
This command generates the input for different cases
```
make target
```
This command runs the experiment for cases with 3 incoming lanes
```
make target1
```
This command runs the experiment for cases with 4 incoming lanes
