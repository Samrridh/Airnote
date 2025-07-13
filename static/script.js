document.getElementById("startBtn").addEventListener("click", () => {
  const statusDiv = document.getElementById("status");
  const quizDiv = document.getElementById("quiz");
  const countrySpan = document.getElementById("countryName");
  const resultP = document.getElementById("result");
  statusDiv.innerHTML = "";
  quizDiv.classList.add("hidden");
  resultP.textContent = "";

  const evtSource = new EventSource("/start");

  let country = "", capital = "";

  evtSource.onmessage = function(event) {
    if (event.data.startsWith("END|")) {
      evtSource.close();
      [_, country, capital] = event.data.split("|");
      countrySpan.textContent = country;
      quizDiv.classList.remove("hidden");
    } else {
      const step = document.createElement("div");
      step.textContent = event.data;
      statusDiv.appendChild(step);
    }
  };

  document.getElementById("submitBtn").onclick = () => {
    const userAnswer = document.getElementById("answerInput").value.trim().toLowerCase();
    if (userAnswer === capital.toLowerCase()) {
      resultP.textContent = `✅ Correct! Capital of ${country} is ${capital}`;
      resultP.classList.remove("text-red-600");
      resultP.classList.add("text-green-600");
    } else {
      resultP.textContent = `❌ Wrong! Correct answer is ${capital}`;
      resultP.classList.remove("text-green-600");
      resultP.classList.add("text-red-600");
    }
  };
});
