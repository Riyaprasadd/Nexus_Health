import React, { useState } from "react";

function Chatbot() {
  const [messages, setMessages] = useState([
    { sender: "bot", message: "Hello! I am your wellness assistant." },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", message: input }];
    setMessages(newMessages);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user: "testuser", // TODO: replace with logged-in username from state
          message: input,
          language: "en", // default language
        }),
      });

      if (!res.ok) {
        const errData = await res.json();
        setMessages([
          ...newMessages,
          { sender: "bot", message: `❌ Error: ${errData.detail || res.status}` },
        ]);
      } else {
        const data = await res.json();
        setMessages([
          ...newMessages,
          { sender: "bot", message: data.response || "⚠️ No response from bot" },
        ]);
      }
    } catch (err) {
      setMessages([
        ...newMessages,
        { sender: "bot", message: "⚠️ Backend not reachable" },
      ]);
    }

    setInput("");
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 p-4">
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto mb-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`p-2 my-1 rounded max-w-xs ${
              msg.sender === "user"
                ? "bg-blue-200 self-end text-right ml-auto"
                : "bg-gray-300 self-start mr-auto"
            }`}
          >
            {msg.message}
          </div>
        ))}
      </div>

      {/* Input Box */}
      <div className="flex">
        <input
          type="text"
          className="flex-1 p-2 border rounded-l"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          onClick={sendMessage}
          className="bg-blue-500 text-white px-4 rounded-r hover:bg-blue-600"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default Chatbot;
