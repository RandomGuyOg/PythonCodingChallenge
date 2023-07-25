import pandas as pd
#getting raw data here

def get_pop_sets(sets_of_states, min_pop, state_population):
    print(sets_of_states)
    pop_sets = []
    max_population = 0
    for x in sets_of_states:
        set_population = 0
        for state in x:
            set_population = set_population + state_population.get(state,0)
        if set_population > min_pop*1e6:
            pop_sets.append(x)
    return pop_sets
def new_nation_with_pop(min_pop, usstates, border_data):
    us_states = pd.read_csv(usstates, header = None).rename(columns={0:"State",1:"State Code",2:"Area",3:"Population"})
    border_data = pd.read_csv(border_data)
    us_states = us_states.drop_duplicates(subset=['State Code'], keep='first')
    state_translater = dict(zip(us_states['State Code'], us_states['State']))
    state_population= dict(zip(us_states['State Code'], us_states['Population']))
    #Getting all borders of a state
    border_data_border = border_data[["ST1ST2"]]
    borders_defined = pd.DataFrame()
    borders_defined["State"] =""
    borders_defined["border state"] =""
    n= 0
    for index, row in border_data_border.iterrows():
        temp_container = row["ST1ST2"].split("-")
        if len(temp_container) ==2:
            borders_defined= pd.concat([borders_defined, pd.DataFrame({"State": [temp_container[0]], "border state" : [temp_container[1]]})])
            borders_defined = pd.concat(
                [borders_defined, pd.DataFrame({"State": [temp_container[1]], "border state": [temp_container[0]]})])
            n= n+2

    borders_defined = borders_defined[borders_defined["State"] != borders_defined["border state"]].reset_index(drop = True)
    borders_defined = borders_defined.drop_duplicates(subset=['State', 'border state'], keep='first')
    print(borders_defined)
    # new dic => state : {population, pd.DataFrame("State", "population") sorted decending order of population}
    required_state_object = {}
    for index, row in borders_defined.iterrows():
        if not row['State'] in required_state_object.keys():
            required_state_object[row['State']] = [state_population.get(row['State'],0),pd.DataFrame({"State":[row['border state'] ], "population": state_population.get(row['border state'],0),  })]
        else:
            #print("adding more data here: ", row['State'])
            required_state_object[row['State']] [1] = pd.concat([required_state_object[row['State']] [1],
                                                             pd.DataFrame({"State":[row['border state'] ], "population": [state_population.get(row['border state'],0)] })]).drop_duplicates().sort_values(by='population', ascending=False).reset_index(drop = True)
            #.drop_duplicates().sort_values(by='population', ascending=False)

    #n= 4
    #max_population = 0

    number_len = 1
    required_pop_sets = []
    while len(required_pop_sets) == 0 and number_len < len(required_state_object.keys()):
        set_states = []
        for state in  required_state_object.keys():
            print(state)
            prev_step = []
            new_step = [[state]]
            number = 0
            while number < number_len-1:
                prev_step = new_step.copy()
                new_step = []
                for x in prev_step:
                    print("previosu step is :, ", x)
                    states_neigbors =  required_state_object[x[-1]][1]["State"].to_list()
                    for neigbor in states_neigbors:
                        new_step.append( x+[neigbor])
                number= number+1
            new_step = [set(x) for x in new_step if len(set(x))==number_len]
            set_states = set_states + new_step
        set_states_distinct = []
        #set_states_distinct = [x for x in set_states if not x in set_states_distinct]
        for x in set_states:
            if not x in set_states_distinct:
                set_states_distinct.append(x)
        #print(len(set_states_distinct))
        required_pop_sets = get_pop_sets(set_states_distinct, min_pop, state_population)
        number_len = number_len+1
    return required_pop_sets


print(new_nation_with_pop(40, 'usstates.csv', 'border_data.csv'))



