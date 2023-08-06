import _sqlite_access

x = _sqlite_access.SqlServerAccess().get_usage_stats()

print(x)