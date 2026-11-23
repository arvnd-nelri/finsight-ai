#!/bin/sh
set -a
. "$HOME/.config/finsight-ai/notion.env"
set +a
exec npx -y @notionhq/notion-mcp-server
