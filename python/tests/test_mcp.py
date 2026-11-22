import io
import json

from wengua.mcp import handle, serve, spec


def rpc(method, params=None, mid=1):
    return handle({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}})


def test_initialize_negotiates_version():
    r = rpc("initialize", {"protocolVersion": "2025-06-18"})["result"]
    assert r["protocolVersion"] == "2025-06-18"
    assert r["serverInfo"]["name"] == "wengua"
    assert "Never invent" in r["instructions"]
    assert rpc("initialize", {"protocolVersion": "1999-01-01"})["result"]["protocolVersion"] == "2025-11-25"


def test_tools_list_matches_spec():
    names = [t["name"] for t in rpc("tools/list")["result"]["tools"]]
    assert names == ["cast", "read_cast", "lookup", "relations"] == [t["name"] for t in spec()["tools"]]


def test_cast_returns_both_scripts():
    r = rpc("tools/call", {"name": "cast", "arguments": {"question": "q", "method": "yarrow"}})["result"]
    sc = r["structuredContent"]
    assert sc["method"] == "yarrow" and len(sc["values"]) == 6
    t = sc["selection"]["texts"][0]["text"]
    assert t["zh_hant"] and t["zh_hans"]
    assert json.loads(r["content"][0]["text"]) == sc


def test_errors_are_tool_results():
    r = rpc("tools/call", {"name": "read_cast", "arguments": {"lines": [1, 2]}})["result"]
    assert r["isError"] is True
    assert rpc("tools/call", {"name": "lookup", "arguments": {"query": "zzz"}})["result"]["isError"] is True
    assert rpc("nope")["error"]["code"] == -32601


def test_relations_and_resources_and_prompt():
    r = rpc("tools/call", {"name": "relations", "arguments": {"hexagram": "屯", "changing_lines": [1]}})["result"]
    assert r["structuredContent"]["relating"]["number"] == 8  # 比
    assert len(rpc("resources/list")["result"]["resources"]) == 73
    body = json.loads(rpc("resources/read", {"uri": "wengua://hexagram/1"})["result"]["contents"][0]["text"])
    assert body["name"]["zh_hant"] == "乾"
    msg = rpc("prompts/get", {"name": "reading", "arguments": {"question": "my job"}})["result"]["messages"][0]
    assert "my job" in msg["content"]["text"]


def test_stdio_loop_skips_notifications():
    inp = io.StringIO('{"jsonrpc":"2.0","method":"notifications/initialized"}\n{"jsonrpc":"2.0","id":9,"method":"ping"}\nnot json\n')
    out = io.StringIO()
    serve(inp, out)
    lines = [json.loads(x) for x in out.getvalue().splitlines()]
    assert lines[0] == {"jsonrpc": "2.0", "id": 9, "result": {}}
    assert lines[1]["error"]["code"] == -32700


def test_reading_card():
    tools = {t["name"]: t for t in rpc("tools/list")["result"]["tools"]}
    uri = tools["cast"]["_meta"]["ui"]["resourceUri"]
    c = rpc("resources/read", {"uri": uri})["result"]["contents"][0]
    assert c["mimeType"] == "text/html;profile=mcp-app"
    assert "ui/notifications/tool-result" in c["text"]
