from config import app
from controller_functions import index, login, dashboard, logout, addint, createint, endintconf, endint, checkinview, checkin

app.add_url_rule("/mtss", view_func=index)
app.add_url_rule("/mtss/login", view_func=login, methods=["POST"])
app.add_url_rule("/mtss/dashboard", view_func=dashboard)
app.add_url_rule("/mtss/logout", view_func=logout)
app.add_url_rule("/mtss/addint", view_func=addint)
app.add_url_rule("/mtss/createint", view_func=createint, methods=["POST"])
app.add_url_rule("/mtss/<int_id>/endintconf", view_func=endintconf)
app.add_url_rule("/mtss/endint", view_func=endint, methods=["POST"])
app.add_url_rule("/mtss/<int_id>/checkin", view_func=checkinview)
app.add_url_rule("/mtss/checkin", view_func=checkin, methods=["POST"])
