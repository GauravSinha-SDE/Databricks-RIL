"""Example runtime secret lookup: never print or persist the returned value."""

dbutils.widgets.text("scope", "")
dbutils.widgets.text("key", "")
scope = dbutils.widgets.get("scope")
key = dbutils.widgets.get("key")
token = dbutils.secrets.get(scope=scope, key=key)
print(f"Secret reference resolved (length={len(token)}); value not logged.")

