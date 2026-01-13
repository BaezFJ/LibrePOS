#!/usr/bin/env python3
"""
Blueprint generator for LibrePOS.

Creates a new Flask blueprint with full boilerplate code including:
- Routes, models, services, schemas, forms, permissions
- Auto-registration with the app factory
- Template and static directories

Usage:
    python scripts/create_blueprint.py # Interactive mode
    python scripts/create_blueprint.py orders # With name
    python scripts/create_blueprint.py orders --prefix /orders --desc "Order management"
    python scripts/create_blueprint.py orders --skip schemas --skip services
"""

import re
import sys
from pathlib import Path

import click

# Base paths
PROJECT_ROOT = Path(__file__).parent.parent
BLUEPRINTS_DIR = PROJECT_ROOT / "librepos" / "app" / "blueprints"
BLUEPRINTS_INIT = BLUEPRINTS_DIR / "__init__.py"
APP_INIT = PROJECT_ROOT / "librepos" / "app" / "__init__.py"


# =============================================================================
# Template definitions
# =============================================================================


def get_init_template(name: str, prefix: str, description: str) -> str:
    """Generate __init__.py template."""
    return f'''"""
{description}
"""
from flask import Blueprint

bp = Blueprint(
    "{name}",
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix="{prefix}",
)

from . import routes  # noqa: E402, F401
'''


def get_routes_template(name: str, _description: str) -> str:
    """Generate routes.py template."""
    return f'''"""Route handlers for {name} blueprint."""
from flask import render_template

from . import bp


@bp.route("/")
def index():
    """List view for {name}."""
    return render_template("{name}/index.html")


@bp.route("/<int:id>")
def detail(id: int):
    """Detail view for a single {name} item."""
    return render_template("{name}/detail.html", id=id)
'''


def get_models_template(name: str, pascal_name: str) -> str:
    """Generate models.py template."""
    return f'''"""SQLAlchemy models for {name} blueprint."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from librepos.app.extensions import db


# Example model - customize as needed
# class {pascal_name}(db.Model):
#     """Model for {name}."""
#
#     __tablename__ = "{name}"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(String(100), nullable=False)
#
#     def __repr__(self) -> str:
#         return f"<{pascal_name} {{self.id}}: {{self.name}}>"
'''


def get_services_template(name: str, pascal_name: str) -> str:
    """Generate services.py template."""
    return f'''"""Business logic for {name} blueprint."""
from librepos.app.extensions import db


class {pascal_name}Service:
    """Service class for {name} operations."""

    @staticmethod
    def get_all():
        """Retrieve all records."""
        pass

    @staticmethod
    def get_by_id(id: int):
        """Retrieve a record by ID."""
        pass

    @staticmethod
    def create(data: dict):
        """Create a new record."""
        pass

    @staticmethod
    def update(id: int, data: dict):
        """Update an existing record."""
        pass

    @staticmethod
    def delete(id: int):
        """Delete a record."""
        pass
'''


def get_schemas_template(name: str, pascal_name: str) -> str:
    """Generate schemas.py template."""
    return f'''"""Marshmallow schemas for {name} blueprint."""
from marshmallow import Schema, fields


class {pascal_name}Schema(Schema):
    """Schema for serializing {name} data."""

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # Add your fields here
    # name = fields.Str(required=True, validate=validate.Length(min=1, max=100))


# Schema instances
{name}_schema = {pascal_name}Schema()
{name}s_schema = {pascal_name}Schema(many=True)
'''


def get_forms_template(name: str, pascal_name: str) -> str:
    """Generate forms.py template."""
    return f'''"""WTForms for {name} blueprint."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class {pascal_name}Form(FlaskForm):
    """Form for creating/editing {name}."""

    # Add your form fields here
    # name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    submit = SubmitField("Submit")
'''


def get_permissions_template(name: str, pascal_name: str, upper_name: str) -> str:
    """Generate permissions.py template."""
    return f'''"""Permission definitions for {name} blueprint."""
from enum import StrEnum


class {pascal_name}Permissions(StrEnum):
    """Permissions for {name} functionality."""

    VIEW = "view:{name}"
    CREATE = "create:{name}"
    EDIT = "edit:{name}"
    DELETE = "delete:{name}"


# Policy definitions can be added here when the permissions system is set up
# {upper_name}_FULL_ACCESS = PolicyDefinition(
#     name="{pascal_name} Full Access",
#     description="Complete access to {name} functionality",
#     permissions=list({pascal_name}Permissions),
#     is_system=True,
# )
#
# DEFAULT_POLICIES = [{upper_name}_FULL_ACCESS]
'''


def get_index_template(name: str, pascal_name: str) -> str:
    """Generate index.html template."""
    return f"""{{% extends "layouts/admin.html" %}}

{{% block title %}}{pascal_name} - LibrePOS{{% endblock %}}

{{% block content %}}
<div class="container">
    <h4>{pascal_name}</h4>
    <p>Welcome to the {name} section.</p>
</div>
{{% endblock %}}
"""


# =============================================================================
# Helper functions
# =============================================================================


