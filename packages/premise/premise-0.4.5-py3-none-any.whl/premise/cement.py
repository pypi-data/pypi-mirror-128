import copy
import uuid
from datetime import date

import numpy as np
import wurst
from wurst import searching as ws
from wurst import transformations as wt

from .activity_maps import InventorySet
from .geomap import Geomap
from .utils import *


class Cement:
    """
    Class that modifies clinker and cement production datasets in ecoinvent, mostly based on WBCSD's GNR data.
    :ivar scenario: name of a Remind pathway
    :vartype pathway: str

    """

    def __init__(self, db, model, scenario, iam_data, year, version):
        self.db = db
        self.model = model
        self.scenario = scenario
        self.iam_data = iam_data
        self.year = year
        self.version = version
        self.geo = Geomap(model=model)

        self.clinker_ratio_eco = get_clinker_ratio_ecoinvent(version)
        self.clinker_ratio_remind = get_clinker_ratio_remind(self.year)
        self.fuels_lhv = get_lower_heating_values()
        self.fuels_co2 = get_fuel_co2_emission_factors()
        mapping = InventorySet(self.db)
        self.emissions_map = mapping.get_remind_to_ecoinvent_emissions()
        self.fuel_map = mapping.generate_fuel_map()

    def fetch_proxies(self, name, ref_prod, relink=False):
        """
        Fetch dataset proxies, given a dataset `name` and `reference product`.
        Store a copy for each REMIND region.
        If a REMIND region does not find a fitting ecoinvent location,
        fetch a dataset with a "RoW" location.
        Delete original datasets from the database.

        :return:
        """

        d_map = {
            self.geo.ecoinvent_to_iam_location(d["location"]): d["location"]
            for d in ws.get_many(
                self.db,
                ws.equals("name", name),
                ws.equals("reference product", ref_prod),
            )
        }

        list_iam_regions = [
            c[1]
            for c in self.geo.geo.keys()
            if type(c) == tuple and c[0].lower() == self.model
        ]

        d_iam_to_eco = {r: d_map.get(r, "RoW") for r in list_iam_regions}

        d_act = {}

        for d in d_iam_to_eco:
            try:
                ds = ws.get_one(
                    self.db,
                    ws.equals("name", name),
                    ws.equals("reference product", ref_prod),
                    ws.equals("location", d_iam_to_eco[d]),
                )

                d_act[d] = wt.copy_to_new_location(ds, d)
                d_act[d]["code"] = str(uuid.uuid4().hex)

                for exc in ws.production(d_act[d]):
                    if "input" in exc:
                        exc.pop("input")

                if "input" in d_act[d]:
                    d_act[d].pop("input")

                if relink:
                    d_act[d] = relink_technosphere_exchanges(
                        d_act[d], self.db, self.model
                    )

            except ws.NoResults:
                print(
                    "No dataset {} found for the {} region {}".format(
                        name, self.model.upper(), d
                    )
                )
                continue

        deleted_markets = [
            (act["name"], act["reference product"], act["location"])
            for act in self.db
            if (act["name"], act["reference product"]) == (name, ref_prod)
        ]

        with open(
            DATA_DIR
            / "logs/log deleted cement datasets {} {} {}-{}.csv".format(
                self.model, self.scenario, self.year, date.today()
            ),
            "a",
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=";", lineterminator="\n")
            for line in deleted_markets:
                writer.writerow(line)

        # Remove old datasets
        self.db = [
            act
            for act in self.db
            if (act["name"], act["reference product"]) != (name, ref_prod)
        ]

        return d_act

    @staticmethod
    def remove_exchanges(exchanges_dict, list_exc):

        keep = lambda x: {
            k: v
            for k, v in x.items()
            if not any(ele in x.get("product", list()) for ele in list_exc)
        }

        for r in exchanges_dict:
            exchanges_dict[r]["exchanges"] = [
                keep(exc) for exc in exchanges_dict[r]["exchanges"]
            ]

        return exchanges_dict

    def get_suppliers_of_a_region(
        self,
        iam_region,
        ecoinvent_technologies,
        reference_product,
        unit="kilogram",
        look_for_locations_in="ecoinvent",
    ):
        """
        Return a list of datasets which location and name correspond to the region, name and reference product given,
        respectively.

        :param unit: unit of the dataset. If not specified, "kilogram" is used.
        :param look_for_locations_in: whether it should look for a supplier in ecoinvent locations or IAM locations.
        :param iam_region: an IAM region
        :type iam_region: str
        :param ecoinvent_technologies: list of names of ecoinvent dataset
        :type ecoinvent_technologies: list
        :param reference_product: reference product
        :type reference_product: str
        :return: list of wurst datasets
        :rtype: list
        """
        if look_for_locations_in == "ecoinvent":
            return ws.get_many(
                self.db,
                *[
                    ws.either(
                        *[
                            ws.contains("name", supplier)
                            for supplier in ecoinvent_technologies
                        ]
                    ),
                    ws.either(
                        *[
                            ws.equals("location", loc)
                            for loc in self.geo.iam_to_ecoinvent_location(iam_region)
                        ]
                    ),
                    ws.equals("unit", unit),
                    ws.equals("reference product", reference_product),
                ]
            )
        else:
            return ws.get_many(
                self.db,
                *[
                    ws.either(
                        *[
                            ws.contains("name", supplier)
                            for supplier in ecoinvent_technologies
                        ]
                    ),
                    ws.equals("location", look_for_locations_in),
                    ws.equals("unit", unit),
                    ws.equals("reference product", reference_product),
                ]
            )

    @staticmethod
    def get_shares_from_production_volume(ds):
        """
        Return shares of supply based on production volumes
        :param ds: list of datasets
        :return: dictionary with (dataset name, dataset location) as keys, shares as values. Shares total 1.
        :rtype: dict
        """
        dict_act = {}
        total_production_volume = 0
        for act in ds:
            for exc in ws.production(act):
                dict_act[
                    (
                        act["name"],
                        act["location"],
                        act["reference product"],
                        act["unit"],
                    )
                ] = float(exc["production volume"])
                total_production_volume += float(exc["production volume"])

        for d in dict_act:
            if total_production_volume != 0:
                dict_act[d] /= total_production_volume
            else:
                dict_act[d] = 1 / len(dict_act)

        return dict_act

    def update_pollutant_emissions(self, ds):
        """
        Update pollutant emissions based on GAINS data.
        We apply a correction factor defined as being equal to
        the emission level in the year in question, compared
        to 2020
        :return:
        """

        # Update biosphere exchanges according to GAINS emission values
        for exc in ws.biosphere(
            ds, ws.either(*[ws.contains("name", x) for x in self.emissions_map])
        ):
            remind_emission_label = self.emissions_map[exc["name"]]

            if (
                self.model == "remind"
                and ds["location"] in self.iam_data.cement_emissions.region
                or ds["location"] == "World"
            ):
                correction_factor = (
                    self.iam_data.cement_emissions.loc[
                        dict(
                            region=ds["location"]
                            if ds["location"] != "World"
                            else "CHA",
                            pollutant=remind_emission_label,
                        )
                    ].interp(year=self.year)
                    / self.iam_data.cement_emissions.loc[
                        dict(
                            region=ds["location"]
                            if ds["location"] != "World"
                            else "CHA",
                            pollutant=remind_emission_label,
                            year=2020,
                        )
                    ]
                ).values.item(0)

            elif (
                self.model == "image"
                and self.geo.iam_to_iam_region(ds["location"])
                in self.iam_data.cement_emissions.region
            ):
                correction_factor = (
                    self.iam_data.cement_emissions.loc[
                        dict(
                            region=self.geo.iam_to_iam_region(ds["location"]),
                            pollutant=remind_emission_label,
                        )
                    ].interp(year=self.year)
                    / self.iam_data.cement_emissions.loc[
                        dict(
                            region=self.geo.iam_to_iam_region(ds["location"]),
                            pollutant=remind_emission_label,
                            year=2020,
                        )
                    ]
                ).values.item(0)
            else:
                correction_factor = (
                    self.iam_data.cement_emissions.loc[
                        dict(
                            region=self.geo.ecoinvent_to_iam_location(ds["location"]),
                            pollutant=remind_emission_label,
                        )
                    ].interp(year=self.year)
                    / self.iam_data.cement_emissions.loc[
                        dict(
                            region=self.geo.ecoinvent_to_iam_location(ds["location"]),
                            pollutant=remind_emission_label,
                            year=2020,
                        )
                    ]
                ).values.item(0)

            if correction_factor != 0 and ~np.isnan(correction_factor):
                if exc["amount"] == 0:
                    wurst.rescale_exchange(
                        exc, correction_factor / 1, remove_uncertainty=True
                    )
                else:
                    wurst.rescale_exchange(exc, correction_factor)

                exc[
                    "comment"
                ] = "This exchange has been modified based on GAINS projections for the cement sector by `premise`."
        return ds

    def build_clinker_market_datasets(self):
        # Fetch clinker market activities and store them in a dictionary
        return self.fetch_proxies("market for clinker", "clinker", relink=True)

    def fuel_efficiency_factor(self, loc):
        """

        :param loc: location of the exchange
        :return: correction factor
        :rtype: float
        """

        if self.model == "remind":
            # REMIND
            final_energy = ["FE|Industry|Cement"]
            prod = "Production|Industry|Cement"
        else:
            # IMAGE
            final_energy = [
                "Final Energy|Industry|Cement|Electricity",
                "Final Energy|Industry|Cement|Gases",
                "Final Energy|Industry|Cement|Heat",
                "Final Energy|Industry|Cement|Hydrogen",
                "Final Energy|Industry|Cement|Liquids",
                "Final Energy|Industry|Cement|Solids",
            ]
            prod = "Production|Cement"

        # sometimes, the energy consumption values are not reported for the region "World"
        # in such case, we then look at the sum of all the regions
        if (
            self.iam_data.data.loc[dict(region=loc, variables=final_energy)]
            .interp(year=self.year)
            .sum()
            == 0
        ):
            loc = self.iam_data.data.region.values

        eff_factor = (
            (
                self.iam_data.data.loc[
                    dict(
                        region=[loc] if isinstance(loc, str) else loc,
                        variables=final_energy,
                    )
                ]
                .interp(year=self.year)
                .sum(dim=["region", "variables"])
                / self.iam_data.data.loc[
                    dict(
                        region=[loc] if isinstance(loc, str) else loc,
                        variables=prod,
                    )
                ]
                .interp(year=self.year)
                .sum(dim="region")
            )
            / (
                self.iam_data.data.loc[
                    dict(
                        region=[loc] if isinstance(loc, str) else loc,
                        variables=final_energy,
                        year=2020,
                    )
                ].sum(dim=["region", "variables"])
                / self.iam_data.data.loc[
                    dict(
                        region=[loc] if isinstance(loc, str) else loc,
                        variables=prod,
                        year=2020,
                    )
                ].sum(dim="region")
            )
        ).values

        # we assume efficiency cannot get worse over time
        if eff_factor == np.nan or eff_factor == np.inf or eff_factor > 1:
            eff_factor = 1

        return eff_factor

    def get_carbon_capture_rate(self, loc):
        """
        Returns the carbon capture rate as indicated by the IAM
        It is calculated as CO2 captured / (CO2 captured + CO2 emitted)

        :param loc: location of the dataset
        :return: rate of carbon capture
        :rtype: float
        """

        if self.model == "remind":
            if all(
                x in self.iam_data.data.variables.values
                for x in [
                    "Emi|CCO2|FFaI|Industry|Cement",
                    "Emi|CO2|FFaI|Industry|Cement",
                ]
            ):
                rate = (
                    self.iam_data.data.sel(
                        variables="Emi|CCO2|FFaI|Industry|Cement", region=loc
                    ).interp(year=self.year)
                    / self.iam_data.data.sel(
                        variables=[
                            "Emi|CCO2|FFaI|Industry|Cement",
                            "Emi|CO2|FFaI|Industry|Cement",
                        ],
                        region=loc,
                    )
                    .interp(year=self.year)
                    .sum(dim="variables")
                ).values
            else:
                rate = 0
        else:
            if all(
                x in self.iam_data.data.variables.values
                for x in [
                    "Emissions|CO2|Industry|Cement|Gross",
                    "Emissions|CO2|Industry|Cement|Sequestered",
                ]
            ):
                # let's check that we have values
                # sometimes, values are not reported for the "World " region

                rate = (
                    self.iam_data.data.sel(
                        variables="Emissions|CO2|Industry|Cement|Sequestered",
                        region=[loc]
                        if loc != "World"
                        else [l for l in self.iam_data.data.region.values],
                    )
                    .interp(year=self.year)
                    .sum(dim="region")
                    / self.iam_data.data.sel(
                        variables=[
                            "Emissions|CO2|Industry|Cement|Gross",
                            "Emissions|CO2|Industry|Cement|Sequestered",
                        ],
                        region=[loc]
                        if loc != "World"
                        else [l for l in self.iam_data.data.region.values],
                    )
                    .interp(year=self.year)
                    .sum(dim=["variables", "region"])
                ).values
            else:
                rate = 0

        return rate

    def build_clinker_production_datasets(self):
        """
        Builds clinker production datasets for each IAM region.
        If `industry_module_present`, the kiln efficiency improvement follows projections from the IAM model
        # If not, it follows projections from the IEA
        Add CO2 capture and Storage if needed.
        Source for CO2 capture and compression: https://www.sciencedirect.com/science/article/pii/S1750583613001230?via%3Dihub#fn0040
        :return: a dictionary with IAM regions as keys and clinker production datasets as values.
        :rtype: dict
        """

        # Fetch clinker production activities and store them in a dictionary
        d_act_clinker = self.fetch_proxies("clinker production", "clinker", relink=True)

        # Fuel exchanges to remove
        list_fuels = [
            "diesel",
            "coal",
            "lignite",
            "coke",
            "fuel",
            "meat",
            "gas",
            "oil",
            "electricity",
            "wood",
            "waste",
        ]

        # we first create current clinker production activities for each region
        # from GNR data, to get a new fuel efficiency and mix than what is
        # currently in ecoinvent

        # Remove fuel and electricity exchanges in each activity
        d_act_clinker = self.remove_exchanges(d_act_clinker, list_fuels)

        for k, v in d_act_clinker.items():

            # Production volume by kiln type
            energy_input_per_kiln_type = self.iam_data.gnr_data.sel(
                region=self.geo.iam_to_iam_region(k) if self.model == "image" else k,
                variables=[
                    v
                    for v in self.iam_data.gnr_data.variables.values
                    if "Production volume share" in v
                ],
            ).clip(0, 1)
            # Energy input per ton of clinker, in MJ, per kiln type
            energy_input_per_kiln_type /= energy_input_per_kiln_type.sum(axis=0)

            energy_eff_per_kiln_type = self.iam_data.gnr_data.sel(
                region=self.geo.iam_to_iam_region(k) if self.model == "image" else k,
                variables=[
                    v
                    for v in self.iam_data.gnr_data.variables.values
                    if "Thermal energy consumption" in v
                ],
            )

            # Weighted average energy input per ton clinker, in MJ
            energy_input_per_ton_clinker = (
                energy_input_per_kiln_type.values * energy_eff_per_kiln_type.values
            )

            # the correction factor applied to all fuel/electricity input is
            # equal to the ratio fuel/output in the year in question
            # divided by the ratio fuel/output in 2020

            correction_factor = self.fuel_efficiency_factor(v["location"])
            energy_input_per_ton_clinker *= correction_factor

            # Fuel mix (waste, biomass, fossil)
            fuel_mix = self.iam_data.gnr_data.sel(
                variables=[
                    "Share waste fuel",
                    "Share biomass fuel",
                    "Share fossil fuel",
                ],
                region=self.geo.iam_to_iam_region(k) if self.model == "image" else k,
            ).clip(0, 1)

            fuel_mix /= fuel_mix.sum(axis=0)

            # Calculate quantities (in kg) of fuel, per type of fuel, per ton of clinker
            # MJ per ton of clinker * fuel mix * (1 / lower heating value)
            fuel_qty_per_type = (
                energy_input_per_ton_clinker.sum()
                * fuel_mix
                * 1
                / np.array(
                    [
                        float(self.fuels_lhv["waste"]),
                        float(self.fuels_lhv["wood pellet"]),
                        float(self.fuels_lhv["hard coal"]),
                    ]
                )
            )

            fuel_fossil_co2_per_type = (
                energy_input_per_ton_clinker.sum()
                * fuel_mix
                * np.array(
                    [
                        (
                            self.fuels_co2["waste"]["co2"]
                            * (1 - self.fuels_co2["waste"]["bio_share"])
                        ),
                        (
                            self.fuels_co2["wood pellet"]["co2"]
                            * (1 - self.fuels_co2["wood pellet"]["bio_share"])
                        ),
                        (
                            self.fuels_co2["hard coal"]["co2"]
                            * (1 - self.fuels_co2["hard coal"]["bio_share"])
                        ),
                    ]
                )
            )

            fuel_biogenic_co2_per_type = (
                energy_input_per_ton_clinker.sum()
                * fuel_mix
                * np.array(
                    [
                        (
                            self.fuels_co2["waste"]["co2"]
                            * (self.fuels_co2["waste"]["bio_share"])
                        ),
                        (
                            self.fuels_co2["wood pellet"]["co2"]
                            * (self.fuels_co2["wood pellet"]["bio_share"])
                        ),
                        (
                            self.fuels_co2["hard coal"]["co2"]
                            * (self.fuels_co2["hard coal"]["bio_share"])
                        ),
                    ]
                )
            )

            # Append it to the dataset exchanges
            new_exchanges = []

            for f, fuel in enumerate(
                [
                    ("waste", "waste plastic, mixture"),
                    ("wood pellet", "wood pellet, measured as dry mass"),
                    ("hard coal", "hard coal"),
                ]
            ):
                # Select waste fuel providers, fitting the IAM region
                # Fetch respective shares based on production volumes
                fuel_suppliers = self.get_shares_from_production_volume(
                    self.get_suppliers_of_a_region(k, self.fuel_map[fuel[0]], fuel[1])
                )
                if len(fuel_suppliers) == 0:
                    fuel_suppliers = self.get_shares_from_production_volume(
                        self.get_suppliers_of_a_region(
                            k,
                            self.fuel_map[fuel[0]],
                            fuel[1],
                            look_for_locations_in="ecoinvent",
                        )
                    )

                if len(fuel_suppliers) == 0:
                    loc = "World"
                    fuel_suppliers = self.get_shares_from_production_volume(
                        self.get_suppliers_of_a_region(
                            loc,
                            self.fuel_map[fuel[0]],
                            fuel[1],
                            look_for_locations_in="ecoinvent",
                        )
                    )

                for s, supplier in enumerate(fuel_suppliers):
                    new_exchanges.append(
                        {
                            "uncertainty type": 0,
                            "loc": 1,
                            "amount": (
                                fuel_suppliers[supplier] * fuel_qty_per_type[f].values
                            )
                            / 1000,
                            "type": "technosphere",
                            "production volume": 0,
                            "product": supplier[2],
                            "name": supplier[0],
                            "unit": supplier[3],
                            "location": supplier[1],
                        }
                    )

            v["exchanges"].extend(new_exchanges)

            v["exchanges"] = [v for v in v["exchanges"] if v]

            # Carbon capture rate: share of capture of total CO2 emitted
            carbon_capture_rate = self.get_carbon_capture_rate(v["location"])

            # Update fossil CO2 exchange, add 525 kg of fossil CO_2 from calcination
            try:
                fossil_co2_exc = [
                    e for e in v["exchanges"] if e["name"] == "Carbon dioxide, fossil"
                ][0]
                fossil_co2_exc["amount"] = (
                    (fuel_fossil_co2_per_type.sum().values + 525) / 1000
                ) * (1 - carbon_capture_rate)
                fossil_co2_exc["uncertainty type"] = 0

            except IndexError:
                # the fossil CO2 flow does not exist
                amount = ((fuel_fossil_co2_per_type.sum().values + 525) / 1000) * (
                    1 - carbon_capture_rate
                )
                fossil_co2_exc = {
                    "uncertainty type": 0,
                    "loc": amount,
                    "amount": amount,
                    "type": "biosphere",
                    "name": "Carbon dioxide, fossil",
                    "unit": "kilogram",
                    "categories": ("air",),
                }
                v["exchanges"].append(fossil_co2_exc)

            try:
                # Update biogenic CO2 exchange
                biogenic_co2_exc = [
                    e
                    for e in v["exchanges"]
                    if e["name"] == "Carbon dioxide, non-fossil"
                ][0]
                biogenic_co2_exc["amount"] = (
                    fuel_biogenic_co2_per_type.sum().values / 1000
                ) * (1 - carbon_capture_rate)
                biogenic_co2_exc["uncertainty type"] = 0

            except IndexError:
                # There isn't a biogenic CO2 emissions exchange
                amount = (fuel_biogenic_co2_per_type.sum().values / 1000) * (
                    1 - carbon_capture_rate
                )
                biogenic_co2_exc = {
                    "uncertainty type": 0,
                    "loc": amount,
                    "amount": amount,
                    "type": "biosphere",
                    "name": "Carbon dioxide, non-fossil",
                    "unit": "kilogram",
                    "input": ("biosphere3", "eba59fd6-f37e-41dc-9ca3-c7ea22d602c7"),
                    "categories": ("air",),
                }
                v["exchanges"].append(biogenic_co2_exc)

            # add CCS-related dataset
            if carbon_capture_rate > 0:

                ds = ws.get_one(
                    self.db,
                    ws.equals(
                        "name",
                        "CO2 capture, at cement production plant, with underground storage, post, 200 km",
                    ),
                    ws.equals("location", "RER"),
                )

                ccs = wt.copy_to_new_location(ds, v["location"])
                ccs["code"] = str(uuid.uuid4().hex)
                ccs = relink_technosphere_exchanges(ccs, self.db, self.model)

                if "input" in ccs:
                    ccs.pop("input")

                # we first fix the biogenic CO2 permanent storage
                # share = sum of biogenic fuel emissions / (sum of fossil fuel emission
                # + sum of biogenic fuel emissions + 525 kg from calcination)
                for exc in ws.biosphere(
                    ccs,
                    ws.equals("name", "Carbon dioxide, to soil or biomass stock"),
                ):
                    exc["amount"] = (
                        fuel_biogenic_co2_per_type.sum()
                        / (
                            fuel_fossil_co2_per_type.sum()
                            + fuel_biogenic_co2_per_type.sum()
                            + 525
                        )
                    ).values.item(0)

                # 0.11 kg CO2 leaks per kg captured
                # we need to align the CO2 composition with
                # the CO2 composition of the cement plant
                for exc in ws.biosphere(
                    ccs,
                    ws.equals("name", "Carbon dioxide, from soil or biomass stock"),
                ):
                    exc["amount"] = (
                        fuel_biogenic_co2_per_type.sum()
                        / (
                            fuel_fossil_co2_per_type.sum()
                            + fuel_biogenic_co2_per_type.sum()
                            + 525
                        )
                    ).values.item(0) * 0.11

                for exc in ws.biosphere(
                    ccs, ws.equals("name", "Carbon dioxide, fossil")
                ):
                    exc["amount"] = 0.11 - (
                        (
                            fuel_biogenic_co2_per_type.sum()
                            / (
                                fuel_fossil_co2_per_type.sum()
                                + fuel_biogenic_co2_per_type.sum()
                                + 525
                            )
                        )
                        * 0.11
                    ).values.item(0)

                # we adjust the heat needs by subtraction 3.66 MJ with what
                # the cement plant is expected to produce as excess heat

                # Heat, as steam: 3.66 MJ/kg CO2 captured, minus excess heat generated on site
                excess_heat_generation = (
                    self.iam_data.gnr_data.sel(
                        variables="Share of recovered energy, per ton clinker",
                        region=self.geo.iam_to_iam_region(v["location"])
                        if self.model == "image"
                        else v["location"],
                    ).values
                    * (energy_input_per_ton_clinker.sum() / 1000)
                )

                for exc in ws.technosphere(
                    ccs, ws.contains("name", "steam production")
                ):
                    exc["amount"] = np.clip(3.66 - excess_heat_generation, 0, 3.66)

                # then, we need to find local suppliers of electricity, water, steam, etc.
                relink_technosphere_exchanges(ccs, self.db, self.model)

                # we add this new dataset to the database
                self.db.append(ccs)

                # add an input from this CCS dataset in the clinker dataset
                ccs_exc = {
                    "uncertainty type": 0,
                    "loc": 0,
                    "amount": (
                        (
                            fuel_fossil_co2_per_type.sum().values
                            + fuel_biogenic_co2_per_type.sum().values
                        )
                        / 1000
                    )
                    * carbon_capture_rate,
                    "type": "technosphere",
                    "production volume": 0,
                    "name": "CO2 capture, at cement production plant, with underground storage, post, 200 km",
                    "unit": "kilogram",
                    "location": v["location"],
                    "product": "CO2, captured and stored",
                }
                v["exchanges"].append(ccs_exc)

            v["exchanges"] = [v for v in v["exchanges"] if v]

            v["comment"] = (
                "WARNING: Dataset modified by `premise` based on WBCSD's GNR data and IAM projections "
                + " for the cement industry.\n"
                + "Calculated energy input per kg clinker: {} MJ/kg clinker.\n".format(
                    np.round(energy_input_per_ton_clinker.sum(), 1) / 1000
                )
                + "Improvement of energy input per kg clinker compared to 2020: {} %.\n".format(
                    (correction_factor - 1) * 100
                )
                + "Share of biomass fuel energy-wise: {} pct.\n".format(
                    int(fuel_mix[1] * 100)
                )
                + "Share of waste fuel energy-wise: {} pct.\n".format(
                    int(fuel_mix[0] * 100)
                )
                + "Share of fossil carbon in waste fuel energy-wise: {} pct.\n".format(
                    int(self.fuels_co2["waste"]["bio_share"] * 100)
                )
                + "Share of fossil CO2 emissions from fuel combustion: {} pct.\n".format(
                    int(
                        (
                            fuel_fossil_co2_per_type.sum()
                            / (fuel_fossil_co2_per_type.sum() + 525)
                        )
                        * 100
                    )
                )
                + "Share of fossil CO2 emissions from calcination: {} pct.\n".format(
                    100
                    - int(
                        (
                            fuel_fossil_co2_per_type.sum()
                            / np.sum(fuel_fossil_co2_per_type.sum() + 525)
                        )
                        * 100
                    )
                )
                + "Rate of carbon capture: {} pct.\n".format(
                    int(carbon_capture_rate * 100)
                )
            ) + v["comment"]

        # TODO: currently, uses the relative improvement as given by GAINS in reference to 2020
        print(
            "Adjusting emissions of hot pollutants for clinker production datasets..."
        )
        d_act_clinker = {
            k: self.update_pollutant_emissions(v) for k, v in d_act_clinker.items()
        }

        return d_act_clinker

    def relink_datasets(self, name, ref_product):
        """
        For a given dataset name, change its location to an IAM location,
        to effectively link the newly built dataset(s).

        :param ref_product:
        :param name: dataset name
        :type name: str
        """

        list_ds = [
            (ds["name"], ds["reference product"], ds["location"]) for ds in self.db
        ]

        for act in self.db:
            excs = [
                exc
                for exc in act["exchanges"]
                if (exc["name"], exc.get("product")) == (name, ref_product)
                and exc["type"] == "technosphere"
            ]

            amount = 0
            for exc in excs:
                amount += exc["amount"]
                act["exchanges"].remove(exc)

            if amount > 0:
                new_exc = {
                    "name": name,
                    "product": ref_product,
                    "amount": amount,
                    "type": "technosphere",
                    "unit": "kilogram",
                }

                if (name, ref_product, act["location"]) in list_ds:
                    new_exc["location"] = act["location"]
                else:
                    try:
                        new_loc = self.geo.ecoinvent_to_iam_location(act["location"])
                    except KeyError:
                        new_loc = ""

                    if (name, ref_product, new_loc) in list_ds:
                        new_exc["location"] = new_loc
                    else:
                        # new locations in ei3.7, not yet defined in `constructive_geometries`
                        if act["location"] in (
                            "North America without Quebec",
                            "US only",
                        ):
                            new_loc = self.geo.ecoinvent_to_iam_location("US")
                            new_exc["location"] = new_loc

                        elif act["location"] in ("RoW", "GLO"):
                            new_loc = self.geo.ecoinvent_to_iam_location("CN")
                            new_exc["location"] = new_loc

                        elif act["location"] in (
                            "RER w/o RU",
                            "WECC",
                            "UCTE without Germany",
                        ):
                            new_loc = self.geo.ecoinvent_to_iam_location("RER")
                            new_exc["location"] = new_loc

                        else:
                            print(
                                "Issue with {} used in {}: cannot find the IAM equivalent for "
                                "the location {}".format(
                                    name, act["name"], act["location"]
                                )
                            )

                act["exchanges"].append(new_exc)

    def adjust_clinker_ratio(self, d_act):
        """Adjust the cement suppliers composition for "cement, unspecified", in order to reach
        the average clinker-to-cement ratio given by the IAM.

        The supply of the cement with the highest clinker-to-cement ratio is decreased by 1% to the favor of
        the supply of the cement with the lowest clinker-to-cement ratio, and the average clinker-to-cement ratio
        is calculated.

        This operation is repeated until the average clinker-to-cement ratio aligns with that given by the IAM.
        When the supply of the cement with the highest clinker-to-cement ratio goes below 1%,
        the cement with the second highest clinker-to-cement ratio becomes affected and so forth.

        """

        for d in d_act:

            ratio_to_reach = self.clinker_ratio_remind.sel(
                dict(
                    region=self.geo.iam_to_iam_region(d) if self.model == "image" else d
                )
            ).values

            share = []
            ratio = []

            for exc in d_act[d]["exchanges"]:
                if "cement" in exc["product"] and exc["type"] == "technosphere":
                    share.append(exc["amount"])
                    ratio.append(self.clinker_ratio_eco[(exc["name"], exc["location"])])

            share = np.array(share)
            ratio = np.array(ratio)

            average_ratio = (share * ratio).sum()

            iteration = 0
            while average_ratio > ratio_to_reach and iteration < 100:
                share[share == 0] = np.nan

                ratio = np.where(share >= 0.001, ratio, np.nan)

                highest_ratio = np.nanargmax(ratio)
                lowest_ratio = np.nanargmin(ratio)

                share[highest_ratio] -= 0.01
                share[lowest_ratio] += 0.01

                average_ratio = (np.nan_to_num(ratio) * np.nan_to_num(share)).sum()
                iteration += 1

            share = np.nan_to_num(share)

            count = 0
            for exc in d_act[d]["exchanges"]:
                if "cement" in exc["product"] and exc["type"] == "technosphere":
                    exc["amount"] = share[count]
                    count += 1

        return d_act

    def update_cement_production_datasets(self, name, ref_prod):
        """
        Update electricity use (mainly for grinding).

        :return:
        """
        # Fetch proxies
        # Delete old datasets
        d_act_cement = self.fetch_proxies(name, ref_prod)
        # Update electricity use
        d_act_cement = self.update_electricity_exchanges(d_act_cement)

        return d_act_cement

    def update_electricity_exchanges(self, d_act):
        """
        Update electricity exchanges in cement production datasets.
        Electricity consumption equals electricity use minus on-site electricity generation from excess heat recovery.

        :return:
        """
        d_act = self.remove_exchanges(d_act, ["electricity"])

        for act in d_act:

            new_exchanges = []
            electricity_needed = (
                self.iam_data.gnr_data.loc[
                    dict(
                        variables="Power consumption",
                        region=self.geo.iam_to_iam_region(act)
                        if self.model == "image"
                        else act,
                    )
                ].values
                / 1000
            )
            electricity_recovered = (
                self.iam_data.gnr_data.loc[
                    dict(
                        variables="Power generation",
                        region=self.geo.iam_to_iam_region(act)
                        if self.model == "image"
                        else act,
                    )
                ].values
                / 1000
            )

            electricity_suppliers = self.get_shares_from_production_volume(
                self.get_suppliers_of_a_region(
                    iam_region=act,
                    ecoinvent_technologies=["electricity, medium voltage"],
                    reference_product="electricity, medium voltage",
                    unit="kilowatt hour",
                    look_for_locations_in=act,
                )
            )

            if len(electricity_suppliers) == 0:
                electricity_suppliers = self.get_shares_from_production_volume(
                    self.get_suppliers_of_a_region(
                        iam_region=act,
                        ecoinvent_technologies=["electricity, medium voltage"],
                        reference_product="electricity, medium voltage",
                        unit="kilowatt hour",
                        look_for_locations_in="ecoinvent",
                    )
                )

            for s, supplier in enumerate(electricity_suppliers):
                share = electricity_suppliers[supplier]
                new_exchanges.append(
                    {
                        "uncertainty type": 0,
                        "loc": 1,
                        "amount": (electricity_needed - electricity_recovered) * share,
                        "type": "technosphere",
                        "production volume": 0,
                        "product": supplier[2],
                        "name": supplier[0],
                        "unit": supplier[3],
                        "location": supplier[1],
                    }
                )

            d_act[act]["exchanges"].extend(new_exchanges)
            d_act[act]["exchanges"] = [v for v in d_act[act]["exchanges"] if v]

            d_act[act]["comment"] = (
                "WARNING: Dataset modified by `premise` based on WBCSD's GNR data and 2018 IEA roadmap for the cement industry.\n "
                + "Electricity consumption per kg cement: {} kWh.\n".format(
                    electricity_needed
                )
                + "Of which {} kWh were generated from on-site waste heat recovery.\n".format(
                    electricity_recovered
                )
            ) + d_act[act]["comment"]

        return d_act

    def add_datasets_to_database(self):

        print("\nStart integration of cement data...\n")

        print(
            "The validity of the datasets produced from the integration of the cement sector is not yet fully tested.\n"
            "Consider the results with caution.\n"
        )

        print("Log of deleted cement datasets saved in {}".format(DATA_DIR / "logs"))
        print("Log of created cement datasets saved in {}".format(DATA_DIR / "logs"))

        if not os.path.exists(DATA_DIR / "logs"):
            os.makedirs(DATA_DIR / "logs")

        with open(
            DATA_DIR
            / "logs/log deleted cement datasets {} {} {}-{}.csv".format(
                self.model, self.scenario, self.year, date.today()
            ),
            "w",
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=";", lineterminator="\n")
            writer.writerow(["dataset name", "reference product", "location"])

        with open(
            DATA_DIR
            / "logs/log created cement datasets {} {} {}-{}.csv".format(
                self.model, self.scenario, self.year, date.today()
            ),
            "w",
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=";", lineterminator="\n")
            writer.writerow(["dataset name", "reference product", "location"])

        created_datasets = list()

        print("\nCreate new clinker production datasets and delete old datasets")
        clinker_prod_datasets = [
            d for d in self.build_clinker_production_datasets().values()
        ]
        self.db.extend(clinker_prod_datasets)

        created_datasets.extend(
            [
                (act["name"], act["reference product"], act["location"])
                for act in clinker_prod_datasets
            ]
        )

        print("\nCreate new clinker market datasets and delete old datasets")
        clinker_market_datasets = [
            d for d in self.build_clinker_market_datasets().values()
        ]
        self.db.extend(clinker_market_datasets)

        created_datasets.extend(
            [
                (act["name"], act["reference product"], act["location"])
                for act in clinker_market_datasets
            ]
        )

        print('Adjust clinker-to-cement ratio in "unspecified cement" datasets')

        if self.version == 3.5:
            name = "market for cement, unspecified"
            ref_prod = "cement, unspecified"

        else:
            name = "cement, all types to generic market for cement, unspecified"
            ref_prod = "cement, unspecified"

        act_cement_unspecified = self.fetch_proxies(name, ref_prod)

        act_cement_unspecified = self.adjust_clinker_ratio(act_cement_unspecified)
        self.db.extend([v for v in act_cement_unspecified.values()])

        created_datasets.extend(
            [
                (act["name"], act["reference product"], act["location"])
                for act in act_cement_unspecified.values()
            ]
        )

        print(
            "\nCreate new cement production datasets and adjust electricity consumption"
        )

        if self.version == 3.5:

            for i in (
                (
                    "market for cement, alternative constituents 21-35%",
                    "cement, alternative constituents 21-35%",
                ),
                (
                    "market for cement, alternative constituents 6-20%",
                    "cement, alternative constituents 6-20%",
                ),
                (
                    "market for cement, blast furnace slag 18-30% and 18-30% other alternative constituents",
                    "cement, blast furnace slag 18-30% and 18-30% other alternative constituents",
                ),
                (
                    "market for cement, blast furnace slag 25-70%, US only",
                    "cement, blast furnace slag 25-70%, US only",
                ),
                (
                    "market for cement, blast furnace slag 31-50% and 31-50% other alternative constituents",
                    "cement, blast furnace slag 31-50% and 31-50% other alternative constituents",
                ),
                (
                    "market for cement, blast furnace slag 36-65%, non-US",
                    "cement, blast furnace slag 36-65%, non-US",
                ),
                (
                    "market for cement, blast furnace slag 5-25%, US only",
                    "cement, blast furnace slag 5-25%, US only",
                ),
                (
                    "market for cement, blast furnace slag 70-100%, non-US",
                    "cement, blast furnace slag 70-100%, non-US",
                ),
                (
                    "market for cement, blast furnace slag 70-100%, US only",
                    "cement, blast furnace slag 70-100%, US only",
                ),
                (
                    "market for cement, blast furnace slag 81-95%, non-US",
                    "cement, blast furnace slag 81-95%, non-US",
                ),
                (
                    "market for cement, blast furnace slag, 66-80%, non-US",
                    "cement, blast furnace slag, 66-80%, non-US",
                ),
                ("market for cement, Portland", "cement, Portland"),
                (
                    "market for cement, pozzolana and fly ash 11-35%, non-US",
                    "cement, pozzolana and fly ash 11-35%, non-US",
                ),
                (
                    "market for cement, pozzolana and fly ash 15-40%, US only",
                    "cement, pozzolana and fly ash 15-40%, US only",
                ),
                (
                    "market for cement, pozzolana and fly ash 36-55%,non-US",
                    "cement, pozzolana and fly ash 36-55%,non-US",
                ),
                (
                    "market for cement, pozzolana and fly ash 5-15%, US only",
                    "cement, pozzolana and fly ash 5-15%, US only",
                ),
            ):
                act_cement = self.fetch_proxies(i[0], i[1])
                self.db.extend([v for v in act_cement.values()])
                created_datasets.extend(
                    [
                        (act["name"], act["reference product"], act["location"])
                        for act in act_cement.values()
                    ]
                )

                self.relink_datasets(i[0], i[1])

            for i in (
                (
                    "cement production, alternative constituents 21-35%",
                    "cement, alternative constituents 21-35%",
                ),
                (
                    "cement production, alternative constituents 6-20%",
                    "cement, alternative constituents 6-20%",
                ),
                (
                    "cement production, blast furnace slag 18-30% and 18-30% other alternative constituents",
                    "cement, blast furnace slag 18-30% and 18-30% other alternative constituents",
                ),
                (
                    "cement production, blast furnace slag 25-70%, US only",
                    "cement, blast furnace slag 25-70%, US only",
                ),
                (
                    "cement production, blast furnace slag 31-50% and 31-50% other alternative constituents",
                    "cement, blast furnace slag 31-50% and 31-50% other alternative constituents",
                ),
                (
                    "cement production, blast furnace slag 36-65%, non-US",
                    "cement, blast furnace slag 36-65%, non-US",
                ),
                (
                    "cement production, blast furnace slag 5-25%, US only",
                    "cement, blast furnace slag 5-25%, US only",
                ),
                (
                    "cement production, blast furnace slag 70-100%, non-US",
                    "cement, blast furnace slag 70-100%, non-US",
                ),
                (
                    "cement production, blast furnace slag 70-100%, US only",
                    "cement, blast furnace slag 70-100%, US only",
                ),
                (
                    "cement production, blast furnace slag 81-95%, non-US",
                    "cement, blast furnace slag 81-95%, non-US",
                ),
                (
                    "cement production, blast furnace slag, 66-80%, non-US",
                    "cement, blast furnace slag, 66-80%, non-US",
                ),
                ("cement production, Portland", "cement, Portland"),
                (
                    "cement production, pozzolana and fly ash 11-35%, non-US",
                    "cement, pozzolana and fly ash 11-35%, non-US",
                ),
                (
                    "cement production, pozzolana and fly ash 15-40%, US only",
                    "cement, pozzolana and fly ash 15-40%, US only",
                ),
                (
                    "cement production, pozzolana and fly ash 36-55%,non-US",
                    "cement, pozzolana and fly ash 36-55%,non-US",
                ),
                (
                    "cement production, pozzolana and fly ash 5-15%, US only",
                    "cement, pozzolana and fly ash 5-15%, US only",
                ),
            ):
                act_cement = self.update_cement_production_datasets(i[0], i[1])
                self.db.extend([v for v in act_cement.values()])

                created_datasets.extend(
                    [
                        (act["name"], act["reference product"], act["location"])
                        for act in act_cement.values()
                    ]
                )
                self.relink_datasets(i[0], i[1])

            print("\nCreate new cement market datasets")

        else:
            print("\nCreate new cement market datasets")

            for i in (
                ("market for cement, Portland", "cement, Portland"),
                (
                    "market for cement, blast furnace slag 35-70%",
                    "cement, blast furnace slag 35-70%",
                ),
                (
                    "market for cement, blast furnace slag 6-34%",
                    "cement, blast furnace slag 6-34%",
                ),
                ("market for cement, limestone 6-10%", "cement, limestone 6-10%"),
                (
                    "market for cement, pozzolana and fly ash 15-50%",
                    "cement, pozzolana and fly ash 15-50%",
                ),
                (
                    "market for cement, pozzolana and fly ash 6-14%",
                    "cement, pozzolana and fly ash 6-14%",
                ),
                (
                    "market for cement, alternative constituents 6-20%",
                    "cement, alternative constituents 6-20%",
                ),
                (
                    "market for cement, alternative constituents 21-35%",
                    "cement, alternative constituents 21-35%",
                ),
                (
                    "market for cement, blast furnace slag 18-30% and 18-30% other alternative constituents",
                    "cement, blast furnace slag 18-30% and 18-30% other alternative constituents",
                ),
                (
                    "market for cement, blast furnace slag 31-50% and 31-50% other alternative constituents",
                    "cement, blast furnace slag 31-50% and 31-50% other alternative constituents",
                ),
                (
                    "market for cement, blast furnace slag 36-65%",
                    "cement, blast furnace slag 36-65%",
                ),
                (
                    "market for cement, blast furnace slag 66-80%",
                    "cement, blast furnace slag, 66-80%",
                ),
                (
                    "market for cement, blast furnace slag 81-95%",
                    "cement, blast furnace slag 81-95%",
                ),
                (
                    "market for cement, pozzolana and fly ash 11-35%",
                    "cement, pozzolana and fly ash 11-35%",
                ),
                (
                    "market for cement, pozzolana and fly ash 36-55%",
                    "cement, pozzolana and fly ash 36-55%",
                ),
                (
                    "market for cement, alternative constituents 45%",
                    "cement, alternative constituents 45%",
                ),
                (
                    "market for cement, blast furnace slag 40-70%",
                    "cement, blast furnace 40-70%",
                ),
                (
                    "market for cement, pozzolana and fly ash 25-35%",
                    "cement, pozzolana and fly ash 25-35%",
                ),
                ("market for cement, limestone 21-35%", "cement, limestone 21-35%"),
                (
                    "market for cement, blast furnace slag 21-35%",
                    "cement, blast furnace slag 21-35%",
                ),
                (
                    "market for cement, blast furnace slag 25-70%",
                    "cement, blast furnace slag 25-70%",
                ),
                (
                    "market for cement, blast furnace slag 5-25%",
                    "cement, blast furnace slag 5-25%",
                ),
                (
                    "market for cement, blast furnace slag 6-20%",
                    "cement, blast furnace slag 6-20%",
                ),
                (
                    "market for cement, blast furnace slag 70-100%",
                    "cement, blast furnace slag 70-100%",
                ),
                (
                    "market for cement, pozzolana and fly ash 15-40%",
                    "cement, pozzolana and fly ash 15-40%",
                ),
                (
                    "market for cement, pozzolana and fly ash 5-15%",
                    "cement, pozzolana and fly ash 5-15%",
                ),
                ("market for cement, unspecified", "cement, unspecified"),
                (
                    "market for cement, portland fly ash cement 21-35%",
                    "cement, portland fly ash cement 21-35%",
                ),
                (
                    "market for cement, portland fly ash cement 6-20%",
                    "cement, portland fly ash cement 6-20%",
                ),
                ("market for cement mortar", "cement mortar"),
                (
                    "market for cement, limestone cement 6-20%",
                    "cement, limestone 6-20%",
                ),
            ):
                act_cement = self.fetch_proxies(i[0], i[1])
                self.db.extend([v for v in act_cement.values()])

                created_datasets.extend(
                    [
                        (act["name"], act["reference product"], act["location"])
                        for act in act_cement.values()
                    ]
                )

                self.relink_datasets(i[0], i[1])

            for i in (
                ("cement production, Portland", "cement, Portland"),
                (
                    "cement production, blast furnace slag 35-70%",
                    "cement, blast furnace slag 35-70%",
                ),
                (
                    "cement production, blast furnace slag 6-34%",
                    "cement, blast furnace slag 6-34%",
                ),
                ("cement production, limestone 6-10%", "cement, limestone 6-10%"),
                (
                    "cement production, pozzolana and fly ash 15-50%",
                    "cement, pozzolana and fly ash 15-50%",
                ),
                (
                    "cement production, pozzolana and fly ash 6-14%",
                    "cement, pozzolana and fly ash 6-14%",
                ),
                (
                    "cement production, alternative constituents 6-20%",
                    "cement, alternative constituents 6-20%",
                ),
                (
                    "cement production, alternative constituents 21-35%",
                    "cement, alternative constituents 21-35%",
                ),
                (
                    "cement production, blast furnace slag 18-30% and 18-30% other alternative constituents",
                    "cement, blast furnace slag 18-30% and 18-30% other alternative constituents",
                ),
                (
                    "cement production, blast furnace slag 31-50% and 31-50% other alternative constituents",
                    "cement, blast furnace slag 31-50% and 31-50% other alternative constituents",
                ),
                (
                    "cement production, blast furnace slag 36-65%",
                    "cement, blast furnace slag 36-65%",
                ),
                (
                    "cement production, blast furnace slag 66-80%",
                    "cement, blast furnace slag, 66-80%",
                ),
                (
                    "cement production, blast furnace slag 81-95%",
                    "cement, blast furnace slag 81-95%",
                ),
                (
                    "cement production, pozzolana and fly ash 11-35%",
                    "cement, pozzolana and fly ash 11-35%",
                ),
                (
                    "cement production, pozzolana and fly ash 36-55%",
                    "cement, pozzolana and fly ash 36-55%",
                ),
                (
                    "cement production, alternative constituents 45%",
                    "cement, alternative constituents 45%",
                ),
                (
                    "cement production, blast furnace slag 40-70%",
                    "cement, blast furnace 40-70%",
                ),
                (
                    "cement production, pozzolana and fly ash 25-35%",
                    "cement, pozzolana and fly ash 25-35%",
                ),
                ("cement production, limestone 21-35%", "cement, limestone 21-35%"),
                (
                    "cement production, blast furnace slag 21-35%",
                    "cement, blast furnace slag 21-35%",
                ),
                (
                    "cement production, blast furnace slag 25-70%",
                    "cement, blast furnace slag 25-70%",
                ),
                (
                    "cement production, blast furnace slag 5-25%",
                    "cement, blast furnace slag 5-25%",
                ),
                (
                    "cement production, blast furnace slag 6-20%",
                    "cement, blast furnace slag 6-20%",
                ),
                (
                    "cement production, blast furnace slag 70-100%",
                    "cement, blast furnace slag 70-100%",
                ),
                (
                    "cement production, pozzolana and fly ash 15-40%",
                    "cement, pozzolana and fly ash 15-40%",
                ),
                (
                    "cement production, pozzolana and fly ash 5-15%",
                    "cement, pozzolana and fly ash 5-15%",
                ),
                (
                    "cement production, blast furnace slag 31-50% and 31-50% other alternative constituents",
                    "hard coal ash",
                ),
                (
                    "cement production, pozzolana and fly ash 6-14%",
                    "nickel smelter slag",
                ),
                (
                    "cement production, fly ash 21-35%",
                    "cement, portland fly ash cement 21-35%",
                ),
                ("cement production, fly ash 21-35%", "hard coal ash"),
                ("cement production, limestone 21-35%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 6-14%", "hard coal ash"),
                ("cement production, alternative constituents 45%", "hard coal ash"),
                ("cement production, limestone 6-20%", "cement, limestone 6-20%"),
                (
                    "cement production, pozzolana and fly ash 15-50%",
                    "nickel smelter slag",
                ),
                (
                    "cement production, blast furnace slag 18-30% and 18-30% other alternative constituents",
                    "hard coal ash",
                ),
                ("cement production, alternative constituents 6-20%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 36-55%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 15-50%", "hard coal ash"),
                (
                    "cement production, fly ash 6-20%",
                    "cement, portland fly ash cement 6-20%",
                ),
                ("cement production, alternative constituents 21-35%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 5-15%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 11-35%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 25-35%", "hard coal ash"),
                ("cement production, fly ash 6-20%", "hard coal ash"),
                ("cement production, pozzolana and fly ash 15-40%", "hard coal ash"),
            ):
                act_cement = self.update_cement_production_datasets(i[0], i[1])
                self.db.extend([v for v in act_cement.values()])

                created_datasets.extend(
                    [
                        (act["name"], act["reference product"], act["location"])
                        for act in act_cement.values()
                    ]
                )

                self.relink_datasets(i[0], i[1])

        if self.version == 3.5:
            name = "market for cement, unspecified"
            ref_prod = "cement, unspecified"

        else:
            name = "cement, all types to generic market for cement, unspecified"
            ref_prod = "cement, unspecified"
        self.relink_datasets(name, ref_prod)

        with open(
            DATA_DIR
            / "logs/log created cement datasets {} {} {}-{}.csv".format(
                self.model, self.scenario, self.year, date.today()
            ),
            "a",
        ) as csv_file:
            writer = csv.writer(csv_file, delimiter=";", lineterminator="\n")
            for line in created_datasets:
                writer.writerow(line)

        print("Relink cement production datasets to new clinker market datasets")
        self.relink_datasets("market for clinker", "clinker")

        print("Relink clinker market datasets to new clinker production datasets")
        self.relink_datasets("clinker production", "clinker")

        return self.db
