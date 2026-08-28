const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

if (loginForm) {
  loginForm.addEventListener("submit", async e => {
    e.preventDefault();
    const message = document.getElementById("message");
    try {
      const data = await api("/login", {
        method:"POST",
        body:JSON.stringify({
          username: username.value,
          password: password.value
        })
      });
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));
      location.href = "dashboard.html";
    } catch(err) { message.textContent = err.message; }
  });
}

if (registerForm) {
  registerForm.addEventListener("submit", async e => {
    e.preventDefault();
    const message = document.getElementById("message");
    try {
      await api("/register", {
        method:"POST",
        body:JSON.stringify({
          username: document.getElementById("username").value,
          email: document.getElementById("email").value,
          password: document.getElementById("password").value
        })
      });
      message.textContent = "Register successful. Redirecting...";
      setTimeout(()=>location.href="index.html", 800);
    } catch(err) { message.textContent = err.message; }
  });
}
