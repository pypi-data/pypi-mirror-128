from ujson import dumps
from typing import Optional
from aiohttp import ClientSession
from aiohttp.client import ClientTimeout

from .utils.exceptions import CheckException


class AminoHttpClient:
    _session: ClientSession = None
    apip: str = "https://aminoapps.com/api-p"
    api: str = "https://service.narvii.com/api/v1"

    headers = {
        "Accept-Language": "en-En",
        "NDCDEVICEID"    : "22CCEA23A7F868405192250D13EDA48245F4442E89" \
                            "293554E7A7320BA4E3F7C6E79985F239D012C1B2",
        "Content-Type"   : "application/json; charset=utf-8"
    }

    @property
    def session(self) -> ClientSession:
        if not self._session:
            self._session = ClientSession(timeout=ClientTimeout(60))
        return self._session
    
    @session.setter
    def session(self, session: ClientSession) -> None:
        self._session = session
    
    @property
    def userId(self) -> ClientSession:
        userId: Optional[str] = self.headers.get("AUID")
        return userId if userId else None
    
    @userId.setter
    def userId(self, userId: str) -> None:
        self.headers["AUID"] = userId
    
    @property
    def deviceId(self) -> Optional[str]:
        deviceId: Optional[str] = self.headers.get("NDCDEVICEID")
        return deviceId if deviceId else None

    @deviceId.setter
    def deviceId(self, device_id: str) -> None:
        self.headers["NDCDEVICEID"] = device_id

    @property
    def sid(self) -> Optional[str]:
        sid: Optional[str] = self.headers.get('NDCAUTH')
        return sid.split("=")[1] if sid else None

    @sid.setter
    def sid(self, sid: str) -> None:
        self.headers["NDCAUTH"] = f"sid={sid}"
    
    async def post_content(self, url: str, data: dict, type: str):
        headers = self.headers
        headers["Content-Type"] = type

        async with self._session.post(f"{self.apip}{url}", 
                json=data, headers=headers) as response:

            if (json := await response.json())["api:statuscode"] != 0:
                return CheckException(json)
            return response
    
    async def post(self, url: str, data: dict = None):
        async with self._session.post(f"{self.apip}{url}", 
                json=data, headers=self.headers) as response:

            if (json := await response.json())["api:statuscode"] != 0:
                return CheckException(json)
            return response

    async def get(self, url: str):
        async with self._session.get(f"{self.api}{url}",
                headers=self.headers) as response:

            if (json := await response.json())["api:statuscode"] != 0:
                return CheckException(json)
            return response
    
    async def delete(self, url: str):
        async with self._session.delete(f"{self.api}{url}",
                headers=self.headers) as response:

            if (json := await response.json())["api:statuscode"] != 0:
                return CheckException(json)
            return response
    
    async def post_request(self, url: str, data: str = None, headers: dict = None):
        return await self._session.post(url, data=data, headers=headers)

    async def get_request(self, url: str, headers: dict = None):
        return await self._session.get(url, headers=headers)
