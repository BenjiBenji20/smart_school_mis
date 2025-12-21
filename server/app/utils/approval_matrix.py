"""
    Date Written: 12/21/2025 at 4:49 PM
"""

from app.models.enums.user_state import UserRole

APPROVAL_MATRIX: dict[UserRole, set[UserRole]] = {
    UserRole.ADMINISTRATOR: {
        UserRole.ADMINISTRATOR,
        UserRole.REGISTRAR,
    },
    UserRole.REGISTRAR: {
        UserRole.REGISTRAR,
        UserRole.DEAN,
        UserRole.PROGRAM_CHAIR,
        UserRole.PROFESSOR,
        UserRole.STUDENT,
    },
    UserRole.DEAN: {
        UserRole.PROGRAM_CHAIR,
        UserRole.PROFESSOR,
        UserRole.STUDENT,
    },
    UserRole.PROGRAM_CHAIR: {
        UserRole.PROFESSOR,
        UserRole.STUDENT,
    },
}

def can_approve(approver_role: UserRole, target_role: UserRole) -> bool:
    """
        Check if a user with `approver_role` is allowed to approve `target_role`.
    """
    allowed_roles = APPROVAL_MATRIX.get(approver_role, set())
    return target_role in allowed_roles
