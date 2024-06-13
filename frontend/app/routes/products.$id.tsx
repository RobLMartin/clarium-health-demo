import { LoaderFunctionArgs } from "@remix-run/node";
import { fetchProductDetails } from "../data/products";
import { HistoricalInventory, PredictedInventory } from "../types";
import { useLoaderData } from "@remix-run/react";

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { id } = params;

  if (!id) {
    return { product: null };
  }

  const product = await fetchProductDetails(id);

  if (!product) {
    return { product: null };
  }

  return { product };
};

export default function ProductPage() {
  const { product } = useLoaderData<typeof loader>();
  const { historicalData, predictedData } = product;
  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>

      <h2>Historical Data</h2>
      <ul>
        {historicalData.map((record: HistoricalInventory) => (
          <li key={record.id}>
            {record.date}: {record.quantity}
          </li>
        ))}
      </ul>

      <h2>Predicted Data</h2>
      <ul>
        {predictedData.map((record: PredictedInventory) => (
          <li key={record.id}>
            {record.date}: {record.predictedQuantity}
          </li>
        ))}
      </ul>
    </div>
  );
}
