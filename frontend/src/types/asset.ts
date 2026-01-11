export interface Asset {
  id?: number;
  type: 'CASH' | 'STOCK' | 'REAL_ESTATE' | 'SAVING' | 'DEBT';
  amount: number;
  description: string;
  date: string;
}

export const ASSET_TYPES = {
  CASH: '현금',
  STOCK: '주식',
  REAL_ESTATE: '부동산',
  SAVING: '예적금',
  DEBT: '부채',
} as const;
