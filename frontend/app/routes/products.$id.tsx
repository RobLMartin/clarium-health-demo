import { LoaderFunctionArgs, ActionFunctionArgs } from "@remix-run/node";
import { fetchProductDetails, predictInventory } from "../data/products";
import { useFetcher, useLoaderData } from "@remix-run/react";
import InventoryChart from "../components/inventory.chart";

export const loader = async ({ params }: LoaderFunctionArgs) => {
  const { id } = params;

  if (!id) {
    return { product: null, historicalData: null, predictedData: null };
  }

  const data = await fetchProductDetails(id);

  if (!data) {
    return { product: null, historicalData: null, predictedData: null };
  }

  return {
    product: data.product,
    historicalData: data.historicalData,
    predictedData: data.predictedData,
  };
};

export const action = async ({ params }: ActionFunctionArgs) => {
  const { id } = params;
  if (!id) {
    throw Error("idk");
  }

  return await predictInventory(Number(id));
};

export default function ProductPage() {
  const { product, historicalData, predictedData } =
    useLoaderData<typeof loader>();
  const fetcher = useFetcher();

  return (
    <div className="p-6">
      <div className="flex justify-between">
        <div className="flex-1">
          <h1 className="text-6xl font-bold mb-1">{product.name}</h1>
          <p className="text-xl font-light">{product.description}</p>
        </div>
        <fetcher.Form method="post">
          <button className="bg-[#1E69FC] flex-none px-6 py-2 text-base leading-normal rounded-lg shadow-sm text-white font-semibold">
            Predict Inventory
          </button>
        </fetcher.Form>
      </div>

      <h2 className="my-6 text-3xl">Historical Data</h2>
      <div className="bg-white shadow-lg rounded-lg p-8">
        <InventoryChart
          historicalData={historicalData}
          predictedData={predictedData}
        />
      </div>
    </div>
  );
}
