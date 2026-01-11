import { useForm } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createAsset } from '../api/assetApi';
import type { Asset } from '../types/asset';
import { ASSET_TYPES } from '../types/asset';

interface AssetFormProps {
  onClose: () => void;
}

export const AssetForm = ({ onClose }: AssetFormProps) => {
  const { register, handleSubmit, reset } = useForm<Asset>();
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: createAsset,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] });
      reset();
      onClose();
    },
  });

  const onSubmit = (data: Asset) => {
    // 날짜가 비어있으면 오늘 날짜로
    if (!data.date) {
        data.date = new Date().toISOString().split('T')[0];
    }
    mutation.mutate(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-lg font-bold mb-4">자산 추가</h3>
      
      <div className="grid grid-cols-1 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">종류</label>
          <select 
            {...register('type')} 
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
          >
            {Object.entries(ASSET_TYPES).map(([key, value]) => (
              <option key={key} value={key}>{value}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">금액</label>
          <input 
            type="number" 
            {...register('amount', { required: true, valueAsNumber: true })} 
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            placeholder="금액을 입력하세요"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">설명</label>
          <input 
            type="text" 
            {...register('description')} 
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            placeholder="예: 월급, 적금 불입"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">날짜</label>
          <input 
            type="date" 
            {...register('date')} 
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm p-2 border"
            defaultValue={new Date().toISOString().split('T')[0]}
          />
        </div>
      </div>

      <div className="flex justify-end gap-2 mt-4">
        <button 
            type="button" 
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
        >
            취소
        </button>
        <button 
          type="submit" 
          disabled={mutation.isPending}
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
          {mutation.isPending ? '저장 중...' : '저장'}
        </button>
      </div>
    </form>
  );
};

