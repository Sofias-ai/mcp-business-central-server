from typing import Dict, Any, Optional
from .common import logger, mcp, bc_request

def create_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a standardized API response"""
    if "error" in data: return {"error": data["error"], "success": False}
    return {    "success": True,
                "count": len(data.get("value", [])) if "value" in data else 1,
                "data": data}

@mcp.tool(name="BC_Get_Schema", description="Get schema information for a Business Central resource.")
async def get_schema_tool(resource: str) -> Dict[str, Any]:
    logger.info(f"Tool 'BC_Get_Schema' called for resource={resource}")
    
    result = await bc_request("GET", resource, params={'$top': 1})
    if "error" in result: return {"error": result["error"], "success": False}
    fields = []
    
    if result.get('value') and result['value']:
        fields = list(result['value'][0].keys())
    
    return {"success": True, "data": {
        "resource": resource,
        "available_fields": fields,
        "sample_item": result.get('value', [{}])[0] if result.get('value') else {},
    }}

@mcp.tool(name="BC_List_Items", description="Get items from Business Central with filtering and pagination.")
async def list_items_tool(resource: str, filter: Optional[str] = None, top: Optional[int] = None, skip: Optional[int] = None) -> Dict[str, Any]:
    logger.info(f"Tool 'BC_List_Items' called for resource={resource}")
    params = {k: v for k, v in {'$filter': filter, '$top': top, '$skip': skip}.items() if v is not None}
    result = await bc_request("GET", resource, params=params)
    return create_response(result)

@mcp.tool(name="BC_Get_Items_By_Field", description="Get items matching a field value.")
async def get_items_by_field_tool(resource: str, field: str, value: str) -> Dict[str, Any]:
    logger.info(f"Tool 'BC_Get_Items_By_Field' called for resource={resource}, field={field}")
    return await list_items_tool(resource, filter=f"{field} eq '{value}'")

@mcp.tool(name="BC_Create_Item", description="Create a new item in Business Central.")
async def create_item_tool(resource: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f"Tool 'BC_Create_Item' called for resource={resource}")
    result = await bc_request("POST", resource, data=item_data)
    return create_response(result)

@mcp.tool(name="BC_Update_Item", description="Update an existing item in Business Central.")
async def update_item_tool(resource: str, item_id: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
    logger.info(f"Tool 'BC_Update_Item' called for resource={resource}, item_id={item_id}")
    result = await bc_request("PATCH", resource, item_id=item_id, data=item_data)
    if "error" in result:
        return {"error": result["error"], "success": False}
    return {"success": True, "item_id": item_id}

@mcp.tool(name="BC_Delete_Item", description="Delete an item from Business Central.")
async def delete_item_tool(resource: str, item_id: str) -> Dict[str, Any]:
    logger.info(f"Tool 'BC_Delete_Item' called for resource={resource}, item_id={item_id}")
    result = await bc_request("DELETE", resource, item_id=item_id)
    if "error" in result:
        return {"error": result["error"], "success": False}
    return {"success": True, "item_id": item_id}