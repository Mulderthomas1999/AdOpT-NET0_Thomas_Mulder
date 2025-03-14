import json
from pathlib import Path

import pandas as pd

import adopt_net0.data_preprocessing as dp
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary


#Run two cluster case
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Infra_2clusters"
    resultpath = "Z:/PyHub/PyHub_results/CM/Infrastructure/2clusters"
    json_filepath = Path(casepath) / "ConfigModel.json"

    objectives = ['costs', 'emissions_minC']
    # objectives = ['emissions_minC']

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

        if obj == 'emissions_minC':
            pyhub.data.model_config['solveroptions']['mipfocus']['value'] = 1

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
                    pyhub.data.time_series['clustered']['period1', 'Zeeland', 'CarbonCost', 'global', 'price'] = 250
                    pyhub.data.time_series['full']['period1', 'Zeeland', 'CarbonCost', 'global', 'price'] = 250

                # solving
                pyhub.quick_solve()


#Run Chemelot cluster case
execute = 1

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster"
    json_filepath = Path(casepath) / "ConfigModel.json"

    scenarios = ['CO2limHigh', 'CO2lim0', 'eleclim']

    for scen in scenarios:
        resultpath = "Z:/PyHub/PyHub_results/CM/Infrastructure/Chemelot_" + str(scen)

        # objectives = ['costs', 'emissions_minC']
        objectives = ['costs']

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

            if scen == 'CO2limHigh':
                pyhub.data.time_series['clustered']['period1', 'Chemelot', 'CarrierData', 'CO2', 'Export limit'] = 285
                pyhub.data.time_series['full']['period1', 'Chemelot', 'CarrierData', 'CO2', 'Export limit'] = 285
            elif scen == 'CO2lim0':
                pyhub.data.time_series['clustered']['period1', 'Chemelot', 'CarrierData', 'CO2', 'Export limit'] = 0
                pyhub.data.time_series['full']['period1', 'Chemelot', 'CarrierData', 'CO2', 'Export limit'] = 0
            elif scen == 'eleclim':
                pyhub.data.time_series['clustered']['period1', 'Chemelot', 'CarrierData', 'electricity', 'Import limit'] = 650
                pyhub.data.time_series['full']['period1', 'Chemelot', 'CarrierData', 'electricity', 'Import limit'] = 650

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

#Run Zeeland cluster case
execute = 0

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Zeeland_cluster"
    json_filepath = Path(casepath) / "ConfigModel.json"

    scenarios = ['CO2limHigh', 'CO2lim0', 'eleclim']

    for scen in scenarios:
        resultpath = "Z:/PyHub/PyHub_results/CM/Infrastructure/Zeeland_" + str(scen)

        # objectives = ['costs', 'emissions_minC']
        objectives = ['costs']

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

            if scen == 'CO2limHigh':
                pyhub.data.time_series['clustered']['period1', 'Zeeland', 'CarrierData', 'CO2', 'Export limit'] = 285
                pyhub.data.time_series['full']['period1', 'Zeeland', 'CarrierData', 'CO2', 'Export limit'] = 285
            elif scen == 'CO2lim0':
                pyhub.data.time_series['clustered']['period1', 'Zeeland', 'CarrierData', 'CO2', 'Export limit'] = 0
                pyhub.data.time_series['full']['period1', 'Zeeland', 'CarrierData', 'CO2', 'Export limit'] = 0
            elif scen == 'eleclim':
                pyhub.data.time_series['clustered']['period1', 'Zeeland', 'CarrierData', 'electricity', 'Import limit'] = 650
                pyhub.data.time_series['full']['period1', 'Zeeland', 'CarrierData', 'electricity', 'Import limit'] = 650

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
                        pyhub.data.time_series['clustered']['period1', 'Zeeland', 'CarbonCost', 'global', 'price'] = 250
                        pyhub.data.time_series['full']['period1', 'Zeeland', 'CarbonCost', 'global', 'price'] = 250

                    # solving
                    pyhub.quick_solve()
