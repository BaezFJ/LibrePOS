"""Business logic for menu blueprint."""

from sqlalchemy import or_

from librepos.app.extensions import db
from librepos.app.shared.images import delete_category_image, process_category_image

from .models import Category


class CategoryService:
    """Service class for category operations."""

    @staticmethod
    def get_parent_choices():
        """Return choices for parent category dropdown."""
        categories = Category.query.order_by(Category.name).all()
        return [(0, "None (Top Level)")] + [(c.id, c.name) for c in categories]

    @staticmethod
    def create(data: dict, image_file=None, static_folder: str | None = None):
        """Create a new category from dict data."""
        image_url = None
        if image_file and static_folder:
            image_url = process_category_image(image_file, static_folder)

        return Category.create(
            name=data["name"],
            description=data.get("description"),
            parent_id=data.get("parent_id") or None,
            display_order=data.get("display_order", 0),
            is_active=data.get("is_active", True),
            image_url=image_url,
        )

    @staticmethod
    def get_filtered_query(status="all", type_filter="all", sort_by="name", search=""):
        """Build and return filtered/sorted query for categories."""
        query = Category.query

        if search:
            query = query.filter(
                or_(
                    Category.name.ilike(f"%{search}%"),
                    Category.description.ilike(f"%{search}%"),
                )
            )

        if status == "active":
            query = query.filter(Category.is_active == True)  # noqa: E712
        elif status == "inactive":
            query = query.filter(Category.is_active == False)  # noqa: E712

        if type_filter == "top-level":
            query = query.filter(Category.parent_id == None)  # noqa: E711
        elif type_filter == "subcategory":
            query = query.filter(Category.parent_id != None)  # noqa: E711

        # Apply sorting
        if sort_by == "-name":
            query = query.order_by(Category.name.desc())
        elif sort_by == "order":
            query = query.order_by(Category.display_order.asc(), Category.name.asc())
        elif sort_by == "status":
            query = query.order_by(Category.is_active.desc(), Category.name.asc())
        else:  # Default: name ascending
            query = query.order_by(Category.name.asc())

        return query

    @staticmethod
    def get_parent_choices_excluding(exclude_id: int):
        """Return choices for parent category dropdown, excluding the given category and its descendants."""

        def get_descendant_ids(cat_id: int) -> set:
            """Recursively get all descendant category IDs."""
            descendants = set()
            children = Category.query.filter(Category.parent_id == cat_id).all()
            for child in children:
                descendants.add(child.id)
                descendants.update(get_descendant_ids(child.id))
            return descendants

        excluded_ids = {exclude_id} | get_descendant_ids(exclude_id)
        categories = (
            Category.query.filter(
                Category.id.notin_(excluded_ids)  # pyright: ignore[reportAttributeAccessIssue]
            )
            .order_by(Category.name)
            .all()
        )
        return [(0, "None (Top Level)")] + [(c.id, c.name) for c in categories]

    @staticmethod
    def update(category_id: int, data: dict, image_file=None, static_folder: str | None = None):
        """Update an existing category."""
        category = Category.get_by_id(category_id)
        if not category:
            return None

        # Handle image upload
        if image_file and static_folder:
            # Delete old image if exists
            if category.image_url:
                delete_category_image(category.image_url, static_folder)
            # Save new image
            category.image_url = process_category_image(image_file, static_folder)

        category.name = data["name"]
        category.description = data.get("description")
        category.parent_id = data.get("parent_id") or None
        category.display_order = data.get("display_order", 0)
        category.is_active = data.get("is_active", True)

        db.session.commit()
        return category

    @staticmethod
    def delete(category_id: int):
        """Delete a category. Subcategories become top-level."""
        category = Category.get_by_id(category_id)
        if not category:
            return False

        # Promote children to top-level
        for child in category.children:
            child.parent_id = None

        db.session.delete(category)
        db.session.commit()
        return True
