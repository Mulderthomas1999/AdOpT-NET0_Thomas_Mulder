import json
from pathlib import Path

import pandas as pd

import adopt_net0.data_preprocessing as dp
from adopt_net0.modelhub import ModelHub
from adopt_net0.result_management.read_results import add_values_to_summary


#Run Chemelot cluster case
execute = 1

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Chemelot_cluster_CGtank"
    json_filepath = Path(casepath) / "ConfigModel.json"

    scenarios = ['slow', 'slowSMR', 'slowCracker']

    for scen in scenarios:
        resultpath = "Z:/PyHub/PyHub_results/CM/Flexibility/Chemelot_" + str(scen)

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

            if scen == 'slow':
                pyhub.data.technology_data['period1']['Chemelot']['eSMR'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Chemelot']['eSMR'].processed_coeff.dynamics['ramping_time'] = 5
                pyhub.data.technology_data['period1']['Chemelot']['NaphthaCracker_Electric'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Chemelot']['NaphthaCracker_Electric'].processed_coeff.dynamics[
                    'ramping_time'] = 5
            elif scen == 'slowSMR':
                pyhub.data.technology_data['period1']['Chemelot']['eSMR'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Chemelot']['eSMR'].processed_coeff.dynamics['ramping_time'] = 5
            elif scen == 'slowCracker':
                pyhub.data.technology_data['period1']['Chemelot'][
                    'NaphthaCracker_Electric'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Chemelot']['NaphthaCracker_Electric'].processed_coeff.dynamics[
                    'ramping_time'] = 5

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
execute = 1

if execute == 1:
    # Specify the path to your input data
    casepath = "Z:/PyHub/PyHub_casestudies/CM/Zeeland_cluster_CGtank"
    json_filepath = Path(casepath) / "ConfigModel.json"

    scenarios = ['Reference_tank', 'slow', 'slowSMR', 'slowCracker']

    for scen in scenarios:
        resultpath = "Z:/PyHub/PyHub_results/CM/Flexibility/Zeeland_" + str(scen)

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

            if scen == 'slow':
                pyhub.data.technology_data['period1']['Zeeland']['eSMR'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Zeeland']['eSMR'].processed_coeff.dynamics['ramping_time'] = 5
                pyhub.data.technology_data['period1']['Zeeland']['NaphthaCracker_Electric'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Zeeland']['NaphthaCracker_Electric'].processed_coeff.dynamics[
                    'ramping_time'] = 5
            elif scen == 'slowSMR':
                pyhub.data.technology_data['period1']['Zeeland']['eSMR'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Zeeland']['eSMR'].processed_coeff.dynamics['ramping_time'] = 5
            elif scen == 'slowCracker':
                pyhub.data.technology_data['period1']['Zeeland'][
                    'NaphthaCracker_Electric'].processed_coeff.time_independent[
                    'min_part_load'] = 0.8
                pyhub.data.technology_data['period1']['Zeeland']['NaphthaCracker_Electric'].processed_coeff.dynamics[
                    'ramping_time'] = 5

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