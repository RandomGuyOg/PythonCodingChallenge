import pandas as pd

def get_top_50_pct_states(sets_of_states, state_population):
    sets_of_states = list(sets_of_states)
    pop_sets_sum = [sum(state_population.get(state, 0) for state in state_set) for state_set in sets_of_states]
    temp_df = pd.DataFrame({"states_sets": sets_of_states,
                            "pop_sets_sum": pop_sets_sum})
    temp_df = temp_df.sort_values(by='pop_sets_sum', ascending=False)
    if len(temp_df) > 5:
        cutoff = int(len(temp_df)/2)
    else:
        cutoff = len(temp_df)
    pop_sets = set(temp_df["states_sets"].to_list()[:cutoff])
    return set(pop_sets)
def get_max_pop_set(sets_of_states, state_population):
    max_set = max(sets_of_states, key=lambda s: sum(state_population.get(state, 0) for state in s))
    max_population = sum(state_population.get(state, 0) for state in max_set)
    return max_set, max_population

def new_nation_n_states(number_len, usstates, border_data):
    us_states = pd.read_csv(usstates, header=None, names=["State", "State Code", "Area", "Population"])
    us_states = us_states.drop_duplicates(subset=['State Code'], keep='first').sort_values(by=['Population'], ascending=False)
    state_population = dict(zip(us_states['State Code'], us_states['Population']))

    border_data = pd.read_csv(border_data)
    borders_defined = border_data["ST1ST2"].str.split("-", expand=True)
    borders_defined = borders_defined.rename(columns={0: "State", 1: "border state"})
    borders_defined_rev = borders_defined.rename(columns={"State": "border state", "border state": "State"})
    borders_defined = pd.concat([borders_defined, borders_defined_rev]).reset_index(drop=True)
    borders_defined = borders_defined[borders_defined["State"] != borders_defined["border state"]].reset_index(drop=True)
    borders_defined = borders_defined.drop_duplicates(subset=['State', 'border state'], keep='first')

    borders_defined_dict = borders_defined.groupby('State')['border state'].apply(set).to_dict()

    set_states = set()
    for state in borders_defined_dict.keys():
        new_step = {frozenset([state])}
        number = 0
        while number < number_len - 1:
            prev_step = new_step.copy()
            new_step = set()
            for step in prev_step:
                states_neighbours = {neighbour for s in step for neighbour in borders_defined_dict.get(s, set())}
                for neighbour in states_neighbours:
                    new_step.add(frozenset(step | {neighbour}))
                new_step = get_top_50_pct_states(new_step, state_population)
            number += 1
        set_states |= new_step

    return get_max_pop_set(set_states, state_population)

#result = new_nation_n_states(9, 'usstates.csv', 'border_data.csv')
#print(result)