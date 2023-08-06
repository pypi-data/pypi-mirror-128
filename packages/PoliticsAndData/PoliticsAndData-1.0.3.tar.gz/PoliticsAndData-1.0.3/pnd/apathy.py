"""
Contains :py:class:`Apathy`.

- Run & Combine everything
"""

import threading
import json
from .specific import Alliances, Cities, Nations, Trades, Wars


class Apathy:
    """
    Made to make running and combining different categories easy.
    """

    def __init__(self, types=(Alliances, Cities, Nations, Trades, Wars), fs="filespace"):
        self.threads = []
        self.things = []
        self.filespace = fs

        for T in types:
            thing = T(fs=fs)
            self.things.append(thing)
            self.threads.append(
                threading.Thread(
                    target=thing.run,
                    daemon=True,
                    name=T.__name__)
            )

    def run(self):
        """
        ..py:function:: run(self: :py:class:`Apathy`) -> None

        - Runs :py:meth:`Apathy.collect` and :py:meth:`Apathy.combine`:.
        """
        self.collect()
        self.combine()

    def collect(self):
        """
        ..py:function:: collect(self: :py:class:`Apathy`) -> None

        - Runs all collection classes.
        """
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()

    def combine(self):
        """
        ..py:function:: combine(self: :py:class:`Apathy`) -> None

        - Combines all collected data into a single ``final.json``.
        """
        data = []

        for thing in self.things:
            with open(thing.file) as f:
                data.append(json.load(f)["timeline"])

        days = set(data[0].keys())
        for dat in data[1:]:
            days = days and set(dat.keys())

        final = {}
        for day in days:
            val = iter([])
            for dat in data:
                val += dat.items()
            final[day] = dict(val)

        with open(f"{self.filespace}/final.json") as f:
            json.dump(f, final)
