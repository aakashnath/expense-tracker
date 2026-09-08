/* ================= THEME TOGGLE ================= */

function toggleTheme() {

    document.body.classList.toggle("dark");

    const isDark =
        document.body.classList.contains("dark");

    localStorage.setItem(
        "expenseTheme",
        isDark ? "dark" : "light"
    );

    updateThemeIcon();
}


/* ================= THEME ICON ================= */

function updateThemeIcon() {

    const icon =
        document.getElementById("themeIcon");

    const isDark =
        document.body.classList.contains("dark");


    if (isDark) {

        icon.innerHTML = `
            <path
                d="M21 12.8A8.5 8.5 0 1 1 11.2 3
                6.5 6.5 0 0 0 21 12.8Z">
            </path>
        `;

    } else {

        icon.innerHTML = `
            <circle
                cx="12"
                cy="12"
                r="4">
            </circle>

            <path d="M12 2v2"></path>
            <path d="M12 20v2"></path>

            <path
                d="m4.93 4.93 1.41 1.41">
            </path>

            <path
                d="m17.66 17.66 1.41 1.41">
            </path>

            <path d="M2 12h2"></path>
            <path d="M20 12h2"></path>

            <path
                d="m6.34 17.66-1.41 1.41">
            </path>

            <path
                d="m19.07 4.93-1.41 1.41">
            </path>
        `;
    }
}


/* ================= PAGE LOAD ================= */

window.addEventListener(
    "DOMContentLoaded",
    function () {

        /* Load saved theme */

        const savedTheme =
            localStorage.getItem("expenseTheme");

        if (savedTheme === "dark") {

            document.body.classList.add("dark");
        }


        updateThemeIcon();


        /* Set today's date automatically */

        const dateInput =
            document.getElementById("expenseDate");

        if (dateInput && !dateInput.value) {

            const today =
                new Date()
                    .toISOString()
                    .split("T")[0];

            dateInput.value = today;
        }

    }
);