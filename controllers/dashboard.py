from flask import Blueprint, render_template, redirect

from controllers.auth import login_required

from services.permission_service import permission_required


dashboard_routes = Blueprint(
    'dashboard',
    __name__
)

@dashboard_routes.route('/tableau-bord')
@login_required
@permission_required("ACCESS_DASHBOARD")
def tableau_bord_graphique():

    return redirect("/ecritures/dashboard-financier")

@dashboard_routes.route('/dashboard-temps-reel')
@login_required
@permission_required("ACCESS_DASHBOARD")
def dashboard_temps_reel():
    return redirect('/ecritures/tableau-bord')


@dashboard_routes.route('/dashboard-complet')
@login_required
@permission_required("ACCESS_DASHBOARD")
def dashboard_complet():
    return redirect('/ecritures/tableau-bord')


@dashboard_routes.route('/dashboard-pro')
@login_required
@permission_required("ACCESS_DASHBOARD")
def page_dashboard_pro():
    return redirect('/ecritures/tableau-bord')

