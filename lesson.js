function checkAnswer(exerciseId) {
    let answer = document.getElementById(`answer-${exerciseId}`).value;

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            answer: answer,
            exercise_id: exerciseId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.correct) {
            alert("✅ Correct!");
        } else {
            alert("❌ Wrong! Try again.");
        }
    });
}