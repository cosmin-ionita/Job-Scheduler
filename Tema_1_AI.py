from copy import copy, deepcopy
from itertools import combinations


def get_constraints(var, constraints):
    return list(filter(lambda x: var in x[0], constraints))


def fixed_constraints(solution, constraints):
	result = {}

	for key in solution.keys():
		for task in solution[key]:
			if len(constraints[task[0]]) > 0:
				result[task[0]] = constraints[task[0]]

	return result

def check_constraint(solution, full_constraint):
	
	# Iterez prin lista de dependinte (ful

	dependant_job = -1
	acumulator = []

	for dep in full_constraint[1]:
		for key in solution:
			for sarcina in solution[key]:
				if sarcina[0] == dep:
					acumulator.append(sarcina[1] + sarcina[2])	# iau timpul de final al tuturor job-urilor dep
				elif sarcina[0] == full_constraint[0]:
					dependant_job = sarcina[1]	# iau timpul de start a job-ului de rerefinta

	#print("Am solutia: ")
	#print(solution)

	#print("Am constraints: ")
	#print(full_constraint)

	if len(acumulator) < len(full_constraint[1]):
		return False

	if dependant_job == -1:
		print("EROARE!! JOB == -1")

	if len(acumulator) == 0:
		print("SOLUTION = ")
		print(solution)
		print("constraint: ")
		print(full_constraint)
		print("accumulator: ")
		print(acumulator)


	# daca jobul care se termina cel mai tarziu se termina inaintea inceperii job-ului de referinta
	if max(acumulator) <= dependant_job:
		return True
	else:
		return False

def PCSP(vars, domains, constraints, acceptable_cost, solution, cost, vars_index):
    global best_solution
    global best_cost

    # Nu mai avem sarcini, deci am ajuns la o solutie mai buna
    if not domains:# and check_solution(solution):
        
        print("New best: " + str(cost) + " - " + str(solution))
        
        best_solution = solution
        best_cost = cost
        
        if cost <= acceptable_cost:
            return True
        else:
            return False

    # Am ajuns la un cost egal cu cel mai bun, deci nu avem cum sa gasim unul si mai bun
    elif cost == best_cost:
        return False

    # Altfel
    else:
        
	if vars_index == len(vars):
		vars_index = 0

 	# Luam prima variabila si prima valoare
        var = vars[vars_index]
        val = domains.pop(0)

	#test_val = val

        new_solution = deepcopy(solution)

        # Construim noua solutie
        if var not in new_solution:
		new_solution[var] = [(val[0], 0, val[1], val[2])]
        else:
		(sarcina, start_time, durata, timeout) = new_solution[var][-1]

		new_solution[var].append((val[0], start_time + durata, val[1], val[2]))
    
        # Calculam costul noii solutii partiale
        new_cost = cost
        

        # Luam restrictiile ce pot fi evaluate pentru solutia asta noua
        new_constraints = fixed_constraints(new_solution, constraints)

        for constr_key in new_constraints:
            
	    if check_constraint(new_solution, (constr_key, new_constraints[constr_key])) == False:
		return False

	(sarcina, start_time, durata, timeout) = new_solution[var][-1]
	new_cost += max(0, start_time + durata - timeout) 
	
        # Daca noul cost este mai bun decat cel mai bun cost, mergem recursiv pe variabile
        if new_cost < best_cost:
            if PCSP(vars, deepcopy(domains), constraints, acceptable_cost, new_solution, new_cost, vars_index + 1):
                return True

	for i in xrange(1, len(domains)):

		domains.insert(i, val)

		var = vars[vars_index]
		val = domains.pop(0)

		second_solution = deepcopy(solution)

		# Construim noua solutie
		if var not in second_solution:
			second_solution[var] = [(val[0], 0, val[1], val[2])]
		else:
			(sarcina, start_time, durata, timeout) = second_solution[var][-1]

			second_solution[var].append((val[0], start_time + durata, val[1], val[2]))

		# Luam restrictiile ce pot fi evaluate pentru solutia asta noua
	        new_constraints = fixed_constraints(new_solution, constraints)

		continue_set = False

	        for constr_key in new_constraints:
            
		    if check_constraint(new_solution, (constr_key, new_constraints[constr_key])) == False:
			continue_set = True
			break

		if continue_set == True:
			continue

		new_cost2 = cost

		(sarcina, start_time, durata, timeout) = second_solution[var][-1]
		new_cost2 += max(0, start_time + durata - timeout)

		if new_cost2 < best_cost:
			result = PCSP(vars, deepcopy(domains), constraints, acceptable_cost, second_solution, new_cost2, vars_index + 1)
			if result == True:
				return True

def run_pcsp(acceptable_cost):
    global best_solution
    global best_cost
    global N

    vars = []
    domain = []
    constraints = {}

    with open('input_file') as f:
	    N, P = [int(x) for x in next(f).split(",")] # read first line
	
	    vars = [i for i in range(P)]

	    for line in f: # read rest of lines
		numbers = line.split(",")

		domain.append((int(numbers[0]), int(numbers[1]), int(numbers[2])))

		constraints[int(numbers[0])] = map(lambda x: int(x), numbers[3:])

    #print("Avem vars: ")
    #print(vars)

    #print("Avem domain: ")
    #print(domain)

    #print("Avem constraints: ")
    #print(constraints)

    best_solution = {}
    best_cost = len(constraints)

    PCSP(vars, deepcopy(domain), constraints, acceptable_cost, {}, 0, 1)
    
    print("Best found: " + str(best_cost) + " - " + str(best_solution))


    f = open('output_file', 'w')

    for key in best_solution.keys():
	print(key)
	f.write(str(key) + '\n')
	f.write(str(len(best_solution[key])) + '\n')

	for job in best_solution[key]:
		f.write(str(job[0]) + ',' + str(job[1]) + '\n')	
    
    f.close()

run_pcsp(0)
