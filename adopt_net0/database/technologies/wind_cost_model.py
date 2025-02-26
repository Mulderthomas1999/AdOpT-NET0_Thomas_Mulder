from .utilities import Irena
from ..utilities import convert_currency
from ..data_component import DataComponent_CostModel


class WindEnergy_CostModel(DataComponent_CostModel):
    """
    Wind energy (onshore and offshore)

    Possible options are:

    If source = "IRENA"

    - cost model is based on IRENA (2023): Renewable power generation costs in 2023
    - region can be chosen among different countries ('Brazil', 'Canada', 'China', 'France', 'Germany', 'India', 'Japan', 'Spain', 'Sweden', 'United Kingdom', 'United States', 'Australia', 'Ireland')

    Financial indicators are:

    - unit_capex in [currency]/turbine
    - fixed capex as fraction of annualized capex
    - variable opex in [currency]/MWh
    - levelized cost in [currency]/MWh
    - lifetime in years
    """

    def __init__(self, tec_name):
        super().__init__(tec_name)
        # Default options:
        self.default_options["source"] = "IRENA"
        self.default_options["region"] = "Germany"

    def _set_options(self, options: dict):
        """
        Sets all provided options
        """
        super()._set_options(options)

        try:
            self.options["terrain"] = options["terrain"]
            self.options["nameplate_capacity_MW"] = options["nameplate_capacity_MW"]
        except KeyError:
            raise KeyError(
                "You need to at least specify the terrain (onshore or offshore) and the nameplate capacity"
            )

        # Set options
        self._set_option_value("source", options)

        if self.options["source"] == "IRENA":
            # Input units
            self.currency_in = "USD"
            self.financial_year_in = 2023

            # Options
            for o in self.default_options.keys():
                self._set_option_value(o, options)

        else:
            raise ValueError("This source is not available")

    def calculate_indicators(self, options: dict):
        """
        Calculates financial indicators
        """
        super().calculate_indicators(options)

        if self.options["source"] == "IRENA":
            if self.options["terrain"] == "Offshore":
                calculation_module = Irena("Wind_Offshore")
            elif self.options["terrain"] == "Onshore":
                calculation_module = Irena("Wind_Onshore")
            else:
                raise ValueError(
                    "Wrong terrain specified, needs to be Onshore or Offshore"
                )

            cost = calculation_module.calculate_cost(
                self.options["region"], self.discount_rate
            )

            self.financial_indicators["module_capex"] = convert_currency(
                cost["unit_capex"] * options["nameplate_capacity_MW"] * 1000,
                self.financial_year_in,
                self.financial_year_out,
                self.currency_in,
                self.currency_out,
            )
            self.financial_indicators["opex_variable"] = convert_currency(
                cost["opex_var"],
                self.financial_year_in,
                self.financial_year_out,
                self.currency_in,
                self.currency_out,
            )
            self.financial_indicators["opex_fix"] = cost["opex_fix"]
            self.financial_indicators["levelized_cost"] = (
                convert_currency(
                    cost["levelized_cost"],
                    self.financial_year_in,
                    self.financial_year_out,
                    self.currency_in,
                    self.currency_out,
                )
                * 1000
            )
            self.financial_indicators["lifetime"] = cost["lifetime"]

        # Write to json template
        self.json_data["Economics"]["unit_CAPEX"] = self.financial_indicators[
            "module_capex"
        ]
        self.json_data["Economics"]["OPEX_fixed"] = self.financial_indicators[
            "opex_fix"
        ]
        self.json_data["Economics"]["OPEX_variable"] = self.financial_indicators[
            "opex_variable"
        ]
        self.json_data["Economics"]["lifetime"] = self.financial_indicators["lifetime"]
        self.json_data["size_is_int"] = 1

        return {"financial_indicators": self.financial_indicators}
