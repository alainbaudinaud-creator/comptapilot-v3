from repositories.notifications.notifications_repository import (
    create_notification,
    list_notifications,
    mark_notification_as_read,
    count_unread_notifications
)

from services_v3.alerts.alerts_service import (
    get_alerts_center
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

        created.append(notification_id)

    return {
        "success": True,
        "created_count": len(created),
        "notification_ids": created,
        "message": "Notifications générées depuis les alertes"
    }


def read_notification(notification_id):

    mark_notification_as_read(notification_id)

    return {
        "success": True,
        "notification_id": notification_id,
        "message": "Notification marquée comme lue"
    }
