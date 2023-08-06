"""
Contains :py:class:`Alliances`, :py:class:`Cities`, :py:class:`Nations`, :py:class:`Trades`, and :py:class:`Wars`.

- Default :py:class:`Boredom` subclass for each category.
- Subclass, modify, or examine as an example for custom subclasses.
"""

from .boredom import Boredom


class Alliances(Boredom):
    """Collect from Alliances. Subclass or modify as object to modify collection"""

    def __init__(self, **kwargs):
        super().__init__("alliances", **kwargs)

        self.length = "aa_count"
        self.total = [("total_aa_score", 7, float)]


class Cities(Boredom):
    """Collect from Cities. Subclass or modify as object to modify collection"""

    def __init__(self, **kwargs):
        super().__init__("cities", **kwargs)

        self.length = "city_count"
        self.total = [
            ("total_infrastructure", 5, float),
            ("total_land", 7, float),
            ("oil_pp", 8, int),
            ("wind_pp", 9, int),
            ("coal_pp", 10, int),
            ("nuclear_pp", 11, int),
            ("coal_mines", 12, int),
            ("oil_wells", 13, int),
            ("uranium_mines", 14, int),
            ("iron_mines", 15, int),
            ("lead_mines", 16, int),
            ("bauxite_mines", 17, int),
            ("farms", 18, int),
            ("supermarkets", 23, int),
            ("banks", 24, int),
            ("shopping_malls", 25, int),
            ("stadiums", 26, int),
            ("oil_refineries", 27, int),
            ("aluminum_refineries", 28, int),
            ("steel_mills", 29, int),
            ("munitions_factories", 30, int)
        ]


class Nations(Boredom):
    """Collect from Nations. Subclass or modify as object to modify collection"""

    def __init__(self, **kwargs):
        super().__init__("nations", **kwargs)

        self.length = "nation_count"
        self.total = [
            ("total_score", "score", float),
            ("total_population", "population", int),
            ("beige", "beige_turns_remaining", int),
            ("soldiers", "soldiers", int),
            ("tanks", "tanks", int),
            ("aircraft", "aircraft", int),
            ("ships", "ships", int),
            ("missiles", "missiles", int),
            ("nukes", "nukes", int),
        ]
        self.match = [
            ("gray", 12, "gray"),
            ("blitzkrieg", 30, "Blitzkrieg"),
        ]

    def run(self, force_new=False, ignore=True):
        """

        :param force_new: Default value = False)
        :param ignore: Default value = True)

        """
        super().run(force_new, ignore)


class Trades(Boredom):
    """Collect from Trades. Subclass or modify as object to modify collection"""

    def __init__(self, **kwargs):
        super().__init__("trades", **kwargs)
        self.rss = [
            "credits",
            "food",
            "coal",
            "oil",
            "uranium",
            "lead",
            "iron",
            "bauxite",
            "gasoline",
            "munitions",
            "steel",
            "aluminum",
        ]

    def spec_collection(self, data: list, ignore=False):
        """

        :param data: list:
        :param ignore: Default value = False)

        """
        super().spec_collection(data, ignore)

        sell = "%s_sell_total_value"
        buy = "%s_buy_total_value"
        quant_s = "%s_sell_quantity"
        quant_b = "%s_buy_quantity"
        av_price_s = "%s_sell_average_price"
        av_price_b = "%s_buy_average_price"

        for resource in self.rss:
            self.collected[sell % resource] = 0
            self.collected[buy % resource] = 0
            self.collected[quant_s % resource] = 0
            self.collected[quant_b % resource] = 0
        for line in data:
            quantity = int(line["quantity"])
            price = int(line["price"])

            resource = self.rss.index(line["resource"])
            if line["accepted"] != "1":
                continue
            if line["offer_type"] != "0":
                continue
            if resource == -1:
                raise KeyError
            rs = self.rss[resource]
            self.collected[sell % rs] += quantity * price*(line["buy_or_sell"] == "sell")
            self.collected[quant_s % rs] += quantity*(line["buy_or_sell"] == "sell")
            self.collected[buy % rs] += quantity * price*(line["buy_or_sell"] == "buy")
            self.collected[quant_b % rs] += quantity*(line["buy_or_sell"] == "buy")

        for resource in self.rss:
            self.collected[av_price_s % resource] = self.collected[sell % resource]/self.collected[quant_s % resource]
            self.collected[av_price_b % resource] = self.collected[buy % resource]/self.collected[quant_b % resource]


class Wars(Boredom):
    """Collect from Wars. Subclass or modify as object to modify collection"""

    def __init__(self, **kwargs):
        super().__init__("wars", **kwargs)
        self.total = [
            ("infra_destroyed", 32, float),
            ("infra_destroyed", 33, float),
            ("aircraft_destroyed", 40, int),
            ("aircraft_destroyed", 41, int),
            ("missiles_used", 44, int),
            ("missiles_used", 45, int),
            ("nukes_used", 46, int),
            ("nukes_used", 47, int)
        ]
        self.match = [
            ("raid_count", "war_type", "raid"),
            ("attrition_count", "war_type", "att"),
            ("ordinary_count", "war_type", "ord")
        ]
