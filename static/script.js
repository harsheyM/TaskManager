// Load tasks on page load
document.addEventListener("DOMContentLoaded", () => {

    // Fetch and display tasks
    fetchTasks();

    // Set up AI button event listener safely
    const askBtn = document.querySelector("#askBtn");
    const promptInput = document.querySelector("#promptInput");

    if (askBtn && promptInput) {
        askBtn.addEventListener("click", () => {
            const prompt = promptInput.value;
            if (prompt.trim() !== "") {
                askAI(prompt);
            }
        });
    }

});

// Fetch tasks from backend
function fetchTasks() {
    fetch("/tasks")
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById("task-list");
            list.innerHTML = "";

            data.forEach(task => {
                const li = document.createElement("li");
                li.textContent = `${task.title} (Priority ${task.priority}) - Due ${task.due_date}`;

                if (!task.completed) {
                    const completeBtn = document.createElement("button");
                    completeBtn.textContent = "Complete";
                    completeBtn.onclick = () => completeTask(task.id);
                    li.appendChild(completeBtn);
                }

                const deleteBtn = document.createElement("button");
                deleteBtn.textContent = "Delete";
                deleteBtn.onclick = () => deleteTask(task.id);
                li.appendChild(deleteBtn);

                if (task.completed) li.classList.add("completed");

                list.appendChild(li);
            });
        });
}

// Task CRUD functions
function addTask() {
    const title = document.getElementById("title").value;
    const priority = document.getElementById("priority").value;
    const due_date = document.getElementById("due_date").value;

    fetch("/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({title, priority, due_date})
    }).then(() => {
        document.getElementById("title").value = "";
        document.getElementById("priority").value = "";
        document.getElementById("due_date").value = "";
        fetchTasks();
    });
}

function completeTask(id) {
    fetch(`/tasks/${id}`, { method: "PUT" })
        .then(() => fetchTasks());
}

function deleteTask(id) {
    fetch(`/tasks/${id}`, { method: "DELETE" })
        .then(() => fetchTasks());
}

// AI function
async function askAI(prompt) {
    try {
        const response = await fetch("/ask-ai", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();  // <--- data must be used here
        if (data.response) {
            console.log("AI Response:", data.response);
            // Display in HTML
            const aiDiv = document.getElementById("ai-response");
            if (aiDiv) aiDiv.textContent = data.response;
        } else {
            console.error("Error:", data.error);
        }
    } catch (err) {
        console.error("Network or server error:", err);
    }
}


askBtn.addEventListener("click", () => {
    const prompt = promptInput.value;
    if (prompt.trim() !== "") {
        askAI(prompt);
        promptInput.value = "";  // Clear input after sending
    }
});


