"""Controllers for asset model endpoints."""

from __future__ import annotations

from typing import Dict, Optional

from .base import BaseController

__all__ = [
    "AssetServerController",
    "AssetDatabaseController",
    "ElementController",
    "ElementCategoryController",
    "ElementTemplateController",
]


class AssetServerController(BaseController):
    """Controller for Asset Server operations."""

    def list(self) -> Dict:
        """List all asset servers."""
        return self.client.get("assetservers")

    def get(self, web_id: str, selected_fields: Optional[str] = None) -> Dict:
        """Get asset server by WebID."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(f"assetservers/{web_id}", params=params)

    def get_by_name(self, name: str, selected_fields: Optional[str] = None) -> Dict:
        """Get asset server by name."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(
            f"assetservers/name/{self._encode_path(name)}", params=params
        )

    def get_by_path(self, path: str, selected_fields: Optional[str] = None) -> Dict:
        """Get asset server by path."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(
            f"assetservers/path/{self._encode_path(path)}", params=params
        )

    def get_databases(self, web_id: str, selected_fields: Optional[str] = None) -> Dict:
        """Get databases for an asset server."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(f"assetservers/{web_id}/assetdatabases", params=params)


class AssetDatabaseController(BaseController):
    """Controller for Asset Database operations."""

    def get_default_server(self) -> Dict:
        asset_server = self.client.asset_server.list()
        return asset_server["Items"][0]

    def get_default_database(self) -> Dict:
        asset_server = self.get_default_server()
        asset_database = self.client.asset_server.get_databases(asset_server["WebId"])
        return asset_database["Items"][1]

    def get(self, web_id: str, selected_fields: Optional[str] = None) -> Dict:
        """Get asset database by WebID."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(f"assetdatabases/{web_id}", params=params)

    def get_by_path(self, path: str, selected_fields: Optional[str] = None) -> Dict:
        """Get asset database by path."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(
            f"assetdatabases/path/{self._encode_path(path)}", params=params
        )

    def update(self, web_id: str, database: Dict) -> Dict:
        """Update an asset database."""
        return self.client.patch(f"assetdatabases/{web_id}", data=database)

    def delete(self, web_id: str) -> Dict:
        """Delete an asset database."""
        return self.client.delete(f"assetdatabases/{web_id}")

    def get_elements(
        self,
        web_id: str,
        name_filter: Optional[str] = None,
        category_name: Optional[str] = None,
        template_name: Optional[str] = None,
        element_type: Optional[str] = None,
        search_full_hierarchy: bool = False,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        start_index: int = 0,
        max_count: int = 1000,
        selected_fields: Optional[str] = None,
    ) -> Dict:
        """Get elements from asset database."""
        params = {
            "startIndex": start_index,
            "maxCount": max_count,
            "searchFullHierarchy": search_full_hierarchy,
        }
        if name_filter:
            params["nameFilter"] = name_filter
        if category_name:
            params["categoryName"] = category_name
        if template_name:
            params["templateName"] = template_name
        if element_type:
            params["elementType"] = element_type
        if sort_field:
            params["sortField"] = sort_field
        if sort_order:
            params["sortOrder"] = sort_order
        if selected_fields:
            params["selectedFields"] = selected_fields

        return self.client.get(f"assetdatabases/{web_id}/elements", params=params)

    def create_element(self, web_id: str, element: Dict) -> Dict:
        """Create an element in the asset database."""
        return self.client.post(f"assetdatabases/{web_id}/elements", data=element)


class ElementController(BaseController):
    """Controller for Element operations."""

    def get(self, web_id: str, selected_fields: Optional[str] = None) -> Dict:
        """Get element by WebID."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(f"elements/{web_id}", params=params)

    def get_by_path(self, path: str, selected_fields: Optional[str] = None) -> Dict:
        """Get element by path."""
        params = {}
        if selected_fields:
            params["selectedFields"] = selected_fields
        return self.client.get(
            f"elements?path={path}".replace(" ", "%20"), params=params
        )

    def update(self, web_id: str, element: Dict) -> Dict:
        """Update an element."""
        return self.client.patch(f"elements/{web_id}", data=element)

    def delete(self, web_id: str) -> Dict:
        """Delete an element."""
        return self.client.delete(f"elements/{web_id}")

    def get_attributes(
        self,
        web_id: str,
        name_filter: Optional[str] = None,
        category_name: Optional[str] = None,
        template_name: Optional[str] = None,
        value_type: Optional[str] = None,
        search_full_hierarchy: bool = False,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        start_index: int = 0,
        max_count: int = 1000,
        selected_fields: Optional[str] = None,
    ) -> Dict:
        """Get attributes for an element."""
        params = {
            "startIndex": start_index,
            "maxCount": max_count,
            "searchFullHierarchy": search_full_hierarchy,
        }
        if name_filter:
            params["nameFilter"] = name_filter
        if category_name:
            params["categoryName"] = category_name
        if template_name:
            params["templateName"] = template_name
        if value_type:
            params["valueType"] = value_type
        if sort_field:
            params["sortField"] = sort_field
        if sort_order:
            params["sortOrder"] = sort_order
        if selected_fields:
            params["selectedFields"] = selected_fields

        return self.client.get(f"elements/{web_id}/attributes", params=params)

    def create_attribute(self, web_id: str, attribute: Dict) -> Dict:
        """Create an attribute on the element."""
        return self.client.post(f"elements/{web_id}/attributes", data=attribute)

    def get_elements(
        self,
        web_id: str,
        name_filter: Optional[str] = None,
        category_name: Optional[str] = None,
        template_name: Optional[str] = None,
        element_type: Optional[str] = None,
        search_full_hierarchy: bool = False,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        start_index: int = 0,
        max_count: int = 1000,
        selected_fields: Optional[str] = None,
    ) -> Dict:
        """Get child elements."""
        params = {
            "startIndex": start_index,
            "maxCount": max_count,
            "searchFullHierarchy": search_full_hierarchy,
        }
        if name_filter:
            params["nameFilter"] = name_filter
        if category_name:
            params["categoryName"] = category_name
        if template_name:
            params["templateName"] = template_name
        if element_type:
            params["elementType"] = element_type
        if sort_field:
            params["sortField"] = sort_field
        if sort_order:
            params["sortOrder"] = sort_order
        if selected_fields:
            params["selectedFields"] = selected_fields

        return self.client.get(f"elements/{web_id}/elements", params=params)

    def create_element(self, web_id: str, element: Dict) -> Dict:
        """Create a child element."""
        return self.client.post(f"elements/{web_id}/elements", data=element)


class ElementCategoryController(BaseController):
    """Controller for Element Category operations."""

    pass


class ElementTemplateController(BaseController):
    """Controller for Element Template operations."""

    pass
