const form = document.getElementById("studentForm");
const tableBody = document.getElementById("studentTableBody");
const emptyState = document.getElementById("emptyState");
const searchInput = document.getElementById("searchInput");
const formMessage = document.getElementById("formMessage");
const statusMessage = document.getElementById("statusMessage");
const studentCount = document.getElementById("studentCount");
const cancelButton = document.getElementById("cancelButton");

let searchTimer;

function showMessage(element, message, isError = false) {
    element.textContent = message;
    element.classList.toggle("error", isError);
}

async function requestJson(url, options = {}) {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json" },
        ...options,
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Something went wrong.");
    return data;
}

async function loadStudents(search = "") {
    try {
        const students = await requestJson(`/api/students?search=${encodeURIComponent(search)}`);
        renderStudents(students);
    } catch (error) {
        showMessage(statusMessage, error.message, true);
    }
}

function renderStudents(students) {
    studentCount.textContent = students.length;
    tableBody.innerHTML = students.map((student) => `
        <tr>
            <td>${escapeHtml(student.name)}<span class="student-email">${escapeHtml(student.email)}</span></td>
            <td>${escapeHtml(student.register_number)}</td>
            <td>${escapeHtml(student.department)}</td>
            <td>Year ${student.year}</td>
            <td><div class="actions">
                <button class="icon-button" title="Edit student" aria-label="Edit ${escapeHtml(student.name)}" onclick="editStudent(${student.id})">✎</button>
                <button class="icon-button delete-button" title="Delete student" aria-label="Delete ${escapeHtml(student.name)}" onclick="deleteStudent(${student.id})">×</button>
            </div></td>
        </tr>
    `).join("");
    emptyState.classList.toggle("hidden", students.length > 0);
}

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, (character) => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
    }[character]));
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    showMessage(formMessage, "");
    const studentId = document.getElementById("studentId").value;
    const payload = Object.fromEntries(new FormData(form).entries());

    try {
        await requestJson(studentId ? `/api/students/${studentId}` : "/api/students", {
            method: studentId ? "PUT" : "POST",
            body: JSON.stringify(payload),
        });
        resetForm();
        showMessage(statusMessage, studentId ? "Student updated successfully." : "Student added successfully.");
        await loadStudents(searchInput.value);
    } catch (error) {
        showMessage(formMessage, error.message, true);
    }
});

async function editStudent(id) {
    try {
        const student = await requestJson(`/api/students/${id}`);
        document.getElementById("studentId").value = student.id;
        document.getElementById("name").value = student.name;
        document.getElementById("register_number").value = student.register_number;
        document.getElementById("email").value = student.email;
        document.getElementById("department").value = student.department;
        document.getElementById("year").value = student.year;
        document.getElementById("formTitle").textContent = "Edit student";
        document.getElementById("submitButton").innerHTML = "Update student <span>↗</span>";
        cancelButton.classList.remove("hidden");
        window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (error) {
        showMessage(statusMessage, error.message, true);
    }
}

async function deleteStudent(id) {
    if (!window.confirm("Delete this student record?")) return;
    try {
        await requestJson(`/api/students/${id}`, { method: "DELETE" });
        showMessage(statusMessage, "Student deleted successfully.");
        await loadStudents(searchInput.value);
    } catch (error) {
        showMessage(statusMessage, error.message, true);
    }
}

function resetForm() {
    form.reset();
    document.getElementById("studentId").value = "";
    document.getElementById("formTitle").textContent = "Add a student";
    document.getElementById("submitButton").innerHTML = "Save student <span>↗</span>";
    cancelButton.classList.add("hidden");
    showMessage(formMessage, "");
}

cancelButton.addEventListener("click", resetForm);
searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => loadStudents(searchInput.value), 250);
});

loadStudents();
