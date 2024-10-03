"""
Vorto Challenge Problem: https://drive.google.com/drive/folders/1Jb7FmR5Ftrg0jwgIJ-n_oKwOjyJ4gDHI
Given a list of <200 loads with a start and stop coordinate, find the shortest collection of paths from (0,0)
That visits all loads.
 total_cost = 500*number_of_drivers + total_number_of_driven_minutes

 Drivers are assumed a constant rate of 1 mile per minute, as the crow flies.

Line of Reasoning:
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
"""


def main(folder):
    print(folder)


if __name__ == "__main__":
    main("problems/")
