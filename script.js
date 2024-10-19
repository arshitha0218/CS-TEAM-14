$(document).ready(function() {
    $('#studentForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        const studentData = {
            name: $('#name').val(),
            batch: $('#batch').val(),
            academicPerformance: parseFloat($('#academicPerformance').val()),
            consistency: parseFloat($('#consistency').val()),
            coreExcellence: parseFloat($('#coreExcellence').val()),
            hackathonParticipation: parseFloat($('#hackathonParticipation').val()),
            paperPresentations: parseFloat($('#paperPresentations').val()),
            contributions: parseFloat($('#contributions').val())
        };

        // Send student data to the backend
        $.post("/api/students", studentData, function(response) {
            alert('Student added successfully!'); // Display success message
            $('#studentForm')[0].reset(); // Reset the form
            fetchTopStudents(); // Fetch the updated list of top students
        }).fail(function() {
            alert('Error adding student!'); // Display error message
        });
    });

    function fetchTopStudents() {
        // Fetch top students from the backend
        $.get("/api/students/top", function(data) {
            $('#topStudents').empty(); // Clear previous results
            data.forEach(student => {
                $('#topStudents').append(`<li>${student.name} - Score: ${student.score}</li>`);
            });
        });
    }

    fetchTopStudents(); // Initial fetch of top students on page load
});
