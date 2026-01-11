import axios from 'axios';

const api = axios.create({
  baseURL: '/api/stock',
});

export interface StockBalance {
  stocks: {
    pdno: string;
    prdt_name: string;
    hldg_qty: string;
    evlu_pfls_amt: string;
    pftrt: string;
  }[];
  cash: number;
}

export const getStockBalance = async (): Promise<StockBalance> => {
  const response = await api.get('/balance');
  return response.data;
};

