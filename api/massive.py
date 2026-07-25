import requests
from flask import current_app

class MassiveAPI:
    def __init__(self):
        # Allow lazy configuration access so app context is available when initialized
        self._endpoint = None
        self._token = None

    @property
    def base_endpoint(self):
        if self._endpoint is None:
            self._endpoint = current_app.config.get("MASSIVE_ENDPOINT", "https://api.massive.com")
        return self._endpoint

    @property
    def token(self):
        if self._token is None:
            self._token = current_app.config.get("MASSIVE_API_TOKEN")
        return self._token

    def custom_bars(self, indices_ticker=None, multiplier=None, timespan=None, from_date=None, to_date=None, sort=None, limit=None, args=None):
        """
        Indices - Custom Bars (OHLC)
        Endpoint: GET /v2/aggs/ticker/{indicesTicker}/range/{multiplier}/{timespan}/{from}/{to}
        """
        if args is None:
            args = {}

        # Support both positional/keyword arguments and dictionary values (args)
        ticker = args.get("indicesTicker", args.get("indices_ticker", indices_ticker))
        mult = args.get("multiplier", multiplier)
        span = args.get("timespan", timespan)
        f_date = args.get("from", args.get("from_date", from_date))
        t_date = args.get("to", args.get("to_date", to_date))
        srt = args.get("sort", sort)
        lim = args.get("limit", limit)

        # Basic validation
        if not ticker:
            raise ValueError("indicesTicker is required")
        if mult is None:
            raise ValueError("multiplier is required")
        if not span:
            raise ValueError("timespan is required")
        if not f_date:
            raise ValueError("from (start date/timestamp) is required")
        if not t_date:
            raise ValueError("to (end date/timestamp) is required")

        base = self.base_endpoint.rstrip("/")
        endpoint = f"{base}/v2/aggs/ticker/I:{ticker}/range/{mult}/{span}/{f_date}/{t_date}"

        headers = {
            "Content-Type": "application/json"
        }
        params = {}

        # Add authentication if token is provided
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
            params["apiKey"] = self.token

        if srt:
            params["sort"] = srt
        if lim is not None:
            params["limit"] = lim

        response = requests.get(endpoint, params=params, headers=headers)
        return response.json()
