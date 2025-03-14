import json
from pathlib import Path
import adopt_net0.data_preprocessing as dp
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary

sdfsdfsf
#Run Chemelot case study min costs
execute = 1

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster"
    resultpath = "Z:/PyHub/PyHub_results/CM/Complexity/Chemelot"
    json_filepath = Path(casepath) / "ConfigModel.json"

    co2tax = ['high']
    TD = [10, 20, 40, 60, 100, 200, 0]
    #
    # co2tax = ['high']
    # TD = [0]

    for tax in co2tax:
        for nr in TD:
            with open(json_filepath) as json_file:
                model_config = json.load(json_file)

            # change save options
            model_config['reporting']['save_summary_path']['value'] = resultpath + '_' + tax + 'CO2tax'
            model_config['reporting']['save_path']['value'] = resultpath + '_' + tax + 'CO2tax'

            model_config['optimization']['typicaldays']['N']['value'] = nr
            model_config['optimization']['objective']['value'] = 'costs'
            model_config['optimization']['emission_limit']['value'] = 0

            # Write the updated JSON data back to the file
            with open(json_filepath, 'w') as json_file:
                json.dump(model_config, json_file, indent=4)

            # Construct and solve the model
            pyhub = ModelHub()
            pyhub.read_data(casepath)

            if tax == 'high':
                if nr != 0:
                    pyhub.data.time_series['clustered']['period1', 'Chemelot', 'CarbonCost', 'global', 'price'] = 250
                pyhub.data.time_series['full']['period1', 'Chemelot', 'CarbonCost', 'global', 'price'] = 250

            #add casename based on resolution
            if pyhub.data.model_config['optimization']['typicaldays']['N']['value'] == 0:
                pyhub.data.model_config['reporting']['case_name']['value'] = 'fullres'
            else:
                pyhub.data.model_config['reporting']['case_name']['value'] = 'TD' + str(pyhub.data.model_config['optimization']['typicaldays']['N']['value'])

            #solving
            pyhub.quick_solve()


# Run Chemelot case study emissions
execute = 1

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster"
    resultpath = "Z:/PyHub/PyHub_results/CM/Complexity/Chemelot_minE"
    json_filepath = Path(casepath) / "ConfigModel.json"

    TD = [10, 20, 40, 60, 100, 200, 0]
    # TD = [30, 40, 60, 100, 200, 0]


    for nr in TD:
        with open(json_filepath) as json_file:
            model_config = json.load(json_file)

        model_config['optimization']['typicaldays']['N']['value'] = nr
        model_config['optimization']['objective']['value'] = 'emissions_minC'
        model_config['optimization']['emission_limit']['value'] = 0

        # change save options
        model_config['reporting']['save_summary_path']['value'] = resultpath
        model_config['reporting']['save_path']['value'] = resultpath

        # Write the updated JSON data back to the file
        with open(json_filepath, 'w') as json_file:
            json.dump(model_config, json_file, indent=4)

        # Construct and solve the model
        pyhub = ModelHub()
        pyhub.read_data(casepath)


        # add casename based on resolution
        if pyhub.data.model_config['optimization']['typicaldays']['N']['value'] == 0:
            pyhub.data.model_config['reporting']['case_name']['value'] = 'fullres'
        else:
            pyhub.data.model_config['reporting']['case_name']['value'] = 'TD' + str(
                pyhub.data.model_config['optimization']['typicaldays']['N']['value'])

        # solving
        pyhub.quick_solve()



#Run Chemelot case study relaxed
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster_relaxed"
    resultpath = "Z:/PyHub/PyHub_results/CM/RDS3_Chemelot_cluster_relaxed"
    json_filepath = Path(casepath) / "ConfigModel.json"

    obj = ['costs', 'emissions_minC']

    for nr in obj:
        with open(json_filepath) as json_file:
            model_config = json.load(json_file)

        model_config['optimization']['typicaldays']['N']['value'] = 0
        model_config['optimization']['objective']['value'] = nr
        model_config['optimization']['emission_limit']['value'] = 0

        #change save options
        model_config['reporting']['save_summary_path']['value'] = resultpath
        model_config['reporting']['save_path']['value'] = resultpath


        # Write the updated JSON data back to the file
        with open(json_filepath, 'w') as json_file:
            json.dump(model_config, json_file, indent=4)

        # Construct and solve the model
        pyhub = ModelHub()
        pyhub.read_data(casepath)

        #solving
        pyhub.quick_solve()


