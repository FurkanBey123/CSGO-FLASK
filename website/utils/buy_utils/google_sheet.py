import json
import gspread
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'buff_keys.json')


class GoogleSheet:
    def __init__(self):
        self.service_account = gspread.service_account(filename=filename)
        self.sheet = "Buff Data"
        self._buff_dict = {}
        self._steam_dict = {}
        self._history_dict = {}

    async def get_buff_items(self):
        sheet = self.service_account.open(self.sheet)
        worksheet = sheet.worksheet("Sheet1")
        buff_data = worksheet.get_all_records()
        for item_buff in buff_data:
            item_name = item_buff["ITEM"]
            item_listing = item_buff["LISTING"]
            item_buy_order = item_buff["BUY ORDER"]
            item_listing7 = item_buff["LISTING_7"]
            item_listing30 = item_buff["LISTING_30"]
            item_listing60 = item_buff["LISTING_60"]

            self._buff_dict[item_name] = {}
            self._buff_dict[item_name]["listing"] = item_listing
            self._buff_dict[item_name]["buy_order"] = item_buy_order
            self._buff_dict[item_name]["listing7"] = item_listing7
            self._buff_dict[item_name]["listing30"] = item_listing30
            self._buff_dict[item_name]["listing60"] = item_listing60
        return self._buff_dict

    async def get_steam_inventories(self):
        sheet = self.service_account.open(self.sheet)
        worksheet = sheet.worksheet("Sheet2")
        users = worksheet.row_values(1)
        for idx, user in enumerate(users):
            items_of_user = worksheet.col_values(idx + 1)
            for item_name in items_of_user[1:]:
                self._steam_dict[item_name] = user

        return self._steam_dict

    async def get_item_histories(self):
        sheet = self.service_account.open(self.sheet)
        worksheet = sheet.worksheet("Sheet3")
        sell_history_data = worksheet.get_all_records()

        for item in sell_history_data:
            item_name = item["ITEM NAME"]
            item_shadowpay7 = json.loads(item["SHADOWPAY_7"])
            item_shadowpay14 = json.loads(item["SHADOWPAY_14"])
            item_shadowpay30 = json.loads(item["SHADOWPAY_30"])
            item_waxpeer7 = json.loads(item["WAXPEER_7"])
            item_waxpeer14 = json.loads(item["WAXPEER_14"])
            item_waxpeer30 = json.loads(item["WAXPEER_30"])
            item_market7 = json.loads(item["CSGOTM_7"])
            item_market14 = json.loads(item["CSGOTM_14"])
            item_market30 = json.loads(item["CSGOTM_30"])

            # Math Here
            total_7 = item_shadowpay7 + item_waxpeer7 + item_market7
            total_7_converted = [int(x) for x in total_7]
            if not len(total_7_converted) == 0:
                average_7 = sum(total_7_converted) / len(total_7_converted)
            else:
                average_7 = 0

            total_14 = item_shadowpay14 + item_waxpeer14 + item_market14
            total_14_converted = [int(x) for x in total_14]
            if not len(total_14_converted) == 0:
                average_14 = sum(total_14_converted) / len(total_14_converted)
            else:
                average_14 = 0

            total_30 = item_shadowpay30 + item_waxpeer30 + item_market30
            total_30_converted = [int(x) for x in total_30]
            if not len(total_30_converted) == 0:
                average_30 = sum(total_30_converted) / len(total_30_converted)
            else:
                average_30 = 0

            self._history_dict[item_name] = {
                "shadowpay": {
                    "7": item_shadowpay7,
                    "14": item_shadowpay14,
                    "30": item_shadowpay30
                },
                "waxpeer": {
                    "7": item_waxpeer7,
                    "14": item_waxpeer14,
                    "30": item_waxpeer30
                },
                "csgo_market": {
                    "7": item_market7,
                    "14": item_market14,
                    "30": item_market30
                },
                "average_7": average_7,
                "average_14": average_14,
                "average_30": average_30,
            }

        return self._history_dict

    def get_buff_dict(self):
        return self._buff_dict

    def set_buff_dict(self, new_dict: dict):
        self._buff_dict = new_dict

    def get_steam_dict(self):
        return self._steam_dict

    def set_steam_dict(self, new_dict: dict):
        self._steam_dict = new_dict