"""Controllers for event frame endpoints."""

from __future__ import annotations

from typing import Dict, Optional

from .base import BaseController

__all__ = [
    'EventFrameController',
]


class EventFrameController(BaseController):
    """Controller for Event Frame operations."""

    def get(self, web_id: str, selected_fields: Optional[str] = None) -> Dict:
        """Get an event frame by its WebID."""
        params: Dict[str, object] = {}
        if selected_fields:
            params['selectedFields'] = selected_fields
        return self.client.get(f"eventframes/{web_id}", params=params)

    def get_by_path(self, path: str, selected_fields: Optional[str] = None) -> Dict:
        """Get an event frame by path."""
        params: Dict[str, object] = {}
        if selected_fields:
            params['selectedFields'] = selected_fields
        encoded_path = self._encode_path(path)
        return self.client.get(f"eventframes/path/{encoded_path}", params=params)

    def create(self, database_web_id: str, event_frame: Dict) -> Dict:
        """Create a new event frame in an asset database."""
        return self.client.post(
            f"assetdatabases/{database_web_id}/eventframes",
            data=event_frame,
        )

    def update(self, web_id: str, event_frame: Dict) -> Dict:
        """Update an existing event frame."""
        return self.client.patch(f"eventframes/{web_id}", data=event_frame)

    def delete(self, web_id: str) -> Dict:
        """Delete an event frame."""
        return self.client.delete(f"eventframes/{web_id}")

    def get_event_frames(
        self,
        database_web_id: str,
        name_filter: Optional[str] = None,
        category_name: Optional[str] = None,
        template_name: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        search_full_hierarchy: bool = False,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        start_index: int = 0,
        max_count: int = 1000,
        selected_fields: Optional[str] = None,
    ) -> Dict:
        """Retrieve event frames from an asset database."""
        params: Dict[str, object] = {
            'searchFullHierarchy': search_full_hierarchy,
            'startIndex': start_index,
            'maxCount': max_count,
        }
        if name_filter:
            params['nameFilter'] = name_filter
        if category_name:
            params['categoryName'] = category_name
        if template_name:
            params['templateName'] = template_name
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        if sort_field:
            params['sortField'] = sort_field
        if sort_order:
            params['sortOrder'] = sort_order
        if selected_fields:
            params['selectedFields'] = selected_fields

        return self.client.get(
            f"assetdatabases/{database_web_id}/eventframes",
            params=params,
        )

    def get_attributes(
        self,
        web_id: str,
        name_filter: Optional[str] = None,
        category_name: Optional[str] = None,
        template_name: Optional[str] = None,
        value_type: Optional[str] = None,
        start_index: int = 0,
        max_count: int = 1000,
        selected_fields: Optional[str] = None,
    ) -> Dict:
        """Retrieve attributes attached to an event frame."""
        params: Dict[str, object] = {
            'startIndex': start_index,
            'maxCount': max_count,
        }
        if name_filter:
            params['nameFilter'] = name_filter
        if category_name:
            params['categoryName'] = category_name
        if template_name:
            params['templateName'] = template_name
        if value_type:
            params['valueType'] = value_type
        if selected_fields:
            params['selectedFields'] = selected_fields

        return self.client.get(f"eventframes/{web_id}/attributes", params=params)

    def create_attribute(self, web_id: str, attribute: Dict) -> Dict:
        """Create an attribute for an event frame."""
        return self.client.post(f"eventframes/{web_id}/attributes", data=attribute)