def to_pascal_case(name: str) -> str:
    """Convert snake_case to PascalCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def validate_name(name: str) -> bool:
    """Validate blueprint name (lowercase, starts with letter, alphanumeric + underscore)."""
    return bool(re.match(r"^[a-z][a-z0-9_]*$", name))


def validate_prefix(prefix: str) -> bool:
    """Validate URL prefix (must start with /)."""
    return prefix.startswith("/")


def blueprint_exists(name: str) -> bool:
    """Check if a blueprint with this name already exists."""
    return (BLUEPRINTS_DIR / name).exists()


# =============================================================================
# Auto-registration functions
# =============================================================================


def setup_blueprints_init():
    """Ensure blueprints/__init__.py has a register_blueprints function."""
    if not BLUEPRINTS_INIT.exists():
        BLUEPRINTS_INIT.parent.mkdir(parents=True, exist_ok=True)
        BLUEPRINTS_INIT.write_text(
            '''"""Blueprint registration for LibrePOS."""


def register_blueprints(app):
    """Register all blueprints with the application."""
    pass  # Blueprints will be registered here
'''
        )
        return

    content = BLUEPRINTS_INIT.read_text()
    if "def register_blueprints" not in content:
        # Add the function if it doesn't exist
        content = (
            content.rstrip()
            + '''


def register_blueprints(app):
    """Register all blueprints with the application."""
    pass  # Blueprints will be registered here
'''
        )
        BLUEPRINTS_INIT.write_text(content)


def register_blueprint_in_init(name: str):
    """Add blueprint import and registration to blueprints/__init__.py."""
    setup_blueprints_init()
    content = BLUEPRINTS_INIT.read_text()

    # Check if already registered
    import_line = f"from .{name} import bp as {name}_bp"
    register_line = f"app.register_blueprint({name}_bp)"

    if import_line in content:
        click.echo(f"  Blueprint '{name}' already imported in blueprints/__init__.py")
        return

    # Find the register_blueprints function and add registration
    lines = content.split("\n")
    new_lines = []
    in_function = False
    added_import = False
    added_register = False

    for line in lines:
        # Add import at the top (after docstring)
        if not added_import and line.startswith("def register_blueprints"):
            # Insert import before function definition
            new_lines.append(import_line)
            new_lines.append("")
            added_import = True

        new_lines.append(line)

        # Track when we're inside register_blueprints
        if "def register_blueprints" in line:
            in_function = True

        # Add registration inside the function
        if in_function and not added_register:
            # Look for the pass statement or existing registrations
            if line.strip() == "pass  # Blueprints will be registered here":
                # Replace pass with our registration
                new_lines[-1] = f"    {register_line}"
                added_register = True
            elif line.strip().startswith("app.register_blueprint("):
                # Add after existing registrations
                pass  # Will add at the end

    # If we haven't added the registration yet, add it at the end of the function
    if not added_register:
        # Find the function and add at the end
        final_lines = []
        in_func = False
        for i, line in enumerate(new_lines):
            final_lines.append(line)
            if "def register_blueprints" in line:
                in_func = True
            if (
                in_func
                and (
                    i + 1 >= len(new_lines)
                    or (
                        new_lines[i + 1]
                        and not new_lines[i + 1].startswith(" ")
                        and new_lines[i + 1].strip()
                    )
                )
                and line.strip()
                and not line.strip().startswith("#")
            ):
                final_lines.append(f"    {register_line}")
                in_func = False
        new_lines = final_lines

    BLUEPRINTS_INIT.write_text("\n".join(new_lines))
    click.echo("  Added blueprint registration to blueprints/__init__.py")


def ensure_app_calls_register():
    """Ensure app/__init__.py calls register_blueprints."""
    content = APP_INIT.read_text()

    # Check if already calling register_blueprints
    if "register_blueprints(app)" in content:
        return

    # Add import if needed
    import_line = "from librepos.app.blueprints import register_blueprints"
    if import_line not in content:
        # Add after other imports from librepos.app
        lines = content.split("\n")
        new_lines = []
        added = False
        for line in lines:
            new_lines.append(line)
            if not added and line.startswith("from librepos.app."):
                new_lines.append(import_line)
                added = True
        if not added:
            # Add after first import block
            for i, line in enumerate(lines):
                if line.startswith(("from ", "import ")):
                    continue
                if line.strip() == "":
                    continue
                new_lines.insert(i, import_line)
                new_lines.insert(i + 1, "")
                break
        content = "\n".join(new_lines)

    # Add call before return app
    if "register_blueprints(app)" not in content:
        content = content.replace(
            "return app", "# Register blueprints\n    register_blueprints(app)\n\n    return app"
        )

    APP_INIT.write_text(content)
    click.echo("  Updated app/__init__.py to call register_blueprints()")


# =============================================================================
# Main CLI
# =============================================================================


@click.command()
@click.argument("name", required=False)
@click.option("--prefix", "-p", help="URL prefix (default: /{name})")
@click.option("--desc", "-d", help="Blueprint description")
@click.option(
    "--skip",
    "-s",
    multiple=True,
    type=click.Choice(["routes", "models", "services", "schemas", "forms", "permissions"]),
    help="Files to skip generating",
)
@click.option("--no-register", is_flag=True, help="Skip auto-registration with app factory")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
def main(name, prefix, desc, skip, no_register, yes):  # noqa: PLR0915
    """Create a new Flask blueprint with full boilerplate.

    NAME is the blueprint name (lowercase, snake_case).
    """
    click.echo()
    click.echo("=" * 50)
    click.echo("  LibrePOS Blueprint Generator")
    click.echo("=" * 50)
    click.echo()

    # Interactive mode for name
    if not name:
        name = click.prompt("Blueprint name (lowercase, snake_case)", type=str)

    # Validate name
    if not validate_name(name):
        click.echo(
            click.style(
                "Error: Blueprint name must be lowercase, start with a letter, "
                "and contain only letters, numbers, and underscores.",
                fg="red",
            )
        )
        sys.exit(1)

    # Check if exists
    if blueprint_exists(name):
        click.echo(click.style(f"Error: Blueprint '{name}' already exists.", fg="red"))
        sys.exit(1)

    # Interactive mode for prefix
    if not prefix:
        default_prefix = f"/{name}"
        prefix = click.prompt("URL prefix", default=default_prefix)

    if not validate_prefix(prefix):
        click.echo(click.style("Error: URL prefix must start with /", fg="red"))
        sys.exit(1)

    # Interactive mode for description
    if not desc:
        desc = click.prompt("Description", default=f"{to_pascal_case(name)} management")

    # Interactive mode for files to generate
    all_files = ["routes", "models", "services", "schemas", "forms", "permissions"]
    if not skip and not yes:
        click.echo()
        click.echo("Select files to generate (press Enter to select all):")
        selected = [f for f in all_files if click.confirm(f"  Generate {f}.py?", default=True)]
        skip = [f for f in all_files if f not in selected]

    files_to_generate = [f for f in all_files if f not in skip]

    # Show summary
    click.echo()
    click.echo("-" * 50)
    click.echo("Summary:")
    click.echo(f"  Name:        {name}")
    click.echo(f"  Prefix:      {prefix}")
    click.echo(f"  Description: {desc}")
    click.echo(f"  Files:       {', '.join(files_to_generate) or 'none'}")
    click.echo(f"  Auto-register: {'No' if no_register else 'Yes'}")
    click.echo(f"  Location:    {BLUEPRINTS_DIR / name}")
    click.echo("-" * 50)

    # Confirm
    if not yes and not click.confirm("\nProceed with creation?", default=True):
        click.echo("Cancelled.")
        sys.exit(0)

    click.echo()

    # Create blueprint
    pascal_name = to_pascal_case(name)
    upper_name = name.upper()
    bp_dir = BLUEPRINTS_DIR / name

    # Create directories
    click.echo("Creating directories...")
    bp_dir.mkdir(parents=True, exist_ok=True)
    (bp_dir / "static" / "css").mkdir(parents=True, exist_ok=True)
    (bp_dir / "static" / "js").mkdir(parents=True, exist_ok=True)
    (bp_dir / "templates" / name).mkdir(parents=True, exist_ok=True)

    # Create __init__.py (always created)
    click.echo("Creating files...")
    (bp_dir / "__init__.py").write_text(get_init_template(name, prefix, desc))
    click.echo(f"  Created {name}/__init__.py")

    # Create selected files
    templates = {
        "routes": lambda: get_routes_template(name, desc),
        "models": lambda: get_models_template(name, pascal_name),
        "services": lambda: get_services_template(name, pascal_name),
        "schemas": lambda: get_schemas_template(name, pascal_name),
        "forms": lambda: get_forms_template(name, pascal_name),
        "permissions": lambda: get_permissions_template(name, pascal_name, upper_name),
    }

    for file_type in files_to_generate:
        file_path = bp_dir / f"{file_type}.py"
        file_path.write_text(templates[file_type]())
        click.echo(f"  Created {name}/{file_type}.py")

    # Create index template
    index_template = bp_dir / "templates" / name / "index.html"
    index_template.write_text(get_index_template(name, pascal_name))
    click.echo(f"  Created {name}/templates/{name}/index.html")

    # Create .gitkeep files
    (bp_dir / "static" / "css" / ".gitkeep").touch()
    (bp_dir / "static" / "js" / ".gitkeep").touch()

    # Auto-registration
    if not no_register:
        click.echo()
        click.echo("Registering blueprint...")
        register_blueprint_in_init(name)
        ensure_app_calls_register()

    click.echo()
    click.echo(click.style(f"Blueprint '{name}' created successfully!", fg="green"))
    click.echo()
    click.echo("Next steps:")
    click.echo(f"  1. Edit {bp_dir / 'models.py'} to define your models")
    click.echo(f"  2. Run 'flask db migrate -m \"Add {name} models\"'")
    click.echo("  3. Run 'flask db upgrade'")
    click.echo(f"  4. Visit {prefix}/ to test your blueprint")
    click.echo()


if __name__ == "__main__":
    main()
