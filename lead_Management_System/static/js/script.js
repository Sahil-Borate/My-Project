// ===============================
// Lead Management System
// script.js
// ===============================

// -------------------------------
// Confirm Delete
// -------------------------------
function confirmDelete() {

    return confirm("Are you sure you want to delete this lead?");
}


// -------------------------------
// Search Leads
// -------------------------------
function searchLead() {

    let input = document.getElementById("searchInput");

    if (!input) return;

    let filter = input.value.toUpperCase();

    let table = document.getElementById("leadTable");

    if (!table) return;

    let tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {

        let td = tr[i].getElementsByTagName("td");

        let found = false;

        for (let j = 0; j < td.length; j++) {

            if (td[j]) {

                let txt = td[j].textContent || td[j].innerText;

                if (txt.toUpperCase().indexOf(filter) > -1) {

                    found = true;
                }

            }

        }

        tr[i].style.display = found ? "" : "none";

    }

}


// -------------------------------
// Lead Form Validation
// -------------------------------
function validateLeadForm() {

    let name = document.getElementById("name").value.trim();

    let mobile = document.getElementById("mobile").value.trim();

    let email = document.getElementById("email").value.trim();

    if (name === "") {

        alert("Enter Student Name");

        return false;

    }

    if (!/^[0-9]{10}$/.test(mobile)) {

        alert("Enter Valid 10 Digit Mobile Number");

        return false;

    }

    if (email !== "") {

        let pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!pattern.test(email)) {

            alert("Invalid Email Address");

            return false;

        }

    }

    return true;

}


// -------------------------------
// Follow-up Date Validation
// -------------------------------
function validateFollowup() {

    let date = document.getElementById("followup_date");

    if (!date) return true;

    let selected = new Date(date.value);

    let today = new Date();

    today.setHours(0,0,0,0);

    if (selected < today) {

        alert("Follow-up date cannot be in the past.");

        return false;

    }

    return true;

}


// -------------------------------
// Auto Hide Alerts
// -------------------------------
setTimeout(function () {

    let alertBox = document.querySelector(".alert");

    if (alertBox) {

        alertBox.style.display = "none";

    }

}, 3000);


// -------------------------------
// Dashboard Card Hover Effect
// -------------------------------
document.addEventListener("DOMContentLoaded", function () {

    let cards = document.querySelectorAll(".card");

    cards.forEach(function(card){

        card.addEventListener("mouseover", function(){

            card.style.transform = "scale(1.03)";

        });

        card.addEventListener("mouseout", function(){

            card.style.transform = "scale(1)";

        });

    });

});


// -------------------------------
// Current Date & Time
// -------------------------------
function showDateTime() {

    let box = document.getElementById("datetime");

    if (!box) return;

    let now = new Date();

    box.innerHTML = now.toLocaleString();

}

setInterval(showDateTime,1000);


// -------------------------------
// Reset Form
// -------------------------------
function resetForm(id){

    document.getElementById(id).reset();

}


// -------------------------------
// Success Message
// -------------------------------
function successMessage(msg){

    alert(msg);

}