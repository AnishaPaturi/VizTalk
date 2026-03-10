import ChartRenderer from "./ChartRenderer";

function Dashboard({ result }) {

  if (!result) return null;

  return (
    <div>

      <h3>Generated SQL</h3>
      <pre>{result.sql}</pre>

      <h3>Chart</h3>
      <ChartRenderer data={result.data} />

    </div>
  );
}

export default Dashboard;