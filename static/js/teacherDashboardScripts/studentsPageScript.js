
 
// TO HANDLE CREATION OF A NEW STUDENT FROM TEACHER DASHBOARD 
 
function openStudentModal() {
    document.getElementById("addStudentModal").style.display = "block";
}

function closeStudentModal() {
    document.getElementById("addStudentModal").style.display = "none";
}

// Handle Add Student Form Submission

window.onload = function() {

document.getElementById("addStudentForm").addEventListener("submit", async (e) => {
    console.log("Im")
    e.preventDefault();
    const formData = new FormData(e.target);

    const data = {
        first_name: formData.get("first_name"),
        last_name: formData.get("last_name"),
        email: formData.get("email"),
        password: formData.get("password"),
        grade: formData.get('grade'),
        faculty: formData.get('faculty'),
    };

    try {
        const response = await fetch("/add-student/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}", // Ensure CSRF token is present in your context
            },
            body: JSON.stringify(data),
        });

        if (response.ok) {
            alert("Student added successfully!");
            closeStudentModal();
            location.reload(); // Reload page to update student table
        } else {
            alert("Failed to add student. Please try again.");
        }
    } catch (error) {
        console.error("Error adding student:", error);
        alert("An error occurred.");
    }
});
}

// ENDS HERE /////////////////////////////////////////////////



// HANDLE STUDENT SEARCH 

async function searchStudents() {
    const query = document.getElementById('searchInput').value.trim();
    if (!query) {
        alert("Please enter a search query.");
        return;
    }

    const response = await fetch(`/teacher_dashboard/students/search/?q=${encodeURIComponent(query)}`);

    if (response.ok) {
        const students = await response.json();
        updateStudentTable(students);
    } else {
        alert("Error fetching students. Please try again.");
    }
}

function updateStudentTable(students) {
    const studentTableBody = document.getElementById('studentTableBody');
    studentTableBody.innerHTML = '';

    students.forEach((student, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${student.first_name} ${student.last_name}</td>
            <td>${student.email}</td>
            <td>${student.related_courses.join(', ')}</td>
            <td><a href="/teacher_dashboard/student/${student.id}/details/" class="details-button">Details</a></td>
        `;
        studentTableBody.appendChild(row);
    });
}