# Run Chemelot case study emission limit
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster"
    resultpath = "Z:/PyHub/PyHub_results/CM/RDS3_Chemelot_cluster_minE"
    json_filepath = Path(casepath) / "ConfigModel.json"


    TD = [10, 20, 40, 60, 100, 200, 0]



    maxemisions = 1304912.69
    elimit = [0.9, 0.8, 0.7, 0.68]

    for lim in elimit:
    # for nr in TD:
        with open(json_filepath) as json_file:
            model_config = json.load(json_file)

        # model_config['optimization']['typicaldays']['N']['value'] = nr
        # model_config['optimization']['objective']['value'] = 'emissions_minC'
        # model_config['optimization']['emission_limit']['value'] = 0

        model_config['optimization']['typicaldays']['N']['value'] = 10
        model_config['optimization']['objective']['value'] = 'costs_emissionlimit'
        model_config['optimization']['emission_limit']['value'] = lim * maxemisions


        # change save options
        model_config['reporting']['save_summary_path']['value'] = resultpath
        model_config['reporting']['save_path']['value'] = resultpath

        # Write the updated JSON data back to the file
        with open(json_filepath, 'w') as json_file:
            json.dump(model_config, json_file, indent=4)

        # Construct and solve the model
        pyhub = ModelHub()
        pyhub.read_data(casepath)

        pyhub.data.model_config['reporting']['case_name']['value'] = 'elimit' + str(int(round(lim*100)))
        pyhub.data.model_config['solveroptions']['mipfocus']['value'] = 1

        # # add casename based on resolution
        # if pyhub.data.model_config['optimization']['typicaldays']['N']['value'] == 0:
        #     pyhub.data.model_config['reporting']['case_name']['value'] = 'fullres'
        # else:
        #     pyhub.data.model_config['reporting']['case_name']['value'] = 'TD' + str(
        #         pyhub.data.model_config['optimization']['typicaldays']['N']['value'])

        # solving
        pyhub.quick_solve()

# Add values of (part of) the parameters and variables to the summary file
# summarypath = Path(resultpath) / "Summary.xlsx"
# add_values_to_summary(summarypath)


#Run Chemelot test case
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster"
    resultpath = "Z:/PyHub/PyHub_results/CM/test"
    json_filepath = Path(casepath) / "ConfigModel.json"

    # objectives = ['costs', 'emissions_minC']
    objectives = ['emissions_minC']

    for obj in objectives:
        with open(json_filepath) as json_file:
            model_config = json.load(json_file)

        model_config['optimization']['typicaldays']['N']['value'] = 20
        model_config['optimization']['objective']['value'] = obj
        model_config['optimization']['emission_limit']['value'] = 0

        #change save options
        model_config['reporting']['save_summary_path']['value'] = resultpath
        model_config['reporting']['save_path']['value'] = resultpath


        # Write the updated JSON data back to the file
        with open(json_filepath, 'w') as json_file:
            json.dump(model_config, json_file, indent=4)

        # Construct and solve the model
        pyhub = ModelHub()
        pyhub.read_data(casepath)

        # pyhub.data.model_config['solveroptions']['ScaleFlag']['value'] = 1

        if obj == 'emissions_minC':
            # add casename
            pyhub.data.model_config['reporting']['case_name']['value'] = 'minE_refCO2tax'

            # solving
            pyhub.quick_solve()

        elif obj == 'costs':
            co2tax = ['ref', 'high']

            for tax in co2tax:
                # add casename
                pyhub.data.model_config['reporting']['case_name']['value'] = 'minC_' + tax + 'CO2tax'

                if tax == 'high':
                    pyhub.data.time_series['clustered']['period1', 'Chemelot', 'CarbonCost', 'global', 'price'] = 250
                    pyhub.data.time_series['full']['period1', 'Chemelot', 'CarbonCost', 'global', 'price'] = 250

                # solving
                pyhub.quick_solve()