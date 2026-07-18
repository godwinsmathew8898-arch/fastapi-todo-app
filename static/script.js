let current_user = "";

function loginUser() {
    let input = document.getElementById("usernameInput").value;
    if (input.trim() !== "") {
        current_user = input.trim(); 
        
        document.getElementById("loginSection").style.display = "none";
        document.getElementById("todoSection").style.display = "block";
        
        document.getElementById("userGreeting").innerText = `📝 ${current_user}'s Todo List`;
        
        loadTasks();
    }
}

function logoutUser() {
    current_user = "";
    document.getElementById("loginSection").style.display = "block";
    document.getElementById("todoSection").style.display = "none";
    
    // FIX: Spelled getElementById correctly
    document.getElementById("usernameInput").value = "";
}

async function loadTasks() {
    let response = await fetch(`/view/${current_user}`);
    let data = await response.json();
    
    let listElement = document.getElementById("list");
    listElement.innerHTML = "";
    
    for (let item of data.todo_list) {
        listElement.innerHTML += `
            <li> 
                <span>✅ ${item.task}</span> 
                <button class="delete-btn" onclick="deleteTask(${item.id})">❌</button> 
            </li>
        `;
    }
}

async function addTask() {
    let input = document.getElementById("taskInput");
    let task = input.value;
    
    if (task !== "") {
        await fetch(`/add/${current_user}/${task}`);
        input.value = "";
        loadTasks();
    }
}

async function deleteTask(taskId) {
    await fetch(`/delete/${taskId}`);
    loadTasks();
}
