import pandas as pd

def get_pop_sets(sets_of_states, min_pop, state_population):
    pop_sets = []
    for state_set in sets_of_states:
        set_population = sum(state_population.get(state, 0) for state in state_set)
        if set_population > min_pop*1e6:
            pop_sets.append(set(state_set))
    return pop_sets


def new_nation_with_pop(min_pop, usstates, border_data):
    us_states = pd.read_csv(usstates, header=None).rename(
        columns={0: "State", 1: "State Code", 2: "Area", 3: "Population"})
    us_states = us_states.drop_duplicates(subset=['State Code'], keep='first')
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
            new_step = [[state]]
            number = 0
            while number < number_len - 1:
                prev_step = new_step.copy()
                new_step = []
                for step in prev_step:
                    states_neighbours = borders_defined_dict[step[-1]]
                    for neighbour in states_neighbours:
                        new_step.append(step + [neighbour])
                number = number + 1
            new_step = [frozenset(x) for x in new_step if len(set(x)) == number_len]
            new_step = set(new_step)
            set_states = set_states.union(new_step)
        set_states_distinct = list(set_states)
        required_pop_sets = get_pop_sets(set_states_distinct, min_pop, state_population)
        number_len = number_len + 1
    return required_pop_sets

result = new_nation_with_pop(40, 'usstates.csv', 'border_data.csv')
print(result)
