from repositories.security.security_repository import (
    list_roles,
    list_permissions,
    list_role_permissions
)


def get_security_dashboard():

    roles = list_roles()
    permissions = list_permissions()
    role_permissions = list_role_permissions()

    return {
        "roles_count": len(roles),
        "permissions_count": len(permissions),
        "role_permissions_count": len(role_permissions),
        "roles": roles,
        "permissions": permissions,
        "role_permissions": role_permissions
    }
