
    // Modal control functions
    function openCourseModal() {
        document.getElementById('addCourseModal').style.display = 'block';
    }

    function closeCourseModal() {
        document.getElementById('addCourseModal').style.display = 'none';
    }

    function getCSRFToken() {
        const csrfToken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return csrfToken;
    }

    window.onload = function () {
        const addCourseForm = document.getElementById('addCourseForm');
        addCourseForm.addEventListener('submit', async function (e) {
            e.preventDefault();

            const formData = new FormData(addCourseForm);

            const csrfToken = getCSRFToken();

            const response = await fetch("/add-course/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken, 
                },
                body: formData,  
            });

            if (response.ok) {
                alert("Course added successfully!");
                closeCourseModal();  
                window.location.reload();
            } else {
                alert("Failed to add course. Please try again.");
            }
        });
    };


    // HANDLE COURSES SEARCH FUNCTIONALITY

    async function searchCourses() {
        const query = document.getElementById('searchInput').value.trim();
    
        if (!query) {
            alert("Please enter a search query.");
            return;
        }
    
        const response = await fetch(`/teacher_dashboard/courses/search/?q=${encodeURIComponent(query)}`);
    
        if (response.ok) {
            const courses = await response.json();
            updateCoursesTable(courses);
        } else {
            alert("Error fetching courses. Please try again.");
        }
    }
    
    function updateCoursesTable(courses) {
        const tableBody = document.getElementById('coursesTableBody');
        tableBody.innerHTML = ''; // Clear the current table
    
        if (courses.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="3">No courses found.</td></tr>';
            return;
        }
    
        courses.forEach((course, index) => {
            const row = `
                <tr>
                    <td>${index + 1}</td>
                    <td>${course.title}</td>
                    <td>
                        <a href="/teacher_dashboard/courses/${course.id}/details/" class="details-button">Details</a>
                    </td>
                </tr>
            `;
            tableBody.innerHTML += row;
        });
    }
    