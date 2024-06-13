import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { HistoricalInventory, PredictedInventory } from "../types";

type InventoryChartProps = {
  historicalData: Array<HistoricalInventory>;
  predictedData: Array<PredictedInventory>;
};

const InventoryChart = ({
  historicalData,
  predictedData,
}: InventoryChartProps) => {
  const dataMap = new Map();

  historicalData.forEach((record) => {
    dataMap.set(record.date, {
      date: record.date,
      historicalQuantity: record.quantity,
      predictedQuantity: null,
    });
  });

  predictedData.forEach((record) => {
    if (dataMap.has(record.date)) {
      dataMap.get(record.date).predictedQuantity = record.predictedQuantity;
    } else {
      dataMap.set(record.date, {
        date: record.date,
        historicalQuantity: null,
        predictedQuantity: record.predictedQuantity,
      });
    }
  });

  const chartData = Array.from(dataMap.values());

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="historicalQuantity"
          stroke="#1E69FC"
          activeDot={{ r: 8 }}
          dot={{ r: 4 }}
          name="Historical"
          strokeWidth={3}
        />
        <Line
          type="monotone"
          dataKey="predictedQuantity"
          stroke="#9cbdff"
          activeDot={{ r: 8 }}
          dot={{ r: 4 }}
          name="Predicted"
          strokeWidth={2}
          strokeDasharray={4}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default InventoryChart;
