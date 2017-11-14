from copy import copy, deepcopy
from itertools import combinations

from argparse import ArgumentParser, Namespace

# [NAME]        Ionita Costel-Cosmin 343C1

# [VERSION]     Brute space search


# This returns the constraints relevant for a specific solution
def fixed_constraints(solution, constraints):
	result = {}

	for key in solution.keys():
		for task in solution[key]:
                        # task[0] is actually the job id
			if len(constraints[task[0]]) > 0:
				result[task[0]] = constraints[task[0]]

	return result

# This checks if a constrained is satisfied or not by a solution
def check_constraint(solution, full_constraint):

	# This is the job that we compare against
	dependant_job = -1

	# This will store the ending times of each job
	acumulator = []

	for dep in full_constraint[1]:
		for key in solution:
			for job in solution[key]:
				if job[0] == dep:
					acumulator.append(job[1] + job[2])	# take the ending time of each dep
				elif job[0] == full_constraint[0]:
					dependant_job = job[1]

	if len(acumulator) < len(full_constraint[1]):
		return False

	if dependant_job == -1:
		print("ERROR IN CHECK CONSTRAINT: JOB = -1")

	# if the latest finishing job finishes before starting the reference job then we return true
	if max(acumulator) <= dependant_job:
		return True
	else:
		return False


# This function checks if a job is already scheduled in a (partial) solution
def existent_job(val, solution):

    for key in solution:
	    for job in solution[key]:
                if job[0] == val[0]:
                    return True
    return False


#   A solution looks like that:
#       [proc_id] : [(job_id, scheduled_start_time, duration, timeout), (...), (...), ...]
#


# This is the core function of the algorithm
def PCSP(processors, domain, constraints, acceptable_cost, solution, cost, proc_index, jobs_count):
    
    global N
    global best_cost
    global best_solution
    

    # If we reach the dimension of a full solution
    if jobs_count == N:
        
        print("New best: " + str(cost) + " - " + str(solution))
        
        best_solution = solution
        best_cost = cost
        
        if cost <= acceptable_cost:
            return True
        else:
            return False

    # If we reach the best cost
    elif cost == best_cost:
        return False
    else:

        # Here we switch the processor id to 0 when we reach the end
        if proc_index == len(processors):
               proc_index = 0

        # We will traverse the entire domain space
        domain_size = len(domain)
        
	for i in xrange(1, domain_size + 1):

                # We take the id of the processor we'll assign the next job
		proc = processors[proc_index]

                # We take the next job from the domain
                job = domain[i - 1]

                # We adjust the job retrieval for the last index
                if i == domain_size + 1:
                    job = domain[i - 2]

                # If the job is already present in the solution then we move to the next one
                if existent_job(job, solution) == True:
                    continue

		# We now start to build the next solution
		new_solution = deepcopy(solution)


                # [See the top of this function for the solution structure]
		if proc not in new_solution:
			new_solution[proc] = [(job[0], 0, job[1], job[2])]
		else:
			(job_id, start_time, duration, timeout) = new_solution[proc][-1]

			new_solution[proc].append((job[0], start_time + duration, job[1], job[2]))

		# Take the appropriate constraints
	        new_constraints = fixed_constraints(new_solution, constraints)

                # This section moves to the next job if at least a constraint is not satisfied
		continue_set = False

	        for constr_key in new_constraints:
		    if check_constraint(new_solution, (constr_key, new_constraints[constr_key])) == False:
                        continue_set = True
                	break

                if continue_set == True:
                    continue

                # Build the new cost
		new_cost = cost

		(job_id, start_time, duration, timeout) = new_solution[proc][-1]
		new_cost += max(0, start_time + duration - timeout)

                # If we get a better cost, we go down on that solution
		if new_cost < best_cost:
			result = PCSP(processors, deepcopy(domain), constraints, acceptable_cost, new_solution, new_cost, proc_index + 1, jobs_count + 1)
			if result == True:
				return True

        # If we finished all the cases, then return false
	return False

# Prototype function that calls the main algorithm function
def run_pcsp(acceptable_cost):
    
    global N
    global best_cost
    global best_solution
    

    processors = []
    domain = []
    constraints = {}

    arg_parser = ArgumentParser()
    arg_parser.add_argument("in_file", help="Input file")
   
    args = arg_parser.parse_args()

    with open(args.in_file) as f:

            # Reads the first line
	    N, P = [int(x) for x in next(f).split(",")]

            # Creates the "variables" for our algorithm
	    processors = [i for i in range(P)]

            # For each line, we store the domain and the constraints
	    for line in f:
		numbers = line.split(",")

		domain.append((int(numbers[0]), int(numbers[1]), int(numbers[2])))

		constraints[int(numbers[0])] = map(lambda x: int(x), numbers[3:])

    best_solution = {}
    best_cost = 100000

    PCSP(processors, deepcopy(domain), constraints, acceptable_cost, {}, 0, 1, 0)

    print("Best found: " + str(best_cost) + " - " + str(best_solution))


    f = open('output_file', 'w')

    for key in best_solution.keys():
	f.write(str(len(best_solution[key])) + '\n')

	for job in best_solution[key]:
		f.write(str(job[0]) + ',' + str(job[1]) + '\n')	
    
    f.close()

run_pcsp(1)
