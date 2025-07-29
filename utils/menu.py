# utils/menu.py

def get_menu_by_role(role):
    base_menu = {"Home": "🏠 Home"}
    client_menu = {
        "Upload CDR": "📤 Upload CDR",
        "My Billing": "📄 My Billing",
        "Anomalies": "🕵️ Anomalies",
    }
    admin_menu = {
        "Manage Users": "👥 Manage Users",
        "All Billing": "💼 All Billing",
        "Email Reports": "📧 Email Reports",
    }

    if role == "admin":
        return {**base_menu, **admin_menu}
    elif role == "client":
        return {**base_menu, **client_menu}
    else:
        return base_menu
