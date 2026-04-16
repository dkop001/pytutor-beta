document.addEventListener('DOMContentLoaded', () => {
  const options = document.querySelectorAll('.option-card');
  const checkBtnActive = document.getElementById('check-btn');
  const footer = document.getElementById('bottom-footer');
  const feedbackMsg = document.getElementById('feedback-msg');
  const nextBtn = document.getElementById('next-btn');

  let selectedOption = null;
  let isChecked = false;

  if (options) {
    options.forEach(opt => {
      opt.addEventListener('click', () => {
        if (isChecked) return; // Prevent changing answer after checking

        // Remove selected class from all
        options.forEach(o => o.classList.remove('selected'));
        
        // Add selected class to clicked
        opt.classList.add('selected');
        selectedOption = opt.dataset.id; // Assume data-id holds the choice id

        // Enable check button
        checkBtnActive.removeAttribute('disabled');
      });
    });
  }

  if (checkBtnActive) {
    checkBtnActive.addEventListener('click', async () => {
      if (!selectedOption || isChecked) return;

      const lessonId = window.lessonId; // passed via script tag in html
      const questionIdx = window.questionIdx; // newly added variable

      try {
        const response = await fetch('/api/check_answer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ lesson_id: lessonId, question_idx: questionIdx, answer_id: selectedOption })
        });
        
        const data = await response.json();
        
        isChecked = true;
        checkBtnActive.style.display = 'none';
        nextBtn.style.display = 'block';
        
        if (data.next_url) {
          nextBtn.dataset.nextUrl = data.next_url;
        }

        const selectedEl = document.querySelector(`.option-card[data-id="${selectedOption}"]`);

        if (data.correct) {
          selectedEl.classList.add('correct');
          footer.classList.add('correct-state');
          feedbackMsg.innerHTML = '<i class="fa-solid fa-circle-check"></i> Excellent!';
          
          // Play sound if possible
          // const audio = new Audio('/static/sounds/correct.mp3');
          // audio.play();
        } else {
          selectedEl.classList.add('wrong');
          selectedEl.classList.add('shake');
          footer.classList.add('wrong-state');
          feedbackMsg.innerHTML = `<i class="fa-solid fa-circle-xmark"></i> Incorrect. The correct answer was: <strong>${data.correct_answer_text}</strong>`;
        }
      } catch (e) {
        console.error("Error checking answer", e);
      }
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      if (nextBtn.dataset.nextUrl) {
        window.location.href = nextBtn.dataset.nextUrl;
      } else {
        window.location.reload();
      }
    });
  }
});
