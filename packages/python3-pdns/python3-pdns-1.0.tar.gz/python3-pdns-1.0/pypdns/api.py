from typing import Dict
import requests
import logging


class Api_PDNS:
    def __init__(
        self,
        url: str,
    ) -> None:
        self.base_url = url
        self.request = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
        }
        self.headers = {}

    def connect(self, login: str, password: str) -> None:
        data = {"identity": login, "password": password}
        url = "%s/login" % self.base_url
        response = self.__make_requests("POST", url, data=data)
        if response.status_code == 200:
            res = response.json()
            self.headers = {"Authorization": "Bearer %s" % res["access_token"]}
        pass

    def get_records(self, domain: str) -> Dict:
        url = "%s/dn/%s" % (self.base_url, domain)
        response = self.__make_requests("GET", url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
    
    def add_domain(self, domain: str) -> bool:
        url = "%s/dn/%s" % (self.base_url, domain)
        response = self.__make_requests("POST", url, headers=self.headers)
        if response.status_code == 201:
            return True
        return False

    def get_reverse(self, ip: str) -> Dict:
        url = "%s/reverse/%s" % (self.base_url, ip)
        response = self.__make_requests("GET", url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_reverse_history(self, ip: str) -> Dict:
        url = "%s/reverse/%s/history" % (self.base_url, ip)
        response = self.__make_requests("GET", url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_resolutions_history(self, domain: str) -> Dict:
        url = "%s/resolution/%s/history" % (self.base_url, domain)
        response = self.__make_requests("GET", url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_last_resolution(self, domain: str) -> Dict:
        url = "%s/resolution/%s" % (self.base_url, domain)
        response = self.__make_requests("GET", url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

    def get_alerts(
        self,
        days=1,
        limit=10,
        filter_by="domainName",
        sort_by="domainName",
        export="json",
    ) -> Dict:
        url = "%s/alert" % self.base_url
        params = {
            "limit": limit,
            "days": days,
            "filter": "",
            "filter_by": filter_by,
            "sort_by": sort_by,
            "export": export,
        }
        response = self.__make_requests("GET", url, headers=self.headers, params=params)

        if response.status_code == 200:
            if export == "json":
                return response.json()
            if export == "csv":
                return response.text
        return {}

    def __make_requests(
        self, method: str, url: str, headers={}, data={}, params={}
    ) -> requests.Response:
        try:
            response = None
            if method == "POST":
                response = self.request[method](url, json=data, headers=headers)
            else:
                response = self.request[method](url, params=params, headers=headers)
        except KeyError:
            logging.error("Unsupported method %s " % method)

        return response
