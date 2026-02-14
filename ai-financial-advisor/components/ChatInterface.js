"use client";
import { useState, useRef, useEffect } from "react";

export default function ChatInterface({ context, initialMessage, apiUrl }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const chatBoxRef = useRef(null);

  // Charger le message initial de l'IA quand l'analyse est faite
  useEffect(() => {
    if (initialMessage) {
      setMessages([{ role: "AI", text: initialMessage }]);
    }
  }, [initialMessage]);

  // Scroll automatique vers le bas
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const sendMessage = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg = input.trim();
    setMessages((prev) => [...prev, { role: "You", text: userMsg }]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch(`${apiUrl}/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: userMsg,
          context: context, // On envoie l'objet context directement
        }),
      });

      const data = await response.json();

      if (data.response) {
        setMessages((prev) => [...prev, { role: "AI", text: data.response }]);
      } else {
        throw new Error("Réponse vide du serveur");
      }
    } catch (error) {
      console.error("Chat Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "AI", text: "Erreur de connexion avec l'IA." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <>
      <div className="chat-header">
        <div
          className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
          style={{ width: 32, height: 32 }}
        >
          <i className="bi bi-robot"></i>
        </div>
        <div className="ms-2">
          <h6 className="m-0 fw-bold">Assistant IA</h6>
          <small className="text-secondary">Expert Financier</small>
        </div>
      </div>

      <div className="chat-messages" ref={chatBoxRef}>
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`message-bubble ${msg.role === "You" ? "msg-user" : "msg-ai"}`}
          >
            <div
              dangerouslySetInnerHTML={{
                __html:
                  msg.role === "AI"
                    ? msg.text
                        .replace(/\n/g, "<br>")
                        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
                    : msg.text,
              }}
            />
          </div>
        ))}
        {isTyping && (
          <div className="message-bubble msg-ai typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
      </div>

      <div className="chat-input-area">
        <input
          type="text"
          className="form-control custom-input"
          placeholder="Posez votre question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="btn btn-primary rounded-circle ms-2"
          style={{ width: 42, height: 42 }}
          onClick={sendMessage}
        >
          <i className="bi bi-send-fill"></i>
        </button>
      </div>
    </>
  );
}
