import axios from 'axios';

const api = axios.create({
  baseURL: '/api/lotto',
});

export interface LottoRecommendation {
  numbers: number[];
  strategy: string;
}

export const getLottoRecommendation = async (strategy: string = 'random'): Promise<LottoRecommendation> => {
  const response = await api.get('/recommend', {
    params: { strategy }
  });
  return response.data;
};
