import { useQuery } from '@tanstack/react-query';
import { getLottoRecommendation } from '../api/lottoApi';
import { RefreshCw, Flame, Snowflake, Scale, Dices } from 'lucide-react';
import { useState } from 'react';

export const LottoPage = () => {
  const [strategy, setStrategy] = useState<string>('random');
  
  const { data: lottoData, refetch: refreshLotto, isLoading } = useQuery({
    queryKey: ['lotto', strategy],
    queryFn: () => getLottoRecommendation(strategy),
    enabled: false,
  });

  const strategies = [
    { id: 'random', name: '랜덤', icon: <Dices size={18} />, desc: '완전 무작위 추천' },
    { id: 'hot', name: 'Hot', icon: <Flame size={18} />, desc: '최근 자주 나온 번호' },
    { id: 'cold', name: 'Cold', icon: <Snowflake size={18} />, desc: '오랫동안 안 나온 번호' },
    { id: 'balanced', name: '균형', icon: <Scale size={18} />, desc: 'Hot + Cold + 랜덤' },
  ];

  return (
    <div className="space-y-8">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold text-gray-900">로또 번호 추천</h1>
        <p className="mt-1 text-sm text-gray-500">다양한 분석 전략으로 이번 주 행운의 번호를 조합해보세요.</p>
      </div>

      <div className="max-w-4xl mx-auto bg-white overflow-hidden shadow-lg rounded-xl border border-gray-100 mt-10">
        <div className="px-8 py-8 text-center">
          
          {/* 전략 선택 버튼 */}
          <div className="flex flex-wrap justify-center gap-3 mb-10">
            {strategies.map((s) => (
              <button
                key={s.id}
                onClick={() => setStrategy(s.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-full border transition-all ${
                  strategy === s.id 
                    ? 'bg-indigo-50 border-indigo-500 text-indigo-700 font-semibold ring-2 ring-indigo-200' 
                    : 'bg-white border-gray-200 text-gray-600 hover:bg-gray-50'
                }`}
              >
                {s.icon}
                <span>{s.name}</span>
              </button>
            ))}
          </div>

          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            {strategies.find(s => s.id === strategy)?.name} 전략 추천 번호
          </h2>
          <p className="text-gray-500 mb-8">{strategies.find(s => s.id === strategy)?.desc}</p>
          
          {lottoData ? (
            <div className="animate-fade-in-up">
              <div className="flex flex-wrap justify-center gap-4 mb-8">
                {lottoData.numbers.map((num) => (
                  <div 
                    key={num} 
                    className={`w-16 h-16 flex items-center justify-center rounded-full text-white font-bold text-2xl shadow-lg transform hover:scale-110 transition-transform cursor-default
                      ${num <= 10 ? 'bg-yellow-400' : num <= 20 ? 'bg-blue-500' : num <= 30 ? 'bg-red-500' : num <= 40 ? 'bg-gray-500' : 'bg-green-500'}
                    `}
                  >
                    {num}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <div className="py-12 bg-gray-50 rounded-xl border border-dashed border-gray-200 mb-8">
              <p className="text-gray-400">원하는 전략을 선택하고 번호를 생성해보세요!</p>
            </div>
          )}

          <button 
            onClick={() => refreshLotto()}
            disabled={isLoading}
            className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-full text-white bg-indigo-600 hover:bg-indigo-700 md:text-lg transition-all shadow-md hover:shadow-lg disabled:opacity-50"
          >
            {isLoading ? '분석 중...' : <><RefreshCw className="mr-2" /> 번호 생성하기</>}
          </button>
        </div>
      </div>
    </div>
  );
};
