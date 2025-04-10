# Business Central MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

A lightweight MCP Server for seamless integration with Microsoft Dynamics 365 Business Central, enabling MCP clients to interact with any entity in your Business Central environment. Developed by [sofias tech](https://github.com/xxx/mcp-business-central-server/).

## Features

This server provides a clean interface to Business Central resources through the Model Context Protocol (MCP), with optimized HTTP request handling for improved performance.

### Tools

The server implements the following tools:

- `BC_Get_Schema`: Retrieves the schema of any Business Central entity including available fields
- `BC_List_Items`: Fetches a list of entities with optional filtering and pagination
- `BC_Get_Items_By_Field`: Searches for entities based on a specific field value
- `BC_Create_Item`: Creates a new entity record in Business Central
- `BC_Update_Item`: Updates an existing entity record
- `BC_Delete_Item`: Removes an entity record from Business Central

## Working with Business Central Entities

This server can work with any entity (table) in Business Central. When using the tools, you must provide the exact entity name as it appears in Business Central. For example:

- `Employees`
- `Customers`
- `Items`
- `Vendors`
- `SalesOrders`
- `Payments`

The entity name is case-sensitive and must match exactly what Business Central exposes through its API.

## Architecture

The server is built with resource efficiency in mind:

- Clear separation between resource management and tool implementation
- Simple and maintainable codebase with minimal code duplication
- Direct HTTP request handling using requests library

## Setup

1. Create API credentials for Business Central
2. Configure your Business Central environment and company information
3. Set up the required environment variables

## Environment Variables

The server requires these environment variables:

- `BC_URL_SERVER`: Your Business Central API server URL (e.g., "https://api.businesscentral.dynamics.com/v2.0/tenant/api/v2.0")
- `BC_USER`: Your Business Central API username
- `BC_PASS`: Your Business Central API password
- `BC_COMPANY`: The name of your Business Central company

## Quickstart

### Installation

```bash
pip install -e .
```

Or install from PyPI once published:

```bash
pip install mcp-business-central-server
```

Using uv:

```bash
uv pip install mcp-business-central-server
```

### Claude Desktop Integration

To integrate with Claude Desktop, update the configuration file:

On Windows: `%APPDATA%/Claude/claude_desktop_config.json`
On macOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`

#### Standard Integration

```json
"mcpServers": {
  "businesscentral": {
    "command": "mcp-business-central-server",
    "env": {
      "BC_URL_SERVER": "your-bc-api-url",
      "BC_USER": "your-bc-username",
      "BC_PASS": "your-bc-password",
      "BC_COMPANY": "your-bc-company"
    }
  }
}
```

#### Using uvx

```json
"mcpServers": {
  "businesscentral": {
    "command": "uvx",
    "args": [
      "mcp-business-central-server"
    ],
    "env": {
      "BC_URL_SERVER": "your-bc-api-url",
      "BC_USER": "your-bc-username",
      "BC_PASS": "your-bc-password",
      "BC_COMPANY": "your-bc-company"
    }
  }
}
```

## Development

### Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt` and `pyproject.toml`

### Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -e .
   ```
4. Create a `.env` file with your Business Central credentials:
   ```
   BC_URL_SERVER=your-bc-api-url
   BC_USER=your-bc-username
   BC_PASS=your-bc-password
   BC_COMPANY=your-bc-company
   ```
5. Run the server:
   ```bash
   python -m mcp_bc_server
   ```

### Debugging

For debugging the MCP server, you can use the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector -- python -m mcp_bc_server
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 sofias tech

