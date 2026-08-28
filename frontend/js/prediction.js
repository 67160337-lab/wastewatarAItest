requireLogin();
document.getElementById("predictionForm").addEventListener("submit", async e => {
  e.preventDefault();
  const message = document.getElementById("message");
  try {
    const data = await api("/prediction", {
      method:"POST",
      body:JSON.stringify({
        influent_cod:+cod.value,
        flow_rate:+flow.value,
        water_temp:+temp.value,
        current_do:+document.getElementById("do").value
      })
    });
    document.getElementById("result").classList.remove("hidden");
    document.getElementById("speed").textContent = data.predicted_speed + "%";
    message.textContent = "Prediction successful";
  } catch(err) { message.textContent = err.message; }
});
