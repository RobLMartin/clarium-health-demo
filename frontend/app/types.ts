export type Product = {
  id: number;
  name: string;
  description: string;
  historicalData?: Array<HistoricalInventory>;
  predictedData?: Array<PredictedInventory>;
};

export type HistoricalInventory = {
  createdAt: string;
  date: string;
  id: number;
  productId: number;
  quantity: number;
  updatedAt: string;
};

export type PredictedInventory = {
  id: number;
  productId: number;
  date: string;
  predictedQuantity: number;
  createdAt: string;
  updatedAt: string;
};
