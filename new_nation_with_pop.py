import pandas as pd



def get_pop_sets(sets_of_states, min_pop, state_population):
    pop_sets = [set(state_set) for state_set in sets_of_states if sum(state_population.get(state, 0) for state in state_set) > min_pop * 1e6]
    return pop_sets


def new_nation_with_pop(min_pop, usstates, border_data):
    us_states = pd.read_csv(usstates, header=None).rename(
        columns={0: "State", 1: "State Code", 2: "Area", 3: "Population"})
    us_states = us_states.drop_duplicates(subset=['State Code'], keep='first').sort_values(by=['Population'], ascending=False)
    #top_50_pct = us_states["State Code"][:int(len(us_states["State Code"])/2+1)].to_list()
    state_population = dict(zip(us_states['State Code'], us_states['Population']))

    border_data = pd.read_csv(border_data)
    borders_defined = border_data["ST1ST2"].str.split("-", expand=True)
    borders_defined = borders_defined.rename(columns={0: "State", 1: "border state"})
    borders_defined_rev = borders_defined.rename(columns={"State":"border state", "border state":"State"})
    borders_defined = pd.concat([borders_defined, borders_defined_rev]).reset_index(drop = True)
    borders_defined = borders_defined[borders_defined["State"] != borders_defined["border state"]].reset_index(
        drop=True)
    borders_defined = borders_defined.drop_duplicates(subset=['State', 'border state'], keep='first')

    borders_defined_dict = borders_defined.groupby('State')['border state'].apply(list).to_dict()

    number_len = 1
    required_pop_sets = []
    while len(required_pop_sets) == 0 and number_len < len(borders_defined_dict.keys()):
        set_states = set()
        for state in borders_defined_dict.keys():
            #for state in top_50_pct:
            new_step = {frozenset([state])}
            number = 0
            while number < number_len - 1:
                prev_step = new_step.copy()
                new_step = set()
                for step in prev_step:
                    if len(step) > 1:
                        states_neighbours = {neighbour for s in step for neighbour in
                                             borders_defined_dict.get(s, set())}
                    else:
                        states_neighbours = borders_defined_dict.get(next(iter(step)), set())
                    for neighbour in states_neighbours:
                        new_step.add(frozenset(step | {neighbour}))
                    #new_step = get_top_50_pct_states(new_step, state_population)
                number += 1
            set_states |= new_step
        #set_states_distinct = list(set_states)
        required_pop_sets = get_pop_sets(set_states, min_pop, state_population)
        number_len = number_len + 1
    return required_pop_sets

#result = new_nation_with_pop(85, 'usstates.csv', 'border_data.csv')
#print(result)