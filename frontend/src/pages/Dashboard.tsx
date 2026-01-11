export const Dashboard = () => {
  return (
    <div className="space-y-8">
      <div className="border-b border-gray-200 pb-5">
        <h1 className="text-2xl font-bold text-gray-900">대시보드</h1>
        <p className="mt-1 text-sm text-gray-500">AutoMoney 서비스의 주요 현황을 한눈에 확인하세요.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white overflow-hidden shadow rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <div className="text-indigo-600 mb-4">
            {/* 아이콘 */}
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900">자산 관리</h3>
          <p className="mt-2 text-sm text-gray-500">내 모든 자산 포트폴리오를 관리하고 분석합니다.</p>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <div className="text-blue-600 mb-4">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900">주식 자동매매</h3>
          <p className="mt-2 text-sm text-gray-500">AI 봇이 자동으로 주식을 매매하고 수익을 관리합니다.</p>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer border border-gray-100">
          <div className="text-green-600 mb-4">
            <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <h3 className="text-lg font-medium text-gray-900">로또 추천</h3>
          <p className="mt-2 text-sm text-gray-500">과거 데이터를 기반으로 이번 주 당첨 번호를 예측합니다.</p>
        </div>
      </div>
    </div>
  );
};
