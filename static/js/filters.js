// 🔍 Фильтр по дате (между двумя значениями)
function filterByDate() {
    const from = document.getElementById("from").value;
    const to = document.getElementById("to").value;
    const rows = document.querySelectorAll("table tbody tr");

    rows.forEach(row => {
        const dateCell = row.querySelector("td[data-date]");
        if (!dateCell) return;

        const date = new Date(dateCell.getAttribute("data-date"));
        const from = from ? new Date(from) : null;
        const to = to ? new Date(to) : null;

        let show = true;
        if (from && date < from) show = false;
        if (to && date > to) show = false;

        row.style.display = show ? "" : "none";
    });
}

// 🔎 Поиск по тексту (например, по товару)
function searchTable(inputId, tableId) {
    const input = document.getElementById(inputId).value.toLowerCase();
    const rows = document.querySelectorAll(`#${tableId} tbody tr`);

    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(input) ? "" : "none";
    });
}