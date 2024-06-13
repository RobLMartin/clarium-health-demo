import { Product } from "../types";

const { VITE_API_URL } = import.meta.env;

export const fetchProducts = async () => {
  try {
    const response = await fetch(`${VITE_API_URL}/products`);
    if (!response.ok) {
      throw new Error("Failed to fetch products");
    }
    const data: Product[] = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching products:", error);
    throw error;
  }
};

export const fetchProductDetails = async (productId: string) => {
  try {
    const response = await fetch(
      `${VITE_API_URL}/products/${productId}/inventory_data`
    );
    if (!response.ok) {
      throw new Error("Failed to fetch product details");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching product details:", error);
    throw error;
  }
};

export const predictInventory = async (productId: number) => {
  console.log(productId);
  try {
    const response = await fetch(`${VITE_API_URL}/predict_inventory`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ productId }),
    });
    if (!response.ok) {
      throw new Error("Failed to predict inventory");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error predicting inventory:", error);
    throw error;
  }
};
