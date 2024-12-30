import pandas as pd
data = pd.read_csv("FcRn competitive landscape.csv")
status_set = set(data.loc[:, "Status"])
status_mapper = {'Discontinued': 0, 'No Development Reported': 1, 'Outlicensed': 2, 'Discovery': 3,
                'Preclinical': 4, 'Phase 1 Clinical': 5, 'Phase 2 Clinical': 6, 'Phase 3 Clinical': 7,
                'Pre-registration': 8, 'Registered': 9, 'Launched': 10}

def status_to_number(stats, status_mapper):
    stats_num = []
    for i in stats:
        if i in status_mapper:
            stats_num.append(status_mapper[i])
        else:
            stats_num.append(-1)
    return stats_num

def number_to_status(stat_num, status_mapper):
    status = 'not defined'
    for k, v in status_mapper.items():
        if v == stat_num:
            status = k
    return status

def status_ranker(stats):
    highest_stat_num = max(status_to_number(stats, status_mapper))
    highest_stat = number_to_status(highest_stat_num, status_mapper)
    return highest_stat

def pivot_table_filter(filter_level, pivot_table):
    drugs = pivot_table.index
    indications = pivot_table.columns
    drug_drop_list = []
    indication_drop_list = []
    for drug in drugs:
        if max(status_to_number(pivot_table.loc[drug, :], status_mapper)) <= filter_level:
            drug_drop_list.append(drug)
    for indication in indications:
        if max(status_to_number(pivot_table.loc[:, indication], status_mapper)) <= filter_level:
            indication_drop_list.append(indication)
    filtered_drugs = list(set(drugs) - set(drug_drop_list))
    filtered_indications = list(set(indications) - set(indication_drop_list))
    filtered_pivot_table = pivot_table.loc[filtered_drugs, filtered_indications]
    return filtered_pivot_table

data_pivot_table = pd.pivot_table(data, values = "Status", index = "Drug", 
                                  columns = "Indication", aggfunc = status_ranker)
data_pivot_table.to_csv("drug_vs_indication.csv")

filtered_data_pivot_table = pivot_table_filter(4, data_pivot_table)
filtered_data_pivot_table.to_csv("drug_vs_indication_clinical.csv")