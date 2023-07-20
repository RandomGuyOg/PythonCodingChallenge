import csv


def load_regions(filename):
    states_dict = dict()

    with open(filename, 'r') as f:
        for line in csv.reader(f):
            states_dict[line[1]] = int(line[3])

    return states_dict


def load_borders(filename):
    borders_list = list()

    with open(filename, 'r') as f:
        for line in csv.reader(f, 1):
            states = line[1].split('-')
            if len(states) == 2:
                borders_list.append((states[0], states[1]))

    return borders_list


# This function returns the state and population of the "most populous
# neighbor" bordering the candidate nation.
def most_populous_neighbor(states, borders, nation):
    neighbor = ''
    pop = 0

    for s in nation:
        for border in borders:
            if border[0] == s and border[1] in states:
                candidate = border[1]
                candidate_pop = states[border[1]]

                if candidate not in nation and candidate_pop > pop:
                    neighbor = candidate
                    pop = candidate_pop

            if border[1] == s and border[0] in states:
                candidate = border[0]
                candidate_pop = states[border[0]]

                if candidate not in nation and candidate_pop > pop:
                    neighbor = candidate
                    pop = candidate_pop

    return neighbor, pop


def new_nation_n_states(n, reg_filename, border_filename):
    new_nation = []
    max_pop = 0

    states = load_regions(reg_filename)
    borders = load_borders(border_filename)

    # Our naive implementation arbitrarily starts with the 'first' state
    # returned by load_states. One easy improvement would be to replace this
    # with the most populous state, but you can do far better than this!
    starting_state = list(states.keys())[0]
    new_nation = (starting_state,)
    max_pop = states[starting_state]

    # This is a "greedy" algorithm - we simply find the most populous
    # state bordering our candidate nation and append it to the list.
    while len(new_nation) < n:
        next_st, pop = most_populous_neighbor(states, borders, new_nation)
        new_nation += (next_st,)
        max_pop += pop

    return new_nation, max_pop
