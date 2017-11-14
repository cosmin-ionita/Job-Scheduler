# Job-Scheduler

Technically, this project is aimed to create an efficient algorithm for a Constraint Satisfaction Problem built around a Job Scheduling problem.

Basically, we have a set of tasks, each one with it's own duration and deadline, and a set of processors. Each job that is finished after the
deadline induces a cost. Also, a job may have other jobs as dependencies, meaning that the current job cannot be started until their dependencies (jobs) are
finished.

Our goal is to design a scheduling algorithm that outputs a scheduling solution of this jobs so that the overall cost is minimal.

## Solution approaches

The first solution is to explore the entire space of possible states of our problem and then to choose the one that induces a minimal cost. This
will be implemented using a backtracking algorithm.

Then, we will adjust this algorithm to get a better cost / time ratio. We will try to order the jobs in a specific way.

Finally, we will use a path-consistency approach in order to improve that ratio.