import pytest
@pytest.mark.asyncio
async def test_classify(client):
    r = await client.post("/api/replies", json={"subject": "Re: demo", "body": "Please unsubscribe me from this list"})
    assert r.json()["label"] == "unsubscribe"
