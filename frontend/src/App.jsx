import { useState } from "react";
import PromptInput from "./components/PromptInput";
import Dashboard from "./components/Dashboard";
import { sendQuery } from "./services/api";

function App() {

  const [result, setResult] = useState(null);

  const handleQuery = async (prompt) => {

    try {

      const response = await sendQuery(prompt);

      setResult(response);

    } catch (error) {

      console.error(error);
      alert("Error generating dashboard");

    }
  };

  return (
    <div style={{ padding: "40px" }}>

      <h1>Conversational BI Dashboard</h1>

      <PromptInput onSubmit={handleQuery} />

      <Dashboard result={result} />

    </div>
  );
}

export default App;