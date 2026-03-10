import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";

function ChartRenderer({ data }) {

  if (!data || data.length === 0) return <p>No data</p>;

  const keys = Object.keys(data[0]);

  const xKey = keys[0];
  const yKey = keys[1];

  return (
    <ResponsiveContainer width="80%" height={400}>
      <BarChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={xKey} />
        <YAxis />
        <Tooltip />
        <Bar dataKey={yKey} />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default ChartRenderer;