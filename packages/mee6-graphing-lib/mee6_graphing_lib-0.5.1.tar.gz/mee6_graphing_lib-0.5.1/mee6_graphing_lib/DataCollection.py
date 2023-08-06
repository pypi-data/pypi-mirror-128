import asyncio
import time
import json
import datetime
import matplotlib.pyplot as plt
from mee6_py_api import API
import itertools
import re
import matplotlib.cm as cm
from collections import OrderedDict
from matplotlib.colors import Normalize
from numpy.random import rand as Rand


class DataCollection(object):
    def __init__(self):
        self.__mee6API = API(377946908783673344)
        self.__time_format_str = "%d-%B-%Y %H:%M:%S"

    def __plotter_1(self):

        with open("db.json", "r") as fo:
            db = json.loads(fo.read())

        keys = list(db.keys())[0:100]

        c = []

        for z in range(10):
            for r in range(10):
                index_to_get = z * 10 + r

                c += [index_to_get]

                e = keys[index_to_get]

                dates = [
                    (datetime.datetime.strptime(i, self.__time_format_str)).strftime(
                        "%-d-%b-%-y"
                    )
                    for i in db[e]["xp_data"].keys()
                ]
                # dates = [i for i in db[e]['xp_data'].keys()]
                user_name = re.sub(
                    "/(\w+)/",
                    "",
                    db[e]["name"],
                )
                plt.plot(dates, db[e]["xp_data"].values(), label=user_name)

            plt.grid()
            plt.xlabel("Dates")
            plt.xticks(rotation=-45, ha="left")
            plt.ylabel("XP")
            plt.title(f"XP Data {r + 1}")
            plt.legend(loc="best", bbox_to_anchor=(1, 1))
            # plt.show()
            # plt.figure(figsize=(8,8));
            plt.savefig(f"static/plot{z + 1}.png", bbox_inches="tight", dpi=200)
            plt.close()

    def __plotter_2(self):
        with open("db.json", "r") as fo:
            db = json.load(fo)

        xp_uid = {}

        x = 0

        date_tmp = list(list(db.values())[0]["xp_data"].keys())

        if len(date_tmp) < 2:
            return

        d2 = (
            datetime.datetime.strptime(date_tmp[-1], self.__time_format_str)
        ).strftime("%-d-%b-%-y")
        d1 = (
            datetime.datetime.strptime(date_tmp[-2], self.__time_format_str)
        ).strftime("%-d-%b-%-y")

        for u_id in db:
            data = db[u_id]
            if len(list(data["xp_data"].values())) < 2:
                continue
            xp_g = (
                list(data["xp_data"].values())[-1] - list(data["xp_data"].values())[-2]
            )
            xp_uid.update({u_id: xp_g})

        fin_list = dict(
            itertools.islice(
                (
                    dict(sorted(xp_uid.items(), key=lambda x: x[1], reverse=True))
                ).items(),
                10,
            )
        )

        n_fin_dict = OrderedDict({})

        for u_id in fin_list:
            name = re.sub(
                "/(\w+)/",
                "",
                db[u_id]["name"],
            )
            xp_g = fin_list[u_id]

            n_fin_dict.update({name: xp_g})

        _tmp_val = list(n_fin_dict.values())

        my_norm = Normalize(vmin=_tmp_val[-1], vmax=_tmp_val[0])
        plt.bar(
            n_fin_dict.keys(),
            n_fin_dict.values(),
            color=["#77dd77", "#89cff0", "#ffb7ce", "#ff6961", "#ca9bf7", "#f4bfff"],
        )

        plt.xlabel("Usernames")
        plt.xticks(rotation=-45, ha="left")
        plt.ylabel("XP Gained")
        plt.title(f"Top XP Earners between {d1} and {d2}")
        plt.legend(loc="best", bbox_to_anchor=(1, 1))
        # plt.show()
        # plt.figure(figsize=(8,8));
        plt.savefig(f"static/top_{d1}_to_{d2}.png", bbox_inches="tight", dpi=200)
        plt.close()

    def get_details(self):
        details = []

        xp_trigger = False

        with open("db.json", "r") as fo:
            db = json.load(fo)

        for i in range(100):
            tom = asyncio.run(self.__API_fetch(i))

            if xp_trigger:
                break

            for l in tom["players"]:
                if l["xp"] < 300:
                    xp_trigger = True
                    break

                try:
                    asd = db[l["id"]]
                    temp_xp_data = asd["xp_data"]
                    temp_xp_data.update(
                        {time.strftime(self.__time_format_str, time.gmtime()): l["xp"]}
                    )

                    # print(temp_xp_data)

                    db.update(
                        {l["id"]: {"name": l["username"], "xp_data": temp_xp_data}}
                    )

                    # print(db[l["id"]])

                except:
                    db.update(
                        {
                            l["id"]: {
                                "name": l["username"],
                                "xp_data": {
                                    time.strftime(
                                        self.__time_format_str, time.gmtime()
                                    ): l["xp"]
                                },
                            }
                        }
                    )

                details += [{int(l["id"]): l["xp"]}]

            # print(i)

        with open("db.json", "w+") as fo:
            json.dump(db, fo, indent=2)

        self.__plotter_1()
        self.__plotter_2()

        # print(details)

        # pl/otter_1(db)
        # for i in range(1, 864001):
        #     print(i)
        #     time.sleep(1)

        return

    async def __API_fetch(self, index):
        return await self.__mee6API.levels.get_leaderboard_page(index)
