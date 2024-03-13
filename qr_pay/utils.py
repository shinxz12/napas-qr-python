import json
from typing import List, Optional

import requests


class Bank:
    def __init__(self) -> None:
        self.banks = self.get_banks()

    def update_banks(self) -> List[dict]:
        url = "https://api.vietqr.io/v2/banks"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["data"]
        with open("./resources/banks.json", "w") as file:
            json.dump(data, file)
        self.banks = data
        return data

    def get_banks(self) -> List[dict]:
        try:
            with open("./resources/banks.json", "r") as file:
                data = json.load(file)
                return data
        except:
            return self.update_banks()

    def get_bank_by_code(self, code: str) -> Optional[dict]:
        result = list(filter(lambda x: x["code"] == code.upper(), self.banks))
        return result[0] if result else None
