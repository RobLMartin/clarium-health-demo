import { Link, useLoaderData } from "@remix-run/react";
import { fetchProducts } from "../data/products";
import { Product } from "../types";

export const loader = async () => {
  const products = await fetchProducts();

  if (!products) {
    return { products: [] };
  }

  return { products };
};

export default function ProductsList() {
  const { products } = useLoaderData<typeof loader>();

  return (
    <div>
      {products.map((product: Product) => (
        <Link
          to={`${product.id}`}
          key={product.id}
          className="flex justify-between items-center p-6 border-b border-gray-300 hover:bg-white"
        >
          <div className="flex-1 flex">
            <span className="mr-4 font-light">{product.id}</span>
            <span className="font-semibold">{product.name}</span>
          </div>
          <span className="flex-2 text-right">{product.description}</span>
        </Link>
      ))}
    </div>
  );
}
