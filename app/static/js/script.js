document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    if (form) {
        form.addEventListener("submit", function (event) {
            const chest = document.getElementById("chest");
            const waist = document.getElementById("waist");
            const inseam = document.getElementById("inseam");

            if (!chest.value || !waist.value || !inseam.value) {
                event.preventDefault();
                alert("Please fill in all measurement fields before submitting.");
            }
        });
    }
});
