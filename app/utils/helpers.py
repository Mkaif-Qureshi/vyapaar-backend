def format_response(success: bool, message: str, data=None):
    """
    Helper function to format API responses.
    """
    return {"success": success, "message": message, "data": data}
