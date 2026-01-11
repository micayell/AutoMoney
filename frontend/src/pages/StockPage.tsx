import { useQuery } from '@tanstack/react-query';
import { getStockBalance } from '../api/stockApi';

export const StockPage = () => {
  const { data: stockBalance, isLoading: isStockLoading } = useQuery({
    queryKey: ['stockBalance'],
    queryFn: getStockBalance,
  });

  return (
    <div className="space-y-8">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold text-gray-900">주식 자동매매 봇</h1>
        <p className="mt-1 text-sm text-gray-500">KIS 증권 계좌와 연동된 실시간 매매 현황입니다.</p>
      </div>

      <div className="bg-white overflow-hidden shadow rounded-lg border border-gray-100">
        <div className="px-5 py-5 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
          <h3 className="text-lg leading-6 font-medium text-gray-900 flex items-center gap-2">
            투자 현황 <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">KIS</span>
          </h3>
          <span className="text-xs text-gray-400">실시간 연동 중</span>
        </div>
        <div className="px-5 py-6">
          {isStockLoading ? (
            <div className="animate-pulse flex space-x-4">
              <div className="flex-1 space-y-4 py-1">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="space-y-2">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                </div>
              </div>
            </div>
          ) : stockBalance ? (
            <div>
              <div className="mb-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
                  <span className="text-gray-600 text-sm font-medium">주문 가능 현금 (예수금)</span>
                  <div className="mt-2 flex items-baseline">
                    <span className="text-4xl font-bold text-gray-900">₩{stockBalance.cash.toLocaleString()}</span>
                  </div>
                </div>
                {/* 추후 총 평가 금액 등 추가 가능 */}
              </div>
              
              <h4 className="text-md font-semibold text-gray-700 mb-4">보유 종목 현황</h4>
              {stockBalance.stocks.length > 0 ? (
                <div className="overflow-hidden border border-gray-200 rounded-lg">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">종목명</th>
                        <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">보유수량</th>
                        <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">평가손익</th>
                        <th scope="col" className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">수익률</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {stockBalance.stocks.map((stock) => (
                        <tr key={stock.pdno} className="hover:bg-gray-50 transition-colors">
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{stock.prdt_name}</td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-500">{Number(stock.hldg_qty).toLocaleString()}주</td>
                          <td className={`px-6 py-4 whitespace-nowrap text-sm text-right font-bold ${Number(stock.evlu_pfls_amt) > 0 ? 'text-red-600' : Number(stock.evlu_pfls_amt) < 0 ? 'text-blue-600' : 'text-gray-900'}`}>
                            {Number(stock.evlu_pfls_amt).toLocaleString()}원
                          </td>
                          <td className={`px-6 py-4 whitespace-nowrap text-sm text-right ${Number(stock.pftrt) > 0 ? 'text-red-600' : Number(stock.pftrt) < 0 ? 'text-blue-600' : 'text-gray-900'}`}>
                            {stock.pftrt}%
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-16 bg-gray-50 rounded-lg border border-dashed border-gray-300">
                  <p className="text-gray-500 font-medium">현재 보유 중인 주식이 없습니다.</p>
                  <p className="text-gray-400 text-sm mt-2">봇이 매수 기회를 포착하면 여기에 표시됩니다.</p>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center py-10 bg-red-50 rounded-md border border-red-100">
              <p className="text-red-500 text-sm">주식 잔고 정보를 불러오지 못했습니다.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

