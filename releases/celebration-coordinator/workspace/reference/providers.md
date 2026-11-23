# Grocery integrations — checked 2026-11-10

## Instacart is the declared default, not a connected account
Official Developer Platform MCP: https://mcp.instacart.com/mcp (production), https://mcp.dev.instacart.tools/mcp (development). Its documented tools are create-recipe and create-shopping-list, producing Marketplace recipe/list pages. Discover actual schemas before use; these are not a general checkout/order API.

This template declares a pinned third-party stdio bridge, mcp-remote@0.16.5, because the current portable remote-MCP shape lacks API-key header configuration. The endpoint itself is Instacart-owned; the adapter is not. At Add, review this executable dependency and capability changes. Host setup must supply INSTACART_API_KEY through its supported environment/secret mechanism. The manifest retains only an unresolved reference, including the bridge header placeholder; never interpolate a real key into the archive or command line. The bridge expands the header from its environment. No connection, authentication, tool listing or page creation was tested during packaging.

The filter allows only create-recipe and create-shopping-list. If the server advertises different names, stop and inspect the actual schema; do not silently broaden permissions. Missing key or bridge: explain setup and keep planning locally. Do not install, log in or modify host configuration automatically.

Before a call, confirm approved ingredients, units and servings. Transmit only approved recipe/list fields, not household notes, health explanations, addresses, private guest records or surprise gifts. A list-page title and its contents may be shared with Instacart; obtain the required disclosure approval. Return the provider URL/receipt and label it list created or recipe created. Do not claim cart contents, stock, prices or delivery unless those exact facts were verified. Failed/uncertain writes require reconciliation before a retry, not blind duplicate pages.

The separate OAuth/provisioned Instacart MCP documentation requires a representative for onboarding and permissions; don't confuse that deployment with this API-key Developer Platform endpoint. It is not evidence that any consumer can immediately authenticate by OAuth.

## Kroger alternative
Kroger has official developer APIs. Its full current API contracts and an official Kroger-owned MCP were not verified in this run (the developer site is JS-rendered). Do not label community wrappers official or install one speculatively. A retailer-specific integration can be added after verifying its publisher, OAuth scopes, product/location pricing semantics and cart operations. An API or MCP declaration is not purchase authority. Instacart is the better verified portable starting point; don't claim price parity, all retailer coverage or free access.

Sources: https://docs.instacart.com/developer_platform_api/guide/tutorials/mcp.md ; https://docs.instacart.com/mcp_servers/get-started/use-instacarts-mcp-server.md ; https://docs.instacart.com/developer_platform_api/get_started/api-keys ; https://developer.kroger.com/api-products/ ; https://www.npmjs.com/package/mcp-remote/v/0.16.5 .
