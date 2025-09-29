"""HTTP client and request coordination for the PI Web API."""

from __future__ import annotations

from typing import Dict, Optional

import requests

from .config import AuthMethod, PIWebAPIConfig
from .controllers import (
    AnalysisController,
    AnalysisCategoryController,
    AnalysisRuleController,
    AnalysisTemplateController,
    AssetDatabaseController,
    AssetServerController,
    AttributeController,
    AttributeCategoryController,
    AttributeTemplateController,
    BatchController,
    CalculationController,
    ChannelController,
    ConfigurationController,
    DataServerController,
    ElementController,
    ElementCategoryController,
    ElementTemplateController,
    EnumerationSetController,
    EnumerationValueController,
    EventFrameController,
    HomeController,
    PointController,
    StreamController,
    StreamSetController,
    SystemController,
    TableController,
)
from .exceptions import PIWebAPIError

__all__ = ['PIWebAPIClient']

class PIWebAPIClient:
    """Main PI Web API client."""

    def __init__(self, config: PIWebAPIConfig):
        self.config = config
        self.session = requests.Session()
        self._setup_authentication()

        # Initialize controller instances
        self.analysis = AnalysisController(self)
        self.analysis_category = AnalysisCategoryController(self)
        self.analysis_rule = AnalysisRuleController(self)
        self.analysis_template = AnalysisTemplateController(self)
        self.asset_database = AssetDatabaseController(self)
        self.asset_server = AssetServerController(self)
        self.attribute = AttributeController(self)
        self.attribute_category = AttributeCategoryController(self)
        self.attribute_template = AttributeTemplateController(self)
        self.batch = BatchController(self)
        self.calculation = CalculationController(self)
        self.channel = ChannelController(self)
        self.configuration = ConfigurationController(self)
        self.data_server = DataServerController(self)
        self.element = ElementController(self)
        self.element_category = ElementCategoryController(self)
        self.element_template = ElementTemplateController(self)
        self.enumeration_set = EnumerationSetController(self)
        self.enumeration_value = EnumerationValueController(self)
        self.event_frame = EventFrameController(self)
        self.home = HomeController(self)
        self.point = PointController(self)
        self.stream = StreamController(self)
        self.streamset = StreamSetController(self)
        self.system = SystemController(self)
        self.table = TableController(self)

    def _setup_authentication(self):
        """Setup authentication for the session."""
        if self.config.auth_method == AuthMethod.BASIC:
            if self.config.username and self.config.password:
                self.session.auth = (self.config.username, self.config.password)
            else:
                raise PIWebAPIError(
                    "Username and password required for basic authentication"
                )
        elif self.config.auth_method == AuthMethod.BEARER:
            if self.config.token:
                self.session.headers.update(
                    {"Authorization": f"Bearer {self.config.token}"}
                )
            else:
                raise PIWebAPIError("Token required for bearer authentication")
        elif self.config.auth_method == AuthMethod.KERBEROS:
            # Kerberos authentication would require additional setup
            raise PIWebAPIError("Kerberos authentication not implemented in this SDK")
        elif self.config.auth_method == AuthMethod.ANONYMOUS:
            # No authentication setup needed for anonymous access
            pass

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json_data: Optional[Dict] = None,
    ) -> Dict:
        """Make HTTP request to PI Web API."""
        url = f"{self.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        # Add webIdType to params if not already specified
        if params is None:
            params = {}
        if "webIdType" not in params:
            params["webIdType"] = self.config.webid_type.value

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                verify=self.config.verify_ssl,
                timeout=self.config.timeout,
            )

            # Check for HTTP errors
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_message = (
                        error_data.get("Errors", [response.text])[0]
                        if error_data.get("Errors")
                        else response.text
                    )
                except:
                    error_message = response.text
                raise PIWebAPIError(
                    error_message,
                    response.status_code,
                    error_data if "error_data" in locals() else None,
                )

            # Parse JSON response
            try:
                return response.json()
            except ValueError:
                return {"content": response.text}

        except requests.RequestException as e:
            raise PIWebAPIError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request."""
        return self._make_request("GET", endpoint, params=params)

    def post(
        self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Dict:
        """Make POST request."""
        return self._make_request("POST", endpoint, params=params, json_data=data)

    def put(
        self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Dict:
        """Make PUT request."""
        return self._make_request("PUT", endpoint, params=params, json_data=data)

    def patch(
        self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None
    ) -> Dict:
        """Make PATCH request."""
        return self._make_request("PATCH", endpoint, params=params, json_data=data)

    def delete(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make DELETE request."""
        return self._make_request("DELETE", endpoint, params=params)
