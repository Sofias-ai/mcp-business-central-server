import requests
from typing import Dict, Any, Optional
from .common import logger, get_bc_headers, get_bc_url

def get_bc_schema(resource: str) -> Dict[str, Any]:
    """Get schema information for a resource in Business Central."""
    logger.info(f"Getting schema for {resource}")
    
    try:
        response = requests.get(
            get_bc_url(resource),
            headers=get_bc_headers(),
            params={'$top': 1},
            verify=True
        )
        response.raise_for_status()
        data = response.json()
        
        # Extract fields from the first item if available
        fields = []
        if data.get('value') and data['value']:
            fields = list(data['value'][0].keys())
        
        return {
            "resource": resource,
            "available_fields": fields,
            "sample_item": data.get('value', [{}])[0] if data.get('value') else {},
        }
    except Exception as e:
        logger.error(f"Error fetching schema for {resource}: {e}")
        return {"error": str(e)}

def get_items(resource: str, top: Optional[int] = None, skip: Optional[int] = None, 
              filter: Optional[str] = None) -> Dict[str, Any]:
    """Get items from Business Central."""
    logger.info(f"Getting {resource}")
    
    # Build query parameters
    params = {k: v for k, v in {
        '$top': top, 
        '$skip': skip, 
        '$filter': filter
    }.items() if v is not None}
    
    try:
        response = requests.get(
            get_bc_url(resource),
            headers=get_bc_headers(),
            params=params,
            verify=True
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Error fetching {resource}: {e}")
        return {"error": str(e), "value": []}

def get_items_by_value(resource: str, field: str, value: str) -> Dict[str, Any]:
    """Get items from Business Central by field value."""
    return get_items(resource, filter=f"{field} eq '{value}'")