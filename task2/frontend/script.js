
let ws;
let username = '';
let currentRoom = null;
let targetUser = null;

//Elements
const UI = {
    loginScreen: document.getElementById('login-screen'),
    chatScreen: document.getElementById('chat-screen'),
    usernameInput: document.getElementById('username-input'),
    loginBtn: document.getElementById('login-button'),
    roomList: document.getElementById('room-list'),
    userList: document.getElementById('user-list'),
    messagesBox: document.getElementById('messages'),
    messageInput: document.getElementById('message-input'),
    sendBtn: document.getElementById('send-button'),
    newRoomInput: document.getElementById('new-room-input'),
    createRoomBtn: document.getElementById('create-room-button'),
    roomNameHeader: document.getElementById('current-room-name'),
    inputArea: document.getElementById('message-input-area'),
    chatModeIndicator: document.getElementById('chat-mode-indicator'),
    targetUserNameSpan: document.getElementById('target-user-name')
};

// Events
UI.loginBtn.addEventListener('click', handleLogin);
UI.createRoomBtn.addEventListener('click', handleCreateRoom);
UI.sendBtn.addEventListener('click', handleSendMessage);
UI.messageInput.addEventListener('keypress', (e) => e.key === 'Enter' && handleSendMessage());

//  Handlers
function handleLogin() {
    username = UI.usernameInput.value.trim();
    if (username) {
        connectWebSocket();
        UI.loginScreen.classList.remove('active'); 
        UI.chatScreen.classList.add('active');
    }
}

function handleCreateRoom() {
    const room = UI.newRoomInput.value.trim();
    if (room && ws) {
        ws.send(JSON.stringify({ action: 'create_room', room: room }));  // create room
        UI.newRoomInput.value = '';
    }
}

function handleSendMessage() {
    const text = UI.messageInput.value.trim();
    if (text && currentRoom && ws) {
        ws.send(JSON.stringify({
            action: 'message',
            content: text,
            recipient: targetUser
        }));
        UI.messageInput.value = '';
    }
}

function joinRoom(room) {
    currentRoom = room;
    targetUser = null;
    updateUIForRoom(room);
    ws.send(JSON.stringify({ action: 'join', room: room }));
}

function startPrivateChat(user) {
    targetUser = user;
    updateChatModeUI();
    fetchHistory();

    Array.from(UI.userList.children).forEach(li => {
        if (li.textContent === targetUser) li.classList.add('selected'); // highlight selected user
        else li.classList.remove('selected');
    });
}

function fetchHistory() {
    if (currentRoom && ws) {
        ws.send(JSON.stringify({
            action: 'get_history',
            target_user: targetUser
        }));
    }
}


function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8765');
    ws.onopen = () => ws.send(JSON.stringify({ action: 'set_username', username }));
    ws.onerror = (err) => console.error('WebSocket Error:', err);

    //handlers for incoming messages
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'room_list') renderRoomList(data.rooms);
        else if (data.type === 'history') loadHistory(data.messages);
        else if (data.type === 'user_list') renderUserList(data.users);
        else if (data.type === 'message') handleNewMessage(data);
    };
}

function handleNewMessage(data) {
    const isPrivateMatch = targetUser && ((data.sender === targetUser && data.recipient === username) || (data.sender === username && data.recipient === targetUser));
    const isPublicMatch = !targetUser && data.recipient === null;
    
    if (isPrivateMatch || isPublicMatch) {
         appendMessage(data);
         UI.messagesBox.scrollTop = UI.messagesBox.scrollHeight;
    }
}


function renderRoomList(rooms) {
    UI.roomList.innerHTML = '';
    rooms.forEach(room => {
        const li = document.createElement('li');
        li.textContent = room;
        if (room === currentRoom) li.classList.add('selected');
        li.addEventListener('click', () => joinRoom(room));
        UI.roomList.appendChild(li);
    });
}

function renderUserList(users) {
    UI.userList.innerHTML = '';
    users.forEach(user => {
        const li = document.createElement('li');
        if (user === username) {
            li.textContent = `${user} (You)`;
        } else {
            li.textContent = user;
            if (user === targetUser) li.classList.add('selected');
            li.addEventListener('click', () => startPrivateChat(user));
        }
        UI.userList.appendChild(li);
    });
}

function loadHistory(messages) {
    UI.messagesBox.innerHTML = '';
    messages.forEach(msg => appendMessage(msg));
    UI.messagesBox.scrollTop = UI.messagesBox.scrollHeight;
}

function appendMessage(msg) {
    const div = document.createElement('div');
    div.className = 'message';
    div.innerHTML = `<b>${msg.sender}:</b> ${msg.content}`;
    UI.messagesBox.appendChild(div);
}

function updateUIForRoom(room) {
    UI.roomNameHeader.textContent = room;
    UI.inputArea.classList.remove('hidden');
    UI.messagesBox.innerHTML = '';
}

function updateChatModeUI() {
    UI.messageInput.placeholder = targetUser ? `Private msg to ${targetUser}` : `Msg ${currentRoom}`;
}
