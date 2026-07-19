from flask import Blueprint, render_template, request, redirect
from datetime import datetime

from models import (
    get_all_leads,
    add_lead,
    add_followup,
    get_all_followups,
    total_leads,
    pending_leads,
    admissions,
    get_lead_by_id,
    update_lead,
    delete_lead as delete_lead_db,
    get_followup_by_id,
    update_followup,
    delete_followup,
    update_followup_status
)

main = Blueprint("main", __name__)


# -----------------------------
# Home Page
# -----------------------------
@main.route("/")
def home():

    leads = get_all_leads()

    return render_template(
        "leads.html",
        leads=leads
    )


# -----------------------------
# All Leads
# -----------------------------
@main.route("/leads")
def leads():

    data = get_all_leads()

    return render_template(
        "leads.html",
        leads=data
    )


# -----------------------------
# Add Lead
# -----------------------------
@main.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        course = request.form["course"]
        city = request.form["city"]
        source = request.form["source"]

        add_lead(
            name=name,
            mobile=mobile,
            email=email,
            course=course,
            city=city,
            source=source,
            status="New Enquiry",
            counsellor="Not Assigned",
            created_date=datetime.now().strftime("%d-%m-%Y %H:%M")
        )

        return redirect("/")

    return render_template("add_lead.html")


# -----------------------------
# Follow-up
# -----------------------------
@main.route("/followup", methods=["GET", "POST"])
def followup():

    if request.method == "POST":

        add_followup(

            request.form["lead_id"],
            request.form["followup_date"],
            request.form["followup_time"],
            request.form["remarks"],
            request.form["status"],
            "Counsellor"

        )

        return redirect("/followups")

    leads = get_all_leads()

    return render_template(
        "add_followup.html",
        leads=leads
    )


# -----------------------------
# Dashboard
# -----------------------------
@main.route("/dashboard")
def dashboard():

    return render_template(
        "dashboard.html",
        total_leads=total_leads(),
        today_followups=0,
        missed_followups=0,
        admissions=admissions(),
        pending_leads=pending_leads(),
        total_calls=0
    )


# -----------------------------
# Search Lead
# -----------------------------
@main.route("/search", methods=["GET"])
def search():

    keyword = request.args.get("keyword", "").lower()

    leads = get_all_leads()

    result = []

    for lead in leads:

        if (
            keyword in str(lead["name"]).lower()
            or keyword in str(lead["mobile"]).lower()
            or keyword in str(lead["course"]).lower()
        ):
            result.append(lead)

    return render_template(
        "leads.html",
        leads=result
    )


# -----------------------------
# Assign Counsellor
# -----------------------------
@main.route("/assign/<int:lead_id>")
def assign(lead_id):

    # Future Implementation

    return redirect("/")


# -----------------------------
# Update Lead Status
# -----------------------------
@main.route("/status/<int:lead_id>")
def update_status_route(lead_id):

    # Future Implementation

    return redirect("/")


# -----------------------------
# Edit Lead
# -----------------------------
@main.route("/edit/<int:lead_id>", methods=["GET", "POST"])
def edit_lead(lead_id):

    lead = get_lead_by_id(lead_id)

    if request.method == "POST":

        update_lead(

            lead_id,

            request.form["name"],
            request.form["mobile"],
            request.form["email"],
            request.form["course"],
            request.form["city"],
            request.form["source"],
            request.form["status"],
            request.form["counsellor"]

        )

        return redirect("/leads")

    return render_template(
        "edit_lead.html",
        lead=lead
    )

# -----------------------------
# Delete Lead
# -----------------------------
@main.route("/delete/<int:lead_id>")
def delete(lead_id):

    print("Deleting:", lead_id)

    delete_lead_db(lead_id)

    print("Deleted Successfully")

    return redirect("/leads")

# -----------------------------
# Follow-up List
# -----------------------------
@main.route("/followups")
def followups():

    data = get_all_followups()

    return render_template(
        "followups.html",
        followups=data
    )


@main.route("/edit_followup/<int:id>", methods=["GET","POST"])
def edit_followup(id):

    followup = get_followup_by_id(id)

    if request.method == "POST":

        update_followup(

            id,

            request.form["followup_date"],
            request.form["followup_time"],
            request.form["remarks"],
            request.form["status"]

        )

        return redirect("/followups")

    return render_template(
        "edit_followup.html",
        followup=followup
    )


@main.route("/delete_followup/<int:id>")
def delete_followup_route(id):

    delete_followup(id)

    return redirect("/followups")

@main.route("/update_followup_status/<int:id>", methods=["POST"])
def update_followup_status_route(id):

    status = request.form["status"]

    update_followup_status(
        id,
        status
    )

    return redirect("/followups")