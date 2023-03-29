from django import dispatch

row_created = dispatch.Signal()
row_updated = dispatch.Signal()
row_deleted = dispatch.Signal()
