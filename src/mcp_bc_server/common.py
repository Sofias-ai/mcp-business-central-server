import os, logging, requests, base64, asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('mcp-business-central-server.log'), logging.StreamHandler()]
)
logger = logging.getLogger('mcp_bc_server')
load_dotenv()

# Configuration
BC_URL_SERVER = os.getenv('BC_URL_SERVER')
BC_USER = os.getenv('BC_USER')
BC_PASS = os.getenv('BC_PASS')
BC_COMPANY = os.getenv('BC_COMPANY')

# Initialize MCP server
mcp = FastMCP(
    name="mcp-business-central-server",
    instructions=f"This server provides tools to interact with Business Central company {BC_COMPANY}"
)

# Common functions
def get_bc_headers(content_type: bool = False) -> Dict[str, str]:
    """Get standard headers for Business Central API requests"""
    headers = {
        'Accept': 'application/json',
        'Authorization': f"Basic {base64.b64encode(f'{BC_USER}:{BC_PASS}'.encode()).decode()}"
    }
    if content_type: headers['Content-Type'] = 'application/json'
    return headers

def get_bc_url(resource: str, item_id: Optional[str] = None) -> str:
    """Build URL for Business Central API endpoints"""
    base = f"{BC_URL_SERVER}/ODataV4/Company('{BC_COMPANY}')"
    return f"{base}/{resource}({item_id})" if item_id else f"{base}/{resource}"

async def bc_request(method: str, resource: str, item_id: Optional[str] = None, 
                    params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
    """Execute a Business Central API request asynchronously"""
    loop = asyncio.get_running_loop()
    url = get_bc_url(resource, item_id)
    headers = get_bc_headers(content_type=(data is not None))
    
    # For GET requests with item_id, first fetch item to get ETag
    if method in ['PATCH', 'DELETE'] and item_id:
        try:
            get_resp = await loop.run_in_executor(None, 
                lambda: requests.get(url, headers=get_bc_headers(), verify=True))
            get_resp.raise_for_status()
            etag = get_resp.json().get('@odata.etag')
            if etag: headers['If-Match'] = etag
        except Exception as e:
            return {"error": f"Failed to fetch item: {str(e)}"}
    
    try:
        response = await loop.run_in_executor(None, lambda: requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data,
            verify=True
        ))
        response.raise_for_status()
        return response.json() if method != 'DELETE' else {"success": True}
    except Exception as e:
        logger.error(f"API error: {e}")
        return {"error": str(e)}