import express from "express";

const app = express();

// Parse form data
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static("views"));

// Home page
app.get("/", (req, res) => {
  res.sendFile("index.html", { root: "views" });
});

// Form page
app.get("/form", (req, res) => {
  res.sendFile("form.html", { root: "views" });
});

// Handle form submission
app.post("/submit", async (req, res) => {
  try {
    const response = await fetch("http://backend:5000/submit", {
    // const response = await fetch("http://localhost:5000/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req.body)
    });

    if (!response.ok) {
      throw new Error("Backend error");
    }

    // Redirect on success
    res.redirect("/success");

  } catch (error) {
    // Show error on same page (no redirect)
    res.send(`
      <h3 style="color:red;">Error submitting data</h3>
      <a href="/form">Go back to form</a>
    `);
  }
});

// Success page
app.get("/success", (req, res) => {
  res.sendFile("success.html", { root: "views" });
});

// IMPORTANT for Docker
app.listen(3000, "0.0.0.0", () => {
  console.log("Frontend running on port 3000");
});
