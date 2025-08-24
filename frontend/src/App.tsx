import React, { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'

// hooks
import { useMapGrid, useOrders, useRestaurants, useDeliveryPoints, useCreateOrder, useMoveBot } from './hooks/userApi'
import type { GridCell } from './types'

// components
import SystemStats from './components/SystemStats'
import OrderForm from './components/OrderForm'
import GridMap from './components/GridMap'
import OrderList from './components/OrderList'

const EagRouteApp: React.FC = () => {
  const [selectedBot, setSelectedBot] = useState<number | null>(null)

  const { data: gridData, isLoading: gridLoading, error: gridError } = useMapGrid()
  const { data: orders, isLoading: ordersLoading } = useOrders()
  const { data: restaurants } = useRestaurants()
  const { data: deliveryPoints } = useDeliveryPoints()
  const createOrderMutation = useCreateOrder()
  const moveBotMutation = useMoveBot()

  const handleCellClick = async (x: number, y: number, cell: GridCell) => {
    if (selectedBot != null && cell.bots.length === 0) {
      try {
        await moveBotMutation.mutateAsync({ botId: selectedBot, x, y })
        setSelectedBot(null)
      } catch (error) {
        console.error('Error moving bot:', error)
      }
    } else if (cell.bots && cell.bots.length > 0) {
      setSelectedBot(cell.bots[0]!.id)
    }
  }

  if (gridError) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 via-gray-50 to-red-100 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl border border-red-100 p-8 max-w-md w-full">
          <div className="text-center">
            <div className="w-20 h-20 bg-gradient-to-br from-red-500 to-red-600 rounded-full flex items-center justify-center mx-auto mb-6 shadow-lg">
              <span className="text-3xl text-white">⚠️</span>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-3">Connection Error</h2>
            <p className="text-gray-600 mb-6 leading-relaxed">Unable to connect to the EagRoute backend server.</p>
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-500 font-mono">Backend: http://localhost:8000</p>
            </div>
            <button onClick={() => window.location.reload()} className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:scale-105">🔄 Retry Connection</button>
          </div>
        </div>
      </div>
    )
  }

  if (gridLoading || ordersLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center">
        <div className="text-center">
          <div className="relative mb-8">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto shadow-2xl">
              <span className="text-3xl text-white">🤖</span>
            </div>
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl blur opacity-25 animate-pulse"></div>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Initializing EagRoute System</h2>
          <p className="text-gray-600 text-lg">Loading delivery bots and map data...</p>
          <div className="mt-6 bg-white rounded-lg p-4 shadow-lg max-w-xs mx-auto">
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>Connecting to backend</span>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
      {/* HEADER: unified container (no Tailwind `container` class), no wrap */}
      <header className="bg-gradient-to-r from-slate-800 via-slate-700 to-slate-800 text-white shadow-2xl sticky top-0 z-50">
        <div className="mx-auto max-w-7xl px-4 lg:px-6 py-4 lg:py-6">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 lg:w-12 lg:h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
                <span className="text-xl lg:text-2xl">🤖</span>
              </div>
              <div>
                <h1 className="text-2xl lg:text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">EagRoute</h1>
                <p className="text-slate-300 text-xs lg:text-sm hidden sm:block">Intelligent Delivery Bot System</p>
              </div>
            </div>

            {selectedBot !== null && (
              <div className="bg-gradient-to-r from-red-500 to-red-600 text-white px-4 lg:px-6 py-2 lg:py-3 rounded-xl shadow-lg animate-pulse">
                <div className="flex items-center gap-2">
                  <span className="text-base lg:text-lg">🎯</span>
                  <div>
                    <div className="font-bold text-sm lg:text-base">Bot #{selectedBot} Selected</div>
                    <div className="text-xs lg:text-sm text-red-100 hidden sm:block">Click empty cell to move</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* MAIN: same max width & paddings */}
      <main className="mx-auto max-w-7xl px-4 lg:px-6 py-6 lg:py-8">
        <div className="grid grid-cols-12 gap-4 lg:gap-6">
          <section className="col-span-12 lg:col-span-3 space-y-4 lg:space-y-6">
            <SystemStats gridData={gridData ?? null} orders={orders ?? []} />
            <OrderForm restaurants={restaurants ?? []} deliveryPoints={deliveryPoints ?? []} onOrderCreated={() => {}} createOrderMutation={createOrderMutation} />
          </section>

          <section className="col-span-12 lg:col-span-6">
            <GridMap gridData={gridData ?? null} selectedBot={selectedBot} onCellClick={handleCellClick} />
          </section>

          <aside className="col-span-12 lg:col-span-3">
            <OrderList orders={orders ?? []} />
          </aside>
        </div>
      </main>

      {/* FOOTER: same max width & paddings */}
      <footer className="bg-white border-t border-gray-200 mt-8 lg:mt-12">
        <div className="mx-auto max-w-7xl px-4 lg:px-6 py-4 lg:py-6">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span>System Online</span>
              <span className="hidden sm:inline text-gray-300">•</span>
              <span className="hidden sm:inline">{orders?.length || 0} Active Orders</span>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-xs text-gray-400">Last updated: {new Date().toLocaleTimeString()}</div>
              <div className="font-medium">EagRoute v2.0 - Enhanced Design</div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      retryDelay: (i) => Math.min(1000 * 2 ** i, 30000),
      staleTime: 5000,
      refetchOnWindowFocus: false,
      refetchOnReconnect: true,
      refetchInterval: 2000,
    },
    mutations: { retry: 1, retryDelay: 1000 },
  },
})

const App: React.FC = () => (
  <QueryClientProvider client={queryClient}>
    <EagRouteApp />
    <ReactQueryDevtools initialIsOpen={false} position="bottom" />
  </QueryClientProvider>
)

export default App
