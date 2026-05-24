from repositories.notifications.notifications_repository import (
    create_notification,
    list_notifications,
    mark_notification_as_read,
    count_unread_notifications
)

from services_v3.alerts.alerts_service import (
    get_alerts_center
)

from services_v3.history.history_service import (
    log_action
)


def get_notifications_center():

    notifications = list_notifications()

    return {
        "count": len(notifications),
        "unread_count": count_unread_notifications(),
        "items": notifications
    }


def notify_from_alerts():

    alerts = get_alerts_center().get("items", [])

    created = []

    for alert in alerts:

        notification_id = create_notification(
            {
                "societe_id": alert.get("societe_id"),
                "type_notification": alert.get("type"),
                "niveau": alert.get("level"),
                "titre": alert.get("title"),
                "message": alert.get("message"),
                "reference_type": alert.get("type"),
                "reference_id": alert.get("reference_id")
            }
        )

        log_action(
            module="notifications",
            action="creation_notification_depuis_alerte",
            statut="ok",
            societe_id=alert.get("societe_id"),
            reference_type="notification",
            reference_id=notification_id,
            message="Notification créée depuis une alerte",
            metadata={
                "alerte_type": alert.get("type"),
                "alerte_reference_id": alert.get("reference_id")
            }
        )

        created.append(notification_id)

    return {
        "success": True,
        "created_count": len(created),
        "notification_ids": created,
        "message": "Notifications générées depuis les alertes"
    }


def read_notification(notification_id):

    mark_notification_as_read(notification_id)

    log_action(
        module="notifications",
        action="lecture_notification",
        statut="ok",
        reference_type="notification",
        reference_id=notification_id,
        message="Notification marquée comme lue"
    )

    return {
        "success": True,
        "notification_id": notification_id,
        "message": "Notification marquée comme lue"
    }
