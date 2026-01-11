import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getAssets, deleteAsset } from '../api/assetApi';
import { ASSET_TYPES } from '../types/asset';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Trash2 } from 'lucide-react';
import { useState } from 'react';
import { AssetForm } from '../components/AssetForm';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export const AssetPage = () => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const queryClient = useQueryClient();

  const { data: assets, isLoading } = useQuery({
    queryKey: ['assets'],
    queryFn: getAssets,
  });

  const deleteMutation = useMutation({
    mutationFn: deleteAsset,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['assets'] });
    },
  });

  if (isLoading) return <div className="p-10 text-center">Loading...</div>;

  const totalAmount = assets?.reduce((sum, asset) => sum + asset.amount, 0) || 0;

  const chartData = assets?.reduce((acc, asset) => {
    const existing = acc.find(item => item.name === ASSET_TYPES[asset.type]);
    if (existing) {
      existing.value += asset.amount;
    } else {
      acc.push({ name: ASSET_TYPES[asset.type], value: asset.amount });
    }
    return acc;
  }, [] as { name: string; value: number }[]) || [];

  return (
    <div className="space-y-8">
      {/* 헤더 */}
      <div className="flex justify-between items-center border-b border-gray-200 pb-5">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">자산 관리</h1>
          <p className="mt-1 text-sm text-gray-500">내 모든 자산을 한눈에 파악하고 관리하세요.</p>
        </div>
        <button 
          onClick={() => setIsFormOpen(true)}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 transition-colors"
        >
          + 자산 추가
        </button>
      </div>

      {isFormOpen && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center z-50 transition-opacity">
            <div className="w-full max-w-lg bg-white rounded-lg shadow-xl overflow-hidden transform transition-all">
                <AssetForm onClose={() => setIsFormOpen(false)} />
            </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* 차트 영역 */}
        <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-100 flex flex-col">
            <div className="px-5 py-5 border-b border-gray-100 bg-gray-50">
            <h3 className="text-lg leading-6 font-medium text-gray-900">포트폴리오 비중</h3>
            </div>
            <div className="px-5 py-6 flex-1">
            {chartData.length > 0 ? (
                <div className="relative h-80 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                        data={chartData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={80}
                        paddingAngle={5}
                        dataKey="value"
                        >
                        {chartData.map((_, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                        </Pie>
                        <Tooltip 
                        formatter={(value: number) => [`₩${value.toLocaleString()}`, '금액']} 
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}
                        />
                        <Legend verticalAlign="bottom" height={36}/>
                    </PieChart>
                    </ResponsiveContainer>
                    <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                    <span className="text-xs text-gray-500">총 자산</span>
                    <span className="text-lg font-bold text-gray-900">₩{totalAmount.toLocaleString()}</span>
                    </div>
                </div>
            ) : (
                <div className="h-80 flex flex-col items-center justify-center text-center">
                    <p className="text-gray-400 mb-2">데이터가 없습니다.</p>
                    <p className="text-xs text-gray-400">자산을 추가하여 포트폴리오를 완성해보세요.</p>
                </div>
            )}
            </div>
        </div>

        {/* 리스트 영역 */}
        <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-100">
            <div className="px-5 py-5 border-b border-gray-100 bg-gray-50">
            <h3 className="text-lg leading-6 font-medium text-gray-900">자산 목록</h3>
            </div>
            <div className="px-5 py-6">
            <div className="overflow-y-auto max-h-[400px]">
                {assets && assets.length > 0 ? (
                    <ul className="divide-y divide-gray-200">
                    {assets.map((asset) => (
                        <li key={asset.id} className="py-4 flex justify-between items-center hover:bg-gray-50 px-2 rounded-md transition-colors">
                        <div className="flex items-center gap-4">
                            <div className={`p-2 rounded-full ${
                                asset.type === 'CASH' ? 'bg-green-100 text-green-600' :
                                asset.type === 'STOCK' ? 'bg-red-100 text-red-600' :
                                asset.type === 'REAL_ESTATE' ? 'bg-blue-100 text-blue-600' :
                                'bg-gray-100 text-gray-600'
                            }`}>
                                <span className="text-xs font-bold">{ASSET_TYPES[asset.type].substring(0, 1)}</span>
                            </div>
                            <div>
                                <p className="font-medium text-gray-900">{asset.description}</p>
                                <p className="text-xs text-gray-500">{asset.date} · {ASSET_TYPES[asset.type]}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-4">
                            <span className="font-bold text-gray-900">₩{asset.amount.toLocaleString()}</span>
                            <button 
                            onClick={() => asset.id && deleteMutation.mutate(asset.id)}
                            className="text-gray-400 hover:text-red-500 p-1 rounded-full hover:bg-red-50 transition-all"
                            title="삭제"
                            >
                            <Trash2 size={18} />
                            </button>
                        </div>
                        </li>
                    ))}
                    </ul>
                ) : (
                    <p className="text-gray-500 text-center py-10 text-sm">등록된 자산이 없습니다.</p>
                )}
            </div>
            </div>
        </div>
      </div>
    </div>
  );
};

