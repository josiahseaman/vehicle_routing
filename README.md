# Vehicle Routing Problem
## To install
- Create a Python 3.12 virtual environment in the local folder `.venv/`
- `pip install -r requirements.txt`
- It's really just pandas.

## To Run
- The command I gave to evaluateShared.py is `--problemDir problems --cmd "./.venv/Scripts/python main.py"`
- I found it necessary to give the path to my virtualenv because `subprocess.check_output(cmd)`
starts a new terminal which does have it activated
- Note: I had to fix a small bug in evaluateShared.py that was not scrubbing Windows newlines
    `line = line.replace("\r", "")`
- Unit tests are in tests.py and can be executed directly: `./.venv/Scripts/pytho tests.py`


# Notes on Process
[Vorto Challenge Problem](https://drive.google.com/drive/folders/1Jb7FmR5Ftrg0jwgIJ-n_oKwOjyJ4gDHI) 
Given a list of <200 loads with a start and stop coordinate, find the shortest collection of paths from (0,0)
That visits all loads.
`total_cost = 500*number_of_drivers + total_number_of_driven_minutes`

 Drivers are assumed a constant rate of 1 mile per minute, as the crow flies.

## Initial Thoughts:
- Multiple constraint satisfaction
- Start by trying to fill the largest available space first
- Add one more driver each time no possible slots are available
- Start by allocating the longest distance first
- Wait to iterate over possible choices until after a basic solution has been accomplished
- Would adding a driver affect our proposed solution from the start? If we're always picking the objectively largest
    route then the answer is no.
- Next generation will be to pick and positions that are close to pick up locations.
- Construct all possible pairs of loads as a distance
- Start by finding the shortest pair for each possible load, then check time remaining
- Each load can have three perspective pairs and then we iterate over a decision tree of triple branches for selecting
    subsequent loads
- 30 second run time means that we can't exhaustively search all loads. Test this hypothesis. How long would it take?
- Fewer than 200 loads is still a massive combinatorial space, but best for search might be able to prune branching
    dimension down to three or less.


## Solutions
There are a total of 3 solvers in drive_solver.py.  Each builds on the previous.
- GreedyPacker - place the largest load into the driver assignment that is already closest to pickup
- TripOptimizer - calculates neighbor_map, a sorted list of directed distances which is used to define the neighbor for
search of likely good solutions.
- StochasticTripOptimizer - Uses TripOptimizer to generate assignments, but shuffles the "first pick" for each
decision so that a larger space can be explored. This checks for "sub-optimal" initial choices that lead to
a more optimal collective solution.

Leverages TripOptimizer, however this function explores a larger space of likely good solutions
by randomizing some of the earlier (closest) neighbors. This means it can pick the 3rd or 10th closest
neighbor on one iteration. Which neighbor is picked is a key factor because it means the next driver
won't be able to pickup the same load. Having one optimized driver pickup a load can lead to subsequent
drivers having less optimized routes. Therefore a bit of sub-optimal at the beginning can lead to better
results overall.

## Rejected Solutions
Under normal circumstances I'd use a library which solves a travelling salesman or VRP after defining the context.
https://en.wikipedia.org/wiki/Vehicle_routing_problem#Metaheuristic
https://www.academia.edu/40719693/_Paolo_Toth_Daniele_Vigo_eds_Vehicle_Routing_z_lib_org_
https://en.wikipedia.org/wiki/Tabu_search#Pseudocode
https://en.wikipedia.org/wiki/Simulated_annealing#Pseudocode
“In the traveling salesman problem above, for example, swapping two consecutive cities in a low-energy tour is 
expected to have a modest effect on its energy (length); whereas swapping two arbitrary cities is far more likely 
to increase its length than to decrease it. Thus, the consecutive-swap neighbor generator is expected to perform 
better than the arbitrary-swap one, even though the latter could provide a somewhat shorter path to the optimum.”
https://github.com/perrygeo/simanneal
https://en.wikipedia.org/wiki/2-opt
https://www.theoj.org/joss-papers/joss.02408/10.21105.joss.02408.pdf
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.basinhopping.html#scipy.optimize.basinhopping
https://www.academia.edu/40719693/_Paolo_Toth_Daniele_Vigo_eds_Vehicle_Routing_z_lib_org_
https://stackoverflow.com/questions/25585401/travelling-salesman-in-scipy

However, any of these solutions would look very similar to solutions you've already seen.  I decided to create a 
solution that is controllable and deterministic logic but one that still defines a neighborhood in which simulated
annealing is viable. 

## Future Directions
- Build a set of individual driver assignments using create_shuffled_neighbors_map() then make a method for picking
a set of non-overlapping routes (pruning)
- Do simulated annealing by cutting routes in half and swapping with another driver
