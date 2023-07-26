import pandas as pd
def get_max_pop_set(sets_of_states, state_population):
    max_set = []
    max_population = 0
    for state_set in sets_of_states:
        set_population = sum(state_population.get(state, 0) for state in state_set)
        if set_population > max_population:
            max_population = set_population
            max_set = state_set
    return (max_set, max_population)


def new_nation_n_states(number_len, usstates, border_data):
    us_states = pd.read_csv(usstates, header=None).rename(
        columns={0: "State", 1: "State Code", 2: "Area", 3: "Population"})
    us_states = us_states.drop_duplicates(subset=['State Code'], keep='first').sort_values(by=['Population'], ascending=False)
    #top_50_pct = us_states["State Code"][:int(len(us_states["State Code"])/2+1)].to_list()
    #top_50_pct = ["CO","IL","MO","AZ","TX","OK","CA"]
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

    set_states = set()
    for state in borders_defined_dict.keys():
        #for state in top_50_pct:
        new_step = [[state]]
        number = 0
        while number < number_len - 1:
            prev_step = new_step.copy()
            new_step = []
            for step in prev_step:
                if len(step)>1:
                    states_neighbours = set(borders_defined_dict[step[-2]]+borders_defined_dict[step[-1]])
                else:
                    states_neighbours = borders_defined_dict[step[-1]]
                for neighbour in states_neighbours:
                    new_step.append(step + [neighbour])
            number = number + 1
        new_step = [frozenset(x) for x in new_step if len(set(x)) == number_len]
        new_step = set(new_step)
        set_states = set_states.union(new_step)
    set_states_distinct = list(set_states)

    return get_max_pop_set(set_states_distinct, state_population)

result = new_nation_n_states(6, 'usstates.csv', 'border_data.csv')
print(result)
