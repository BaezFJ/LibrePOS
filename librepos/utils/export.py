"""CSV export utilities for LibrePOS."""

import csv
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from io import StringIO
from typing import Any

from flask import Response


@dataclass
class ExportField:
    """Defines a single column in a CSV export.

    Attributes:
        header: Column header name in the CSV
        getter: Function that extracts/formats the value from an item

    Example:
        ExportField("Username", lambda u: u.username)
        ExportField("Status", lambda u: u.status.value.title())
    """

    header: str
    getter: Callable[[Any], str]


def export_to_csv(
    items: Sequence[Any],
    fields: list[ExportField],
    filename_prefix: str = "export",
) -> Response:
    """Export a sequence of items to CSV.

    Args:
        items: Sequence of objects to export
        fields: List of ExportField definitions specifying columns
        filename_prefix: Prefix for the downloaded filename

    Returns:
        Flask Response with CSV as a downloadable file

    Example:
        fields = [
            ExportField("Name", lambda u: u.name),
            ExportField("Email", lambda u: u.email),
        ]
        return export_to_csv(users, fields, "users_export")
    """
    output = StringIO()
    writer = csv.writer(output)

    # Write headers
    writer.writerow([f.header for f in fields])

    # Write data rows
    for item in items:
        writer.writerow([f.getter(item) for f in fields])

    filename = f"{filename_prefix}_{datetime.now().strftime('%Y%m%d')}.csv"

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )
