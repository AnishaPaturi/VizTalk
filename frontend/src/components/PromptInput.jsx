import { useState } from "react";

function PromptInput({ onSubmit }) {
  const [query, setQuery] = useState("");

  const handleSubmit = () => {
    if (!query) return;
    onSubmit(query);
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <input
        type="text"
        placeholder="Ask a business question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "400px", padding: "8px" }}
      />

      <button onClick={handleSubmit} style={{ marginLeft: "10px" }}>
        Generate
      </button>
    </div>
  );
}

export default PromptInput;