import React, { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { Bot, Package, MapPin, Activity, AlertTriangle } from 'lucide-react'
import clsx from 'clsx'

// Types
interface Bot {
    id: number
    name: string
    current_x: number
    current_y: number
    max_capacity: number
    status: 'IDLE' | 'BUSY' | 'MAINTENANCE'
    current_orders: number
    battery_level: number
    created_at: string
    updated_at: string
}

interface Order {           
    id: number
    customer_name: string
    customer_phone: string | null
    restaurant_type: 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI'
    pickup_x: number
    pickup_y: number
    delivery_x: number
    delivery_y: number
    status: 'PENDING' | 'ASSIGNED' | 'PICKED_UP' | 'DELIVERED' | 'CANCELLED'
    bot_id: number | null
    priority: number
    estimated_distance: number | null
    estimated_time: number | null
    created_at: string
    updated_at: string
}

interface Restaurant {
    id: number
    x: number
    y: number
    restaurant_type: 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI'
    name: string
}

interface DeliveryPoint {
    id: number
    x: number
    y: number
    name: string
}

interface GridCell {
  x: number
  y: number
  node_type: 'NODE' | 'HOUSE' | 'RESTAURANT' | 'BOT_STATION'
  is_delivery_point: boolean
  is_restaurant: boolean
  is_bot_station: boolean
  restaurant_type: string | null
  name: string
  bots: Array<{
    id: number
    name: string
    status: string
    current_orders: number
    battery_level: number
  }>
  active_orders: Array<{
    id: number
    customer_name: string
    restaurant_type: string
    status: string
    bot_id: number | null
    location_type: 'pickup' | 'delivery'
  }>
}

interface MapGrid {
  grid: Record<string, GridCell>
  grid_size: number
  total_nodes: number
  total_bots: number
  active_orders: number
}

// API Service (simplified for demo)
const API_BASE_URL = 'http://localhost:8000'

const apiService = {
  async getMapGrid(): Promise<MapGrid> {
    const response = await fetch(`${API_BASE_URL}/api/v1/map/grid`)
    if (!response.ok) throw new Error('Failed to fetch map grid')
return (await response.json()) as MapGrid
  },
  
  async getAllOrders(): Promise<Order[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/orders/`)
    if (!response.ok) throw new Error('Failed to fetch orders')
    return response.json()
  },
  
  async getRestaurants(): Promise<Restaurant[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/map/restaurants`)
    if (!response.ok) throw new Error('Failed to fetch restaurants')
    return response.json()
  },
  
  async getDeliveryPoints(): Promise<DeliveryPoint[]> {
    const response = await fetch(`${API_BASE_URL}/api/v1/map/delivery-points`)
    if (!response.ok) throw new Error('Failed to fetch delivery points')
    return response.json()
  },
  
  async createOrder(orderData: any): Promise<Order> {
    const response = await fetch(`${API_BASE_URL}/api/v1/orders/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData)
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to create order')
    }
    return response.json()
  },
  
  async moveBot(botId: number, x: number, y: number) {
    const response = await fetch(`${API_BASE_URL}/api/v1/bots/${botId}/move?x=${x}&y=${y}`, {
      method: 'POST'
    })
    if (!response.ok) throw new Error('Failed to move bot')
    return response.json()
  }
}

// Custom hooks with React Query
const useMapGrid = () => {
  const [data, setData] = React.useState<MapGrid | null>(null)
  const [isLoading, setIsLoading] = React.useState(true)
  const [error, setError] = React.useState<string | null>(null)

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await apiService.getMapGrid()
        setData(result)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 2000)
    return () => clearInterval(interval)
  }, [])

  return { data, isLoading, error }
}

const useOrders = () => {
  const [data, setData] = React.useState<Order[]>([])
  const [isLoading, setIsLoading] = React.useState(true)

  React.useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await apiService.getAllOrders()
        setData(result)
      } catch (err) {
        console.error('Failed to fetch orders:', err)
      } finally {
        setIsLoading(false)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 2000)
    return () => clearInterval(interval)
  }, [])

  return { data, isLoading }
}

const useRestaurants = () => {
  const [data, setData] = React.useState<Restaurant[]>([])

  React.useEffect(() => {
    apiService.getRestaurants().then(setData).catch(console.error)
  }, [])

  return { data }
}

const useDeliveryPoints = () => {
  const [data, setData] = React.useState<DeliveryPoint[]>([])

  React.useEffect(() => {
    apiService.getDeliveryPoints().then(setData).catch(console.error)
  }, [])

  return { data }
}

// Components
const SystemStats: React.FC<{ gridData: MapGrid | null; orders: Order[] }> = ({ gridData, orders }) => {
  if (!gridData) return null

  const stats = {
    totalBots: gridData.total_bots,
    activeBots: Object.values(gridData.grid).map(cell => 
      cell.bots.filter(bot => bot.status == 'IDLE')).length,
    totalOrders: orders.length,
    pendingOrders: orders.filter(o => o.status === 'PENDING').length,
    activeOrders: orders.filter(o => ['ASSIGNED', 'PICKED_UP'].includes(o.status)).length,
    deliveredOrders: orders.filter(o => o.status === 'DELIVERED').length
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <Activity className="w-5 h-5 mr-2" />
        System Status
      </h3>
      <div className="grid grid-cols-2 gap-4">
        <div className="bg-blue-50 p-4 rounded-lg">
          <div className="text-sm text-blue-600 font-medium">Active Bots</div>
          <div className="text-2xl font-bold text-blue-800">{stats.activeBots}/{stats.totalBots}</div>
        </div>
        <div className="bg-orange-50 p-4 rounded-lg">
          <div className="text-sm text-orange-600 font-medium">Pending Orders</div>
          <div className="text-2xl font-bold text-orange-800">{stats.pendingOrders}</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-sm text-green-600 font-medium">Active Deliveries</div>
          <div className="text-2xl font-bold text-green-800">{stats.activeOrders}</div>
        </div>
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="text-sm text-purple-600 font-medium">Completed</div>
          <div className="text-2xl font-bold text-purple-800">{stats.deliveredOrders}</div>
        </div>
      </div>
    </div>
  )
}

const OrderForm: React.FC<{
  restaurants: Restaurant[]
  deliveryPoints: DeliveryPoint[]
  onOrderCreated: () => void
}> = ({ restaurants, deliveryPoints, onOrderCreated }) => {
  const [formData, setFormData] = useState({
    customer_name: '',
    customer_phone: '',
    restaurant_type: '' as 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI' | '',
    pickup_x: 0,
    pickup_y: 0,
    delivery_x: 0,
    delivery_y: 0
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    if (!formData.customer_name || !formData.restaurant_type || !formData.delivery_x) {
      setError('Please fill in all required fields')
      return
    }

    setIsSubmitting(true)
    setError('')
    
    try {
      await apiService.createOrder(formData)
      setFormData({
        customer_name: '',
        customer_phone: '',
        restaurant_type: '',
        pickup_x: 0,
        pickup_y: 0,
        delivery_x: 0,
        delivery_y: 0
      })
      onOrderCreated()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create order')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleRestaurantChange = (restaurantType: string) => {
    const restaurant = restaurants.find(r => r.restaurant_type === restaurantType)
    if (restaurant) {
      setFormData(prev => ({
        ...prev,
        restaurant_type: restaurantType as 'RAMEN' | 'CURRY' | 'PIZZA' | 'SUSHI',
        pickup_x: restaurant.x,
        pickup_y: restaurant.y
      }))
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <Package className="w-5 h-5 mr-2" />
        Create New Order
      </h3>
      
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3 mb-4">
          <div className="flex">
            <AlertTriangle className="w-5 h-5 text-red-400 mr-2" />
            <div className="text-sm text-red-700">{error}</div>
          </div>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Customer Name *
          </label>
          <input
            type="text"
            value={formData.customer_name}
            onChange={(e) => setFormData(prev => ({...prev, customer_name: e.target.value}))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter customer name"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Phone Number
          </label>
          <input
            type="text"
            value={formData.customer_phone}
            onChange={(e) => setFormData(prev => ({...prev, customer_phone: e.target.value}))}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Optional"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Restaurant *
          </label>
          <select
            value={formData.restaurant_type}
            onChange={(e) => handleRestaurantChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">Select Restaurant</option>
            {restaurants.map(restaurant => (
              <option key={restaurant.id} value={restaurant.restaurant_type}>
                {restaurant.name} ({restaurant.restaurant_type}) - ({restaurant.x}, {restaurant.y})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Delivery Address *
          </label>
          <select
            value={`${formData.delivery_x},${formData.delivery_y}`}
            onChange={(e) => {
              const [xStr, yStr] = e.target.value.split(',')
              const x = Number(xStr)
              const y = Number(yStr)
              setFormData(prev => ({...prev, delivery_x: x, delivery_y: y}))
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="0,0">Select Delivery Address</option>
            {deliveryPoints.map(point => (
              <option key={point.id} value={`${point.x},${point.y}`}>
                {point.name} - ({point.x}, {point.y})
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleSubmit}
          disabled={isSubmitting}
          className={clsx(
            "w-full py-2 px-4 rounded-md text-white font-medium transition-colors",
            isSubmitting
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-600 hover:bg-blue-700"
          )}
        >
          {isSubmitting ? 'Creating Order...' : 'Create Order'}
        </button>
      </div>
    </div>
  )
}

const GridMap: React.FC<{
  gridData: MapGrid | null
  selectedBot: number | null
  onCellClick: (x: number, y: number, cell: GridCell) => void
}> = ({ gridData, selectedBot, onCellClick }) => {
  if (!gridData) {
    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">Loading map...</span>
        </div>
      </div>
    )
  }

  const renderCell = (x: number, y: number) => {
    const cellKey = `${x},${y}`
    const cell = gridData.grid[cellKey]
    if (!cell) return null

    let cellClasses = 'w-10 h-10 border border-gray-300 flex flex-col items-center justify-center cursor-pointer transition-all hover:scale-105 text-xs'
    let cellContent = ''
    let bgColor = 'bg-gray-50'
    
    // Determine cell type and styling
    if (cell.is_restaurant) {
      bgColor = 'bg-yellow-200'
      cellContent = cell.restaurant_type?.[0] || 'R'
    } else if (cell.is_delivery_point) {
      bgColor = 'bg-green-200'
      cellContent = '🏠'
    } else if (cell.is_bot_station) {
      bgColor = 'bg-purple-200'
      cellContent = '⚡'
    }

    // Add bots if present
    if (cell.bots && cell.bots.length > 0) {
      bgColor = 'bg-blue-400'
      cellContent = `🤖${cell.bots[0]?.id}`
      if (selectedBot === cell.bots[0]?.id) {
        cellClasses += ' ring-4 ring-red-400'
      }
    }

    // Add orders if present
    if (cell.active_orders && cell.active_orders.length > 0) {
      cellClasses += ' ring-2 ring-orange-400'
    }

    return (
      <div
        key={cellKey}
        className={clsx(cellClasses, bgColor)}
        onClick={() => onCellClick(x, y, cell)}
        title={`(${x},${y}) ${cell.name}`}
      >
        <div className="font-bold">{cellContent}</div>
        <div className="text-xs text-gray-600">{x},{y}</div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <MapPin className="w-5 h-5 mr-2" />
        Delivery Map (9x9 Grid)
      </h3>
      
      <div className="grid grid-cols-9 gap-1 border-2 border-gray-800 p-2 bg-gray-100 rounded-lg">
        {Array.from({ length: 9 }, (_, y) =>
          Array.from({ length: 9 }, (_, x) => renderCell(x, y))
        )}
      </div>
      
      <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
        <div className="space-y-1">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-blue-400 rounded mr-2"></div>
            <span>🤖 = Bot</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-green-200 rounded mr-2"></div>
            <span>🏠 = House</span>
          </div>
        </div>
        <div className="space-y-1">
          <div className="flex items-center">
            <div className="w-4 h-4 bg-yellow-200 rounded mr-2"></div>
            <span>R/P/C/S = Restaurant</span>
          </div>
          <div className="flex items-center">
            <div className="w-4 h-4 bg-purple-200 rounded mr-2"></div>
            <span>⚡ = Bot Station</span>
          </div>
        </div>
      </div>
    </div>
  )
}

const OrderList: React.FC<{ orders: Order[] }> = ({ orders }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDING': return 'text-orange-600 bg-orange-100'
      case 'ASSIGNED': return 'text-blue-600 bg-blue-100'
      case 'PICKED_UP': return 'text-green-600 bg-green-100'
      case 'DELIVERED': return 'text-emerald-600 bg-emerald-100'
      case 'CANCELLED': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center">
        <Package className="w-5 h-5 mr-2" />
        Orders ({orders.length})
      </h3>
      
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {orders.length === 0 ? (
          <p className="text-gray-500 text-center py-8">No orders yet. Create your first order!</p>
        ) : (
          orders.map(order => (
            <div key={order.id} className="border border-gray-200 rounded-lg p-4 bg-gray-50">
              <div className="flex justify-between items-start mb-2">
                <span className="font-semibold text-gray-800">#{order.id}</span>
                <span className={clsx(
                  "px-2 py-1 rounded-full text-xs font-medium",
                  getStatusColor(order.status)
                )}>
                  {order.status}
                </span>
              </div>
              <div className="space-y-1 text-sm text-gray-600">
                <div className="font-medium text-gray-800">{order.customer_name}</div>
                <div>{order.restaurant_type} from ({order.pickup_x}, {order.pickup_y})</div>
                <div>To ({order.delivery_x}, {order.delivery_y})</div>
                {order.bot_id && <div>Bot: #{order.bot_id}</div>}
                {order.estimated_time && <div>ETA: {order.estimated_time}s</div>}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

const EagRouteApp: React.FC = () => {
  const [selectedBot, setSelectedBot] = useState<number | null>(null)
  const { data: gridData, isLoading: gridLoading, error: gridError } = useMapGrid()
  const { data: orders, isLoading: ordersLoading } = useOrders()
  const { data: restaurants } = useRestaurants()
  const { data: deliveryPoints } = useDeliveryPoints()

  const handleCellClick = async (x: number, y: number, cell: GridCell) => {
    if (selectedBot != null && cell.bots.length === 0) {
      try {
        await apiService.moveBot(selectedBot, x, y)
        setSelectedBot(null)
      } catch (error) {
        console.error('Error moving bot:', error)
      }
    } else if (cell.bots && cell.bots.length > 0) {
      setSelectedBot(cell.bots[0]!.id)
    }
  }

  const handleOrderCreated = () => {
    // Orders will auto-refresh via polling
  }

  if (gridError) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-md p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Connection Error</h2>
            <p className="text-gray-600 mb-4">Unable to connect to the EagRoute backend.</p>
            <p className="text-sm text-gray-500">Make sure the backend is running on http://localhost:8000</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Bot className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-xl font-semibold text-gray-800">EagRoute - Delivery Bot System</h1>
            </div>
            {selectedBot && (
              <div className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
                Selected Bot: #{selectedBot} (Click empty cell to move)
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Panel */}
          <div className="lg:col-span-3 space-y-6">
            <SystemStats gridData={gridData} orders={orders} />
            <OrderForm 
              restaurants={restaurants}
              deliveryPoints={deliveryPoints}
              onOrderCreated={handleOrderCreated}
            />
          </div>

          {/* Center Panel */}
          <div className="lg:col-span-6">
            <GridMap 
              gridData={gridData}
              selectedBot={selectedBot}
              onCellClick={handleCellClick}
            />
          </div>

          {/* Right Panel */}
          <div className="lg:col-span-3">
            <OrderList orders={orders} />
          </div>
        </div>
      </main>
    </div>
  )
}

// Create QueryClient
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5000,
      refetchOnWindowFocus: false,
    },
  },
})

// Main App with Providers
const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <EagRouteApp />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

export default App
