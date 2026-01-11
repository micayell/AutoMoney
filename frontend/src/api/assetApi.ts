import axios from 'axios';
import type { Asset } from '../types/asset';

// Proxy 설정이 vite.config.ts에 필요함 (CORS 회피)
// 혹은 백엔드에서 @CrossOrigin 설정 필요
const client = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getAssets = async (): Promise<Asset[]> => {
  const response = await client.get<Asset[]>('/assets');
  return response.data;
};

export const createAsset = async (asset: Asset): Promise<Asset> => {
  const response = await client.post<Asset>('/assets', asset);
  return response.data;
};

export const deleteAsset = async (id: number): Promise<void> => {
  await client.delete(`/assets/${id}`);
};

